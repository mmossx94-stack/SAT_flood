/**
 * Disater_BKK_DB — JK World canals API
 *
 * ใช้ข้อมูลจาก:
 *   https://world.tehx.dyndns.info/api/v1/canals
 *
 * หลักการ:
 * - เก็บภาพข้อมูลล่าสุด 1 แถวต่อสถานี (ไม่ใช่ history)
 * - รักษา schema 23 คอลัมน์เดิม เพื่อให้ Dashboard/สูตรเดิมใช้ต่อได้
 * - null คงเป็นค่าว่าง ไม่แปลงเป็น 0
 * - ค่า -99 ถือเป็น sentinel และไม่เขียนเป็นระดับน้ำ แต่เก็บไว้ใน raw_station_json
 * - ระดับน้ำคลองเป็น “เมตร รทก.” ไม่ใช่ความลึกน้ำท่วมถนน
 * - freshness คำนวณเทียบเวลาวัดกับเวลาที่ Apps Script ดึงข้อมูล
 */
const BKK_CONFIG = Object.freeze({
  SPREADSHEET_URL: 'https://docs.google.com/spreadsheets/d/1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4/edit?usp=drivesdk', // วางลิงก์ Google Sheets เช่น https://docs.google.com/spreadsheets/d/FILE_ID/edit
  SHEET_NAME: 'Disater_BKK_DB',
  JK_CANALS_URL: 'https://world.tehx.dyndns.info/api/v1/canals',
  TIMEZONE: 'Asia/Bangkok',
  STALE_MINUTES: 60,
  INTERVAL_MINUTES: 10
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
    .addItem('เปิดอัปเดตทุก 10 นาที', 'installBkkWaterTrigger')
    .addItem('ปิดอัปเดตอัตโนมัติ', 'removeBkkWaterTrigger')
    .addSeparator()
    .addItem('ทดสอบ JK World API', 'testJKWorldCanals')
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
  if (!lock.tryLock(1000)) {
    console.log('ข้ามรอบนี้: มีการอัปเดตอยู่');
    return;
  }

  const props = PropertiesService.getScriptProperties();

  try {
    const id = bkkSpreadsheetId_();
    const batch = bkkFetchBatch_(); // ตรวจให้ครบก่อนแก้ตารางเดิม
    const fetchedAt = batch.fetchedAt;
    const rows = batch.rows;

    const ss = SpreadsheetApp.openById(id);
    let sheet = ss.getSheetByName(BKK_CONFIG.SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(BKK_CONFIG.SHEET_NAME);

    if (sheet.getLastRow() > 0) {
      const oldHeader = sheet.getRange(1, 1, 1, BKK_HEADERS.length).getValues()[0];
      if (sheet.getLastColumn() !== BKK_HEADERS.length ||
          JSON.stringify(oldHeader) !== JSON.stringify(BKK_HEADERS)) {
        throw new Error(
          'แท็บ ' + BKK_CONFIG.SHEET_NAME +
          ' มีหัวตารางไม่ตรง schema 23 คอลัมน์เดิม กรุณาสำรองข้อมูลก่อนแก้ไข'
        );
      }
    }

    const values = [BKK_HEADERS].concat(rows);
    const previousRows = sheet.getLastRow();

    if (sheet.getMaxRows() < values.length) {
      sheet.insertRowsAfter(sheet.getMaxRows(), values.length - sheet.getMaxRows());
    }
    if (sheet.getMaxColumns() < BKK_HEADERS.length) {
      sheet.insertColumnsAfter(sheet.getMaxColumns(), BKK_HEADERS.length - sheet.getMaxColumns());
    }

    sheet.getRange(1, 1, values.length, BKK_HEADERS.length).setValues(values);

    // ล้างเฉพาะข้อมูลเก่าที่เกินจำนวนแถวชุดใหม่ หลังเขียนชุดใหม่สำเร็จแล้ว
    if (previousRows > values.length) {
      sheet.getRange(values.length + 1, 1, previousRows - values.length, BKK_HEADERS.length).clearContent();
    }

    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, BKK_HEADERS.length)
      .setBackground('#174b64')
      .setFontColor('#ffffff')
      .setFontWeight('bold');

    if (rows.length) {
      sheet.getRange(2, 6, rows.length, 2).setNumberFormat('0.00000');
      sheet.getRange(2, 9, rows.length, 5).setNumberFormat('0.00');
    }

    sheet.setColumnWidth(3, 360);
    sheet.setColumnWidth(4, 200);
    sheet.setColumnWidth(5, 200);
    sheet.setColumnWidth(8, 190);
    sheet.setColumnWidth(19, 190);
    sheet.setColumnWidth(21, 190);
    sheet.setColumnWidth(22, 360);

    sheet.getRange('A1').setNote(
      'อัปเดตสำเร็จ: ' + bkkThaiTime_(fetchedAt) +
      '\nจำนวนสถานี: ' + rows.length +
      '\nแหล่งข้อมูลรอบนี้: JK World /api/v1/canals' +
      '\nX-Data-Updated: ' + (batch.dataUpdated || 'ไม่มี header') +
      '\nระดับน้ำคลองเป็นเมตรเหนือระดับน้ำทะเลปานกลาง (ม.รทก.) ไม่ใช่ความลึกน้ำบนถนน' +
      '\nnull = ไม่มีข้อมูล ห้ามตีความเป็น 0' +
      '\nค่า -99 ไม่เขียนลงคอลัมน์ระดับน้ำ แต่ตรวจพบได้จาก has_minus99_source และ raw_station_json' +
      '\nfreshness_at_fetch คำนวณจาก observed_at_th ณ เวลาดึงข้อมูล เกิน 60 นาที = ข้อมูลเก่าเกิน 60 นาที' +
      '\nJK World เป็นผู้รวบรวม/จัดแสดงข้อมูล ไม่ใช่ประกาศเตือนภัยทางการ' +
      '\nข้อมูลต้นทางหลักของจุดคลอง: สำนักการระบายน้ำ กรุงเทพมหานคร ผ่าน JK World'
    );

    SpreadsheetApp.flush();
    props.setProperty('BKK_LAST_SUCCESS', fetchedAt.toISOString());
    props.deleteProperty('BKK_LAST_ERROR');

    console.log('อัปเดต ' + rows.length + ' สถานี เวลา ' + bkkThaiTime_(fetchedAt));
  } catch (error) {
    props.setProperty('BKK_LAST_ERROR', new Date().toISOString() + ' | ' + error.message);
    console.error(error);
    throw error;
  } finally {
    lock.releaseLock();
  }
}

/**
 * ดึง JK World JSON พร้อม header X-Data-Updated
 */
function bkkFetchJson_(url) {
  const response = UrlFetchApp.fetch(url, {
    method: 'get',
    followRedirects: true,
    muteHttpExceptions: true,
    headers: {
      Accept: 'application/json'
    }
  });

  const code = response.getResponseCode();
  const text = response.getContentText('UTF-8');

  if (code !== 200) {
    throw new Error(url + ' ตอบ HTTP ' + code + ': ' + text.slice(0, 500));
  }

  let payload;
  try {
    payload = JSON.parse(text);
  } catch (e) {
    throw new Error('JK World ตอบกลับมาไม่ใช่ JSON ที่อ่านได้');
  }

  const headers = response.getHeaders();
  const dataUpdated = headers['X-Data-Updated'] || headers['x-data-updated'] || '';

  return { payload, dataUpdated };
}

function bkkFetchBatch_() {
  const fetchedAt = new Date();
  const result = bkkFetchJson_(BKK_CONFIG.JK_CANALS_URL);
  const sourceRows = bkkExtractStationArray_(result.payload);

  if (!sourceRows.length) {
    throw new Error('JK World /canals ไม่มีรายการสถานี จึงไม่แทนที่ข้อมูลเดิม');
  }

  const rows = bkkBuildJKWorldRows_(sourceRows, fetchedAt);

  return {
    rows,
    fetchedAt,
    source: 'JK World /api/v1/canals',
    dataUpdated: result.dataUpdated
  };
}

/**
 * รองรับ payload หลายรูปแบบ โดยไม่ผูกกับ wrapper ชื่อเดียว
 * เช่น [] หรือ {data: []} หรือ {canals: []} หรือ {stations: []}
 */
function bkkExtractStationArray_(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload || typeof payload !== 'object') return [];

  const preferred = ['data', 'canals', 'stations', 'items', 'results'];
  for (const key of preferred) {
    if (Array.isArray(payload[key])) return payload[key];
  }

  // เผื่อ API ซ้อนอีกชั้น เช่น data.canals / result.data
  for (const key of Object.keys(payload)) {
    const value = payload[key];
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      for (const innerKey of preferred) {
        if (Array.isArray(value[innerKey])) return value[innerKey];
      }
    }
  }

  return [];
}

function bkkBuildJKWorldRows_(sourceRows, fetchedAt) {
  const seen = new Set();

  return sourceRows.map((r, index) => {
    if (!r || typeof r !== 'object') {
      throw new Error('รายการสถานีลำดับ ' + (index + 1) + ' ไม่ใช่ object');
    }

    const rawId = bkkFirst_(r, [
      'station_id', 'id', 'water_id', 'station.id', 'station.station_id', 'sensor_id'
    ]);

    const stationCode = bkkFirst_(r, [
      'station_code', 'code', 'water_code', 'station_code_old',
      'station.code', 'station.station_code', 'station.canal_oldcode'
    ]);

    const stationName = bkkFirst_(r, [
      'station_name', 'name', 'water_name', 'station.name',
      'station.station_name', 'canal_name', 'station.canal_name.th'
    ]);

    if ((rawId === null || rawId === undefined || rawId === '') && !stationCode && !stationName) {
      throw new Error('ไม่พบ id/code/name ของสถานี JK World ลำดับ ' + (index + 1));
    }

    const identity = rawId !== null && rawId !== undefined && rawId !== ''
      ? String(rawId)
      : String(stationCode || stationName);

    const stationId = /^JKWORLD:/i.test(identity) ? identity : 'JKWORLD:' + identity;

    if (seen.has(stationId)) {
      throw new Error('รหัสสถานีซ้ำจาก JK World: ' + stationId);
    }
    seen.add(stationId);

    const district = bkkFirst_(r, [
      'district', 'district_name', 'district_or_area', 'area',
      'geocode.amphoe_name.th', 'location.district', 'station.district'
    ]);

    const canal = bkkFirst_(r, [
      'canal', 'canal_name', 'river_name', 'waterway',
      'station.canal_name.th', 'station.canal_name', 'location.canal'
    ]);

    const lat = bkkFirst_(r, [
      'lat', 'latitude', 'station_lat', 'canal_lat',
      'station.lat', 'station.latitude', 'station.canal_lat', 'location.lat', 'location.latitude'
    ]);

    const lng = bkkFirst_(r, [
      'lng', 'lon', 'long', 'longitude', 'station_lng', 'canal_long',
      'station.lng', 'station.lon', 'station.longitude', 'station.canal_long',
      'location.lng', 'location.lon', 'location.longitude'
    ]);

    const observedRaw = bkkFirst_(r, [
      'ts', 'measured_at', 'observed_at', 'updated', 'updated_at', 'timestamp',
      'site_timestamp', 'datetime', 'canal_datetime', 'measurement.measured_at'
    ]);
    const observed = bkkObservedDate_(observedRaw);

    const waterInRaw = bkkFirst_(r, [
      'water_level', 'level', 'water_level_m_msl', 'water_in_m_msl',
      'wl_in', 'canal_value', 'value', 'measurement.value', 'measurement.level'
    ]);

    const waterOut01Raw = bkkFirst_(r, [
      'water_out01_m_msl', 'wl_out01', 'water_out01', 'out01'
    ]);

    const waterOut02Raw = bkkFirst_(r, [
      'water_out02_m_msl', 'wl_out02', 'water_out02', 'out02'
    ]);

    const warning = bkkFirst_(r, [
      'warning_level', 'warning', 'warning_in_source',
      'thresholds.warning', 'station.warning_level'
    ]);

    const critical = bkkFirst_(r, [
      'critical_level', 'critical', 'critical_in_source',
      'thresholds.critical', 'station.critical_level'
    ]);

    // JK World `status` สื่อสถานะข้อมูล/ความสด เช่น stale, nodata
    // ไม่ใช่ระดับน้ำท่วม จึงเก็บใน sensor_status_source
    const sensorStatusRaw = bkkFirst_(r, [
      'status', 'sensor_status', 'device_status', 'water_status', 'sensor_status_source',
      'health', 'station.status'
    ]);

    // สถานะระดับน้ำคำนวณจาก level เทียบ warning/critical ของต้นทาง
    const floodAssessment = bkkAssessCanalLevel_(waterInRaw, warning, critical);
    const floodStatusRaw = floodAssessment.status;
    const floodCode = floodAssessment.code;

    const sensorCode = bkkSensorStatusCode_(sensorStatusRaw);

    const age = observed
      ? Math.round(((fetchedAt.getTime() - observed.getTime()) / 60000) * 10) / 10
      : '';

    const freshness = bkkFreshness_(age);

    const rawValuesForMinus99 = [
      waterInRaw, waterOut01Raw, waterOut02Raw, warning, critical
    ];
    const hasMinus99 = rawValuesForMinus99.some(v => v !== null && v !== undefined && Number(v) === -99);

    return [
      stationId,
      stationCode,
      stationName,
      district,
      canal,
      bkkNumber_(lat),
      bkkNumber_(lng),
      observed ? bkkThaiTime_(observed) : (observedRaw || ''),
      bkkLevel_(waterInRaw),
      bkkLevel_(waterOut01Raw),
      bkkLevel_(waterOut02Raw),
      bkkLevel_(warning),
      bkkLevel_(critical),
      bkkStatusText_(floodStatusRaw),
      bkkStatusText_(sensorStatusRaw),
      bkkNumberOrText_(floodCode),
      bkkNumberOrText_(sensorCode),
      age,
      freshness,
      hasMinus99,
      bkkThaiTime_(fetchedAt),
      BKK_CONFIG.JK_CANALS_URL,
      JSON.stringify(r)
    ].map(bkkCell_);
  });
}

/**
 * อ่านค่า nested path โดยคืน “ค่าตัวแรกที่มีอยู่จริง”
 * สำคัญ: 0 และ false ถือเป็นค่าที่ถูกต้อง ไม่ถูกข้าม
 */
function bkkFirst_(obj, paths) {
  for (const path of paths) {
    const parts = path.split('.');
    let cur = obj;
    let exists = true;

    for (const part of parts) {
      if (cur === null || cur === undefined ||
          typeof cur !== 'object' ||
          !Object.prototype.hasOwnProperty.call(cur, part)) {
        exists = false;
        break;
      }
      cur = cur[part];
    }

    if (exists && cur !== null && cur !== undefined && cur !== '') {
      // ถ้าเป็น object ภาษา เช่น {th:'...', en:'...'} ให้เลือก th ก่อน
      if (typeof cur === 'object' && !Array.isArray(cur)) {
        if (cur.th !== null && cur.th !== undefined && cur.th !== '') return cur.th;
        if (cur.en !== null && cur.en !== undefined && cur.en !== '') return cur.en;
      } else {
        return cur;
      }
    }
  }
  return '';
}

function bkkFreshness_(ageMinutes) {
  if (ageMinutes === '' || ageMinutes === null || ageMinutes === undefined) return 'ไม่มีเวลา';
  if (!Number.isFinite(Number(ageMinutes))) return 'ไม่มีเวลา';
  if (Number(ageMinutes) < 0) return 'เวลาอนาคต';
  if (Number(ageMinutes) > BKK_CONFIG.STALE_MINUTES) return 'ข้อมูลเก่าเกิน 60 นาที';
  return 'ข้อมูลไม่เกิน 60 นาที';
}

function bkkStatusText_(value) {
  if (value === null || value === undefined || value === '') return 'ไม่ทราบ';
  if (typeof value === 'object') {
    if (value.th !== null && value.th !== undefined && value.th !== '') return String(value.th);
    if (value.en !== null && value.en !== undefined && value.en !== '') return String(value.en);
    return JSON.stringify(value);
  }
  return String(value);
}

function bkkNumberOrText_(value) {
  if (value === null || value === undefined || value === '') return '';
  return Number.isFinite(Number(value)) ? Number(value) : String(value);
}


/**
 * จัดระดับสถานการณ์จากค่าระดับน้ำเทียบ threshold ที่ API ส่งมา
 * code: 0=ปกติ, 1=เฝ้าระวัง, 2=วิกฤต, 9=ไม่มีข้อมูล
 */
function bkkAssessCanalLevel_(level, warning, critical) {
  const lv = bkkNumericOrNull_(level);
  const w = bkkNumericOrNull_(warning);
  const c = bkkNumericOrNull_(critical);

  if (lv === null) return { status: 'ไม่มีข้อมูล', code: 9 };
  if (c !== null && lv >= c) return { status: 'วิกฤต', code: 2 };
  if (w !== null && lv >= w) return { status: 'เฝ้าระวัง', code: 1 };
  return { status: 'ปกติ', code: 0 };
}

/** JK World status -> code สำหรับใช้งานในชีท */
function bkkSensorStatusCode_(status) {
  const s = String(status || '').toLowerCase();
  if (!s) return '';
  if (s === 'nodata') return 2;
  if (s === 'stale') return 1;
  if (s === 'ok' || s === 'normal' || s === 'fresh') return 0;
  return '';
}

function bkkNumericOrNull_(v) {
  if (v === null || v === undefined || v === '' || Number(v) === -99) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function installBkkWaterTrigger() {
  // ตรวจลิงก์และสิทธิ์ก่อนเปลี่ยน trigger
  SpreadsheetApp.openById(bkkSpreadsheetId_());
  removeBkkWaterTrigger();
  ScriptApp.newTrigger('updateBkkWater')
    .timeBased()
    .everyMinutes(BKK_CONFIG.INTERVAL_MINUTES)
    .create();
}

function removeBkkWaterTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'updateBkkWater') {
      ScriptApp.deleteTrigger(t);
    }
  });
}

/**
 * ทดสอบการเชื่อมต่อโดยไม่แตะข้อมูลในชีท
 * ดูผลที่ Executions > Logs
 */
function testJKWorldCanals() {
  const result = bkkFetchJson_(BKK_CONFIG.JK_CANALS_URL);
  const rows = bkkExtractStationArray_(result.payload);
  console.log('HTTP JSON OK');
  console.log('X-Data-Updated: ' + (result.dataUpdated || 'ไม่มี'));
  console.log('generated: ' + (result.payload.generated || 'ไม่มี'));
  console.log('sources: ' + JSON.stringify(result.payload.sources || []));
  console.log('unit: ' + (result.payload.unit || 'ไม่มี'));
  console.log('จำนวนรายการที่ตรวจพบ: ' + rows.length);
  if (rows.length) {
    console.log('ตัวอย่าง record แรก: ' + JSON.stringify(rows[0], null, 2));
    console.log('ตัวอย่างแถวหลัง normalize: ' + JSON.stringify(bkkBuildJKWorldRows_([rows[0]], new Date())[0], null, 2));
  }
}

function bkkSpreadsheetId_() {
  return bkkParseSpreadsheetUrl_(BKK_CONFIG.SPREADSHEET_URL);
}

function bkkParseSpreadsheetUrl_(value) {
  const match = /^https:\/\/docs\.google\.com\/spreadsheets\/d\/([a-zA-Z0-9_-]+)(?:[/?#]|$)/
    .exec(String(value || '').trim());

  if (!match || match[1] === 'FILE_ID') {
    throw new Error(
      'กรุณาใส่ลิงก์ Google Sheets จริงใน BKK_CONFIG.SPREADSHEET_URL เช่น ' +
      'https://docs.google.com/spreadsheets/d/รหัสไฟล์/edit'
    );
  }
  return match[1];
}

function bkkObservedDate_(value) {
  if (!value) return null;

  // รองรับ epoch seconds / milliseconds
  if (typeof value === 'number' && Number.isFinite(value)) {
    const ms = value < 100000000000 ? value * 1000 : value;
    const d = new Date(ms);
    return isNaN(d.getTime()) ? null : d;
  }

  let text = String(value).trim();
  if (!text) return null;

  // YYYY-MM-DD HH:mm[:ss] -> ISO-like
  text = text.replace(' ', 'T');

  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(text)) return null;

  // JK World ระบุเวลาเป็นไทย UTC+7 หาก field ไม่มี timezone ให้เติม +07:00
  if (!/(Z|[+-]\d{2}:?\d{2})$/i.test(text)) text += '+07:00';

  const date = new Date(text);
  return isNaN(date.getTime()) ? null : date;
}

function bkkThaiTime_(date) {
  return Utilities.formatDate(date, BKK_CONFIG.TIMEZONE, "yyyy-MM-dd'T'HH:mm:ss") + '+07:00';
}

function bkkNumber_(v) {
  return v === null || v === undefined || v === '' || !Number.isFinite(Number(v))
    ? ''
    : Number(v);
}

function bkkLevel_(v) {
  return Number(v) === -99 ? '' : bkkNumber_(v);
}

function bkkCell_(v) {
  if (v === null || v === undefined) return '';

  // ป้องกันข้อความต้นทางกลายเป็นสูตรใน Google Sheets
  return typeof v === 'string' && /^[=+@-]/.test(v) ? "'" + v : v;
}
