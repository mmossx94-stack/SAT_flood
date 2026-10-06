function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setTitle('รายงานสถานการณ์สาธารณภัยรายจังหวัด (ปภ.)');
}

function getDashboardData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 1. ข้อมูลน้ำท่วม (สมมติว่าเป็น Sheet แรกถ้าไม่ระบุชื่อ)
  var floodSheet = ss.getSheets()[0];
  var floodData = floodSheet.getDataRange().getValues();
  var floodResult = parseSheetData(floodData);
  
  // 2. ข้อมูลกลุ่มเปราะบาง
  var vulSheet = ss.getSheetByName('Vulnerable_group');
  var vulResult = vulSheet ? parseSheetData(vulSheet.getDataRange().getValues()) : [];
  
  // 3. ข้อมูลน้ำ กทม.
  var bkkWaterSheet = ss.getSheetByName('BKK_water_DB');
  var bkkWaterResult = bkkWaterSheet ? parseSheetData(bkkWaterSheet.getDataRange().getValues()) : [];
  
  // 4. ข้อมูลน้ำ ประเทศไทย
  var thaiWaterSheet = ss.getSheetByName('thai_water_DB');
  var thaiWaterResult = thaiWaterSheet ? parseSheetData(thaiWaterSheet.getDataRange().getValues()) : [];
  
  // 5. ข้อมูลศูนย์พักพิง
  var shelterSheet = ss.getSheetByName('shelter_DB');
  var shelterResult = shelterSheet ? parseSheetData(shelterSheet.getDataRange().getValues()) : [];
  
  return {
    floodData: floodResult,
    vulData: vulResult,
    bkkWaterData: bkkWaterResult,
    thaiWaterData: thaiWaterResult,
    shelterData: shelterResult
  };
}

function parseSheetData(data) {
  if (data.length <= 1) return [];
  var headers = data[0];
  var result = [];
  
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var obj = {};
    for (var j = 0; j < headers.length; j++) {
      var cellValue = row[j];
      if (cellValue instanceof Date) {
        obj[headers[j]] = Utilities.formatDate(cellValue, Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm");
      } else {
        obj[headers[j]] = cellValue;
      }
    }
    result.push(obj);
  }
  return result;
}
