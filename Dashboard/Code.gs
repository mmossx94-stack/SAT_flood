function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setTitle('รายงานสถานการณ์สาธารณภัยรายจังหวัด (ปภ.)');
}

function getDashboardData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  var floodSheet = ss.getSheets()[0];
  var floodData = floodSheet ? parseSheetData(floodSheet.getDataRange().getValues()) : [];
  
  var vulSheet = ss.getSheetByName('Vulnerable_group');
  var vulResult = vulSheet ? parseSheetData(vulSheet.getDataRange().getValues()) : [];
  
  var bkkWaterSheet = ss.getSheetByName('BKK_water_DB');
  var bkkWaterResult = bkkWaterSheet ? parseSheetData(bkkWaterSheet.getDataRange().getValues()) : [];
  
  var thaiWaterSheet = ss.getSheetByName('thai_water_DB');
  var thaiWaterResult = thaiWaterSheet ? parseSheetData(thaiWaterSheet.getDataRange().getValues()) : [];
  
  var shelterSheet = ss.getSheetByName('shelter_DB');
  var shelterResult = shelterSheet ? parseSheetData(shelterSheet.getDataRange().getValues()) : [];

  var trendsSheet = ss.getSheetByName('Google_Trends_DB');
  var trendsResult = null;
  if (trendsSheet) {
    var rawJson = trendsSheet.getRange('A1').getValue();
    if (rawJson) {
      try {
        trendsResult = JSON.parse(rawJson);
      } catch (e) {
        trendsResult = null;
      }
    }
  }
  
  return {
    floodData: floodResult,
    vulData: vulResult,
    bkkWaterData: bkkWaterResult,
    thaiWaterData: thaiWaterResult,
    shelterData: shelterResult,
    trendsData: trendsResult
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
        obj[headers[j]] = Utilities.formatDate(cellValue, Session.getScriptTimeZone(), 'dd/MM/yyyy HH:mm');
      } else {
        obj[headers[j]] = cellValue;
      }
    }
    result.push(obj);
  }
  return result;
}