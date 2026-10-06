/**
 * ใส่ลิงก์ Google Sheets ใน SPREADSHEET_URL แล้วรัน setupBkkWater()
 * ใช้ได้ทั้งสคริปต์แยกที่ script.google.com และสคริปต์ที่ผูกกับชีท
 * ปลายทางคือแท็บ Disater_BKK_DB ในไฟล์ตามลิงก์ (ไม่ใช้ gid เลือกแท็บ)
 * เก็บภาพข้อมูลล่าสุด 1 แถวต่อสถานี ไม่ใช่ประวัติย้อนหลัง
 */
const BKK_CONFIG = Object.freeze({
  SPREADSHEET_URL: '', // วางลิงก์ เช่น https://docs.google.com/spreadsheets/d/FILE_ID/edit
  SHEET_NAME: 'Disater_BKK_DB',
  SOURCE_URL: 'https://weather.bangkok.go.th/water/summary',
  SOURCE_MODE: 'AUTO', // AUTO = กทม. ก่อน แล้ว ThaiWater; THAIWATER = ใช้ ThaiWater โดยตรง
  THAIWATER_URL: 'https://api-v3.thaiwater.net/api/v1/thaiwater30/public/canal_waterlevel',
  TIMEZONE: 'Asia/Bangkok',
  STALE_MINUTES: 1440,
  INTERVAL_MINUTES: 15
});

const BKK_HEADERS = [
  'station_id', 'station_code', 'station_name', 'district_or_area', 'canal',
  'latitude', 'longitude', 'observed_at_th',
  'water_in_m_msl', 'water_out01_m_msl', 'water_out02_m_msl',
  'warning_in_source', 'critical_in_source',
  'flood_status_source', 'sensor_status_source',
  'flood_status_code', 'sensor_status_code',
  'age_minutes_at_fetch', 'freshness_at_fetch', 'has_minus99_source',
  'fetched_at_th', 'source_url', 'raw_station_json'
];

function onOpen() {
  SpreadsheetApp.getUi().createMenu('น้ำ กทม.')
    .addItem('ตั้งค่าและดึงครั้งแรก', 'setupBkkWater')
    .addItem('อัปเดตข้อมูล', 'updateBkkWater')
    .addSeparator()
    .addItem('เปิดอัปเดตทุก 15 นาที', 'installBkkWaterTrigger')
    .addItem('ปิดอัปเดตอัตโนมัติ', 'removeBkkWaterTrigger')
    .addToUi();
}

function setupBkkWater() {
  const spreadsheetId = bkkSpreadsheetId_();
  updateBkkWater();
  console.log('ดึงข้อมูลแล้วสำหรับ spreadsheet ' + spreadsheetId +
    '. หากต้องการอัตโนมัติ ให้รัน installBkkWaterTrigger');
}

function updateBkkWater() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) { console.log('ข้ามรอบนี้: มีการอัปเดตอยู่'); return; }
  const props = PropertiesService.getScriptProperties();
  try {
    const id = bkkSpreadsheetId_();
    const batch = bkkFetchBatch_(); // ตรวจข้อมูลครบก่อนแตะตารางเดิม
    const fetchedAt = batch.fetchedAt;
    const rows = batch.rows;
    const ss = SpreadsheetApp.openById(id);
    let sheet = ss.getSheetByName(BKK_CONFIG.SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(BKK_CONFIG.SHEET_NAME);
    if (sheet.getLastRow() > 0) {
      if (sheet.getLastColumn() !== BKK_HEADERS.length ||
          JSON.stringify(sheet.getRange(1, 1, 1, BKK_HEADERS.length).getValues()[0]) !== JSON.stringify(BKK_HEADERS)) {
        throw new Error('แท็บ ' + BKK_CONFIG.SHEET_NAME + ' มีข้อมูล/หัวตารางอื่นอยู่ กรุณาย้ายข้อมูลเดิมหรือเปลี่ยนชื่อแท็บก่อน');
      }
    }
    const values = [BKK_HEADERS].concat(rows);
    const previousRows = sheet.getLastRow();
    if (sheet.getMaxRows() < values.length) sheet.insertRowsAfter(sheet.getMaxRows(), values.length - sheet.getMaxRows());
    if (sheet.getMaxColumns() < BKK_HEADERS.length) sheet.insertColumnsAfter(sheet.getMaxColumns(), BKK_HEADERS.length - sheet.getMaxColumns());
    sheet.getRange(1, 1, values.length, BKK_HEADERS.length).setValues(values);
    // ล้างเฉพาะแถวเก่าที่เกิน หลังเขียนชุดใหม่สำเร็จ
    if (previousRows > values.length) sheet.getRange(values.length + 1, 1, previousRows - values.length, BKK_HEADERS.length).clearContent();
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, BKK_HEADERS.length).setBackground('#174b64').setFontColor('#ffffff').setFontWeight('bold');
    sheet.getRange(2, 6, rows.length, 2).setNumberFormat('0.00000');
    sheet.getRange(2, 9, rows.length, 5).setNumberFormat('0.00');
    sheet.setColumnWidth(3, 360);
    sheet.setColumnWidth(4, 200);
    sheet.setColumnWidth(5, 200);
    sheet.setColumnWidth(8, 180);
    sheet.setColumnWidth(21, 180);
    sheet.getRange('A1').setNote(
      'อัปเดตสำเร็จ: ' + bkkThaiTime_(fetchedAt) + '\nจำนวนสถานี: ' + rows.length +
      '\nแหล่งข้อมูลรอบนี้: ' + batch.source +
      '\nเหตุผลใช้สำรอง: ' + (batch.fallbackReason || 'ไม่ได้ใช้สำรอง') +
      '\nระดับน้ำ ม.รทก. ไม่ใช่ความลึกน้ำท่วมถนน' +
      '\nสถานะน้ำและเครื่องวัดยึดต้นทาง ไม่คำนวณสถานะจากเกณฑ์ใหม่' +
      '\nรหัสเครื่องวัด 0/3 ยังไม่ยืนยันความหมาย จึงแสดงไม่ทราบ' +
      '\nnull และ -99 แสดงว่างในคอลัมน์ระดับน้ำ; ค่าเดิมอยู่ใน raw_station_json' +
      '\nเวลาเป็นข้อความ ISO เวลาไทย มี +07:00; freshness คำนวณ ณ เวลาดึง ไม่เปลี่ยนเองระหว่างรอบ' +
      '\nข้อมูลเป็นชุดล่าสุด รวมสถานีพื้นที่นอก กทม. ตามต้นทาง'
      + '\nThaiWater: ไม่ได้ให้สถานะเครื่อง/สถานะเตือนแบบ กทม. จึงแสดงไม่ทราบ ไม่คำนวณแทน' +
      '\nThaiWater: station_id ใช้คำนำหน้า THAIWATER: เพราะเป็นคนละระบบรหัส; จับคู่ข้ามแหล่งด้วย station_code' +
      '\nThaiWater: canal_out เก็บใน raw_station_json เท่านั้น จนยืนยันความหมายของฟิลด์ได้' +
      '\nการสลับแหล่งแทนที่ทั้งชุด จำนวนและเวลาวัดอาจต่างกัน ไม่รวมข้อมูลข้ามแหล่ง'
    );
    SpreadsheetApp.flush();
    props.setProperty('BKK_LAST_SUCCESS', fetchedAt.toISOString());
    props.deleteProperty('BKK_LAST_ERROR');
    console.log('อัปเดต ' + rows.length + ' สถานี เวลา ' + bkkThaiTime_(fetchedAt));
  } catch (error) {
    props.setProperty('BKK_LAST_ERROR', new Date().toISOString() + ' | ' + error.message);
    console.error(error);
    throw error; // ให้หน้า Executions และระบบแจ้งข้อผิดพลาดของ trigger แสดงความล้มเหลว
  } finally { lock.releaseLock(); }
}

function bkkFetchText_(url, accept) {
  const response = UrlFetchApp.fetch(url, {
    method: 'get', followRedirects: true, muteHttpExceptions: true,
    headers: { Accept: accept }
  });
  if (response.getResponseCode() !== 200) throw new Error(url + ' ตอบ HTTP ' + response.getResponseCode());
  return response.getContentText('UTF-8');
}

function bkkFetchBatch_() {
  if (!['AUTO', 'THAIWATER'].includes(BKK_CONFIG.SOURCE_MODE)) throw new Error('SOURCE_MODE ต้องเป็น AUTO หรือ THAIWATER');
  let fallbackReason = '';
  if (BKK_CONFIG.SOURCE_MODE === 'AUTO') {
    try {
      const html = bkkFetchText_(BKK_CONFIG.SOURCE_URL, 'text/html');
      const fetchedAt = new Date();
      const rows = bkkBuildRows_(bkkExtractArray_(html, 'waterSummaryList'), bkkExtractArray_(html, 'districtList'), fetchedAt);
      return {rows, fetchedAt, source: 'สำนักการระบายน้ำ กทม. โดยตรง', fallbackReason};
    } catch (error) {
      fallbackReason = error.message;
      console.warn('ใช้ ThaiWater สำรอง: ' + fallbackReason);
    }
  }
  try {
    const payload = JSON.parse(bkkFetchText_(BKK_CONFIG.THAIWATER_URL, 'application/json'));
    const fetchedAt = new Date();
    const rows = bkkBuildThaiwaterRows_(payload, fetchedAt);
    return {rows, fetchedAt, source: 'สำนักการระบายน้ำ กทม. ผ่าน ThaiWater', fallbackReason};
  } catch (error) {
    throw new Error((fallbackReason ? 'กทม.: ' + fallbackReason + ' | ' : '') + 'ThaiWater: ' + error.message);
  }
}

function bkkBuildThaiwaterRows_(payload, fetchedAt) {
  if (!payload || payload.result !== 'OK' || !Array.isArray(payload.data)) throw new Error('รูปแบบ ThaiWater ไม่ตรงที่รองรับ');
  const sourceRows = payload.data.filter(r => r.agency && r.agency.agency_name &&
    r.agency.agency_name.th === 'สำนักการระบายน้ำ กรุงเทพมหานคร');
  if (!sourceRows.length) throw new Error('ThaiWater ไม่มีสถานีของสำนักการระบายน้ำ กทม.');
  const districts = [];
  const normalized = sourceRows.map((r, i) => {
    if (!r.station || r.station.id == null || !Object.prototype.hasOwnProperty.call(r, 'canal_value')) throw new Error('สถานี ThaiWater ไม่ครบ');
    districts.push({district_id: i, name: r.geocode && r.geocode.amphoe_name ? r.geocode.amphoe_name.th : ''});
    return {
      water_id: 'THAIWATER:' + r.station.id, water_code: r.station.canal_oldcode,
      water_name: r.station.canal_name && r.station.canal_name.th, district_id: i,
      river_name: '', latitude: r.station.canal_lat, longitude: r.station.canal_long,
      site_timestamp: r.canal_datetime, wl_in: r.canal_value,
      wl_out01: null, wl_out02: null,
      warning: r.station.warning_level, critical: r.station.critical_level,
      water_status_flood: null, water_status: null
    };
  });
  return bkkBuildRows_(normalized, districts, fetchedAt).map((row, i) => {
    row[21] = BKK_CONFIG.THAIWATER_URL;
    row[22] = JSON.stringify(sourceRows[i]);
    return row;
  });
}

function installBkkWaterTrigger() {
  // ตรวจลิงก์และสิทธิ์ก่อนเปลี่ยน trigger
  SpreadsheetApp.openById(bkkSpreadsheetId_());
  removeBkkWaterTrigger();
  ScriptApp.newTrigger('updateBkkWater').timeBased().everyMinutes(BKK_CONFIG.INTERVAL_MINUTES).create();
}

function removeBkkWaterTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'updateBkkWater') ScriptApp.deleteTrigger(t);
  });
}

function bkkSpreadsheetId_() {
  return bkkParseSpreadsheetUrl_(BKK_CONFIG.SPREADSHEET_URL);
}

function bkkParseSpreadsheetUrl_(value) {
  const match = /^https:\/\/docs\.google\.com\/spreadsheets\/d\/([a-zA-Z0-9_-]+)(?:[/?#]|$)/.exec(String(value || '').trim());
  if (!match || match[1] === 'FILE_ID') {
    throw new Error('กรุณาใส่ลิงก์ Google Sheets จริงใน BKK_CONFIG.SPREADSHEET_URL เช่น https://docs.google.com/spreadsheets/d/รหัสไฟล์/edit');
  }
  return match[1];
}

// อ่าน JSON array โดยนับวงเล็บและตรวจ string โดยไม่ execute JavaScript จากเว็บ
function bkkExtractArray_(html, name) {
  const match = new RegExp('\\b(?:const|let|var)\\s+' + name + '\\s*=\\s*\\[').exec(html);
  if (!match) throw new Error('ต้นทางเปลี่ยนรูปแบบ: ไม่พบ ' + name + ' (ยังไม่เขียนข้อมูล)');
  const start = match.index + match[0].lastIndexOf('[');
  let depth = 0, inString = false, escaped = false;
  for (let i = start; i < html.length; i++) {
    const c = html[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === '"') inString = false;
    } else if (c === '"') inString = true;
    else if (c === '[') depth++;
    else if (c === ']' && --depth === 0) return JSON.parse(html.slice(start, i + 1));
  }
  throw new Error('JSON ต้นทางไม่ครบ: ' + name);
}

function bkkBuildRows_(stations, districts, fetchedAt) {
  if (!Array.isArray(stations) || !stations.length || !Array.isArray(districts) || !districts.length) {
    throw new Error('ต้นทางไม่มีข้อมูลสถานี/เขต จึงไม่แทนที่ข้อมูลเดิม');
  }
  const names = new Map(districts.map(d => [String(d.district_id), d.name]));
  const seen = new Set();
  return stations.map(s => {
    if (!s || s.water_id == null || !s.water_name || !Object.prototype.hasOwnProperty.call(s, 'wl_in')) {
      throw new Error('โครงสร้างสถานีไม่ตรงรูปแบบที่รองรับ');
    }
    const id = String(s.water_id);
    if (seen.has(id)) throw new Error('รหัสสถานีซ้ำ: ' + id);
    seen.add(id);
    const observed = bkkObservedDate_(s.site_timestamp);
    const age = observed ? (fetchedAt.getTime() - observed.getTime()) / 60000 : '';
    const freshness = age === '' ? 'ไม่มีเวลา' : age < 0 ? 'เวลาอนาคต' : age > BKK_CONFIG.STALE_MINUTES ? 'ข้อมูลเก่า' : 'ภายใน 24 ชั่วโมง';
    const flood = ({1: 'ปกติ', 2: 'เตือนภัย', 3: 'วิกฤติ'})[s.water_status_flood] || 'ไม่ทราบ';
    const sensor = ({1: 'ปกติ', 2: 'ขัดข้อง'})[s.water_status] || 'ไม่ทราบ';
    return [
      s.water_id, s.water_code, s.water_name, names.get(String(s.district_id)) || '', s.river_name,
      bkkNumber_(s.latitude), bkkNumber_(s.longitude), observed ? bkkThaiTime_(observed) : (s.site_timestamp || ''),
      bkkLevel_(s.wl_in), bkkLevel_(s.wl_out01), bkkLevel_(s.wl_out02),
      bkkNumber_(s.warning), bkkNumber_(s.critical), flood, sensor,
      s.water_status_flood, s.water_status, age, freshness,
      [s.wl_in, s.wl_out01, s.wl_out02].some(v => v != null && Number(v) === -99),
      bkkThaiTime_(fetchedAt), BKK_CONFIG.SOURCE_URL, JSON.stringify(s)
    ].map(bkkCell_);
  });
}

function bkkObservedDate_(value) {
  if (!value) return null;
  let text = String(value).trim().replace(' ', 'T');
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(text)) return null;
  if (!/(Z|[+-]\d{2}:?\d{2})$/i.test(text)) text += '+07:00';
  const date = new Date(text);
  return isNaN(date.getTime()) ? null : date;
}
function bkkThaiTime_(date) { return Utilities.formatDate(date, BKK_CONFIG.TIMEZONE, "yyyy-MM-dd'T'HH:mm:ss") + '+07:00'; }
function bkkNumber_(v) { return v === null || v === undefined || v === '' || !Number.isFinite(Number(v)) ? '' : Number(v); }
function bkkLevel_(v) { return Number(v) === -99 ? '' : bkkNumber_(v); }
function bkkCell_(v) {
  if (v === null || v === undefined) return '';
  // ข้อความต้นทางต้องไม่กลายเป็นสูตรในชีท
  return typeof v === 'string' && /^[=+@-]/.test(v) ? "'" + v : v;
}
