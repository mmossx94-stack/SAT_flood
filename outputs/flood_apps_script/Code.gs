const SPREADSHEET_ID = '1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4';

function doGet(e) {
  // We will serve the Index.html file
  let template = HtmlService.createTemplateFromFile('Index');
  return template.evaluate()
      .setTitle('Dashboard เฝ้าระวังน้ำ - กรมอนามัย')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Function to fetch data from sheets
function getDashboardData() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  
  const disasters = getSheetDataAsObjects(ss, 'Disaster_DB');
  const thaiWater = getSheetDataAsObjects(ss, 'thai_water_DB');
  const bkkWater = getSheetDataAsObjects(ss, 'BKK_water_DB');
  const shelters = getSheetDataAsObjects(ss, 'shelter_DB');
  const vulnerable = getSheetDataAsObjects(ss, 'Vulnerable_Group_DB');

  return JSON.stringify({
    disasters: disasters,
    thai_water: thaiWater,
    bkk_water: bkkWater,
    shelters: shelters,
    vulnerable: vulnerable
  });
}

function getSheetDataAsObjects(ss, sheetName) {
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];
  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];
  
  const headers = data[0];
  const rows = data.slice(1);
  
  return rows.map(row => {
    let obj = {};
    headers.forEach((header, i) => {
      let val = row[i];
      if (val instanceof Date) {
        obj[header] = Utilities.formatDate(val, "GMT+07:00", "yyyy-MM-dd'T'HH:mm:ssXXX");
      } else if (typeof val === 'string' && /^\d{1,2}\/\d{1,2}\/\d{4}/.test(val.trim())) {
        // Handle Thai string dates like "03/10/2569 03:15"
        let m = val.trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?/);
        if (m) {
          let y = parseInt(m[3], 10);
          if (y > 2500) y -= 543; // Convert Buddhist to Gregorian
          let d = m[1].padStart(2, '0');
          let mth = m[2].padStart(2, '0');
          let h = (m[4] || '0').padStart(2, '0');
          let mn = (m[5] || '0').padStart(2, '0');
          let s = (m[6] || '0').padStart(2, '0');
          obj[header] = `${y}-${mth}-${d}T${h}:${mn}:${s}+07:00`;
        } else {
          obj[header] = val;
        }
      } else {
        obj[header] = val;
      }
    });
    return obj;
  });
}

function getGeoJson() {
  // We can't easily store huge JSON in GAS code without making it ugly, 
  // so we'll put the raw JSON in a separate HTML file and include it.
  return HtmlService.createHtmlOutputFromFile('GeoJSON').getContent();
}
