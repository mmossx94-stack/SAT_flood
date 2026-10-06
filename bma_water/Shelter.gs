/** เพิ่มไฟล์ Shelter.gs ใน Apps Script เดิม แล้วรัน setupShelter ครั้งเดียว */
const SHELTER_CONFIG = Object.freeze({
  SPREADSHEET_ID: '1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4',
  SHEET_NAME: 'shelter_DB',
  URL: 'https://floodsupport.bangkok.go.th/api/data',
  STALE_MINUTES: 1440,
  CATEGORY: 'ศูนย์พักพิงชั่วคราว'
});
const SHELTER_HEADERS = [
  'shelter_id','district','shelter_name','category','capacity','occupied','available',
  'unit','status_source','map_url','additional_details','route_details',
  'created_at_source','updated_at_source','source_generated_at','source_stale',
  'fetched_at_th','source_url','raw_record_json',
  'latitude','longitude','coordinate_status','coordinate_url','coordinate_checked_at',
  'map_url_found','map_search_status','map_search_query_url','map_matched_address',
  'map_place_id','map_search_checked_at',
  'age_minutes_at_fetch','freshness_at_fetch'
];

const SHELTER_MANUAL_COORDS = {
  "d47bf7af-910f-be9a-1015-e3669c6d6b59": [
    13.7130698,
    100.4934718,
    "bma_school.json"
  ],
  "6c09bbed-58f3-8db6-bcb6-00abd4d65cd7": [
    13.7340192,
    100.5064446,
    "bma_school.json"
  ],
  "ae6a1e1f-dd60-8eda-1312-b16fafab6a1c": [
    13.7331238,
    100.5083614,
    "bma_school.json"
  ],
  "893d718f-1fc7-05d1-eb9c-bd57f45498f1": [
    13.7244692,
    100.5007125,
    "bma_school.json"
  ],
  "4b8d7251-8897-a8c9-625c-b32f8ae6c9f7": [
    13.7327454,
    100.4971926,
    "bma_school.json"
  ],
  "08267586-0c76-6a16-1c46-515a9b01b6b9": [
    13.7131086,
    100.4934223,
    "bma_school.json"
  ],
  "cb64c88c-65ac-4406-89a5-fbad303fcc1c": [
    13.724199,
    100.5104975,
    "bma_school.json"
  ],
  "2b25b8c2-0107-1c5d-5e8c-0256ef0c4a9d": [
    13.7131209,
    100.5060561,
    "bma_school.json"
  ],
  "64581ef2-b823-cc2e-f161-dbe4285ff141": [
    13.8538904,
    100.5620488,
    "bma_school.json"
  ],
  "57c52eca-7e19-268b-5ebb-ac4470cebbb6": [
    13.8404236,
    100.5562791,
    "bma_school.json"
  ],
  "e5c896e0-c1df-34db-4f87-8a8096472399": [
    13.8317499,
    100.5883609,
    "bma_school.json"
  ],
  "db069ece-3cc7-20fa-1725-1988e6dc3f3f": [
    13.9495167,
    100.615449,
    "bma_school.json"
  ],
  "8404aba6-d4dc-3f49-49d0-f491f6fa42b7": [
    13.9214919,
    100.6010932,
    "bma_school.json"
  ],
  "f121cc39-0c1b-298e-d247-72fbee6948d5": [
    13.7807771,
    100.5156618,
    "bma_school.json"
  ],
  "165c7fd3-3a14-d02d-b852-f0f3982eb9c0": [
    13.7730088,
    100.5016567,
    "bma_school.json"
  ],
  "078156ff-1e9f-4177-a2e5-fd725054a93b": [
    13.7835033,
    100.3838333,
    "bma_school.json"
  ],
  "b17e35b9-6828-468b-a753-c3fe90479a46": [
    13.7555626,
    100.3516647,
    "bma_school.json"
  ],
  "3dc7b92c-20e7-4ddd-a7eb-6012a01bae5c": [
    13.7686342,
    100.368626,
    "bma_school.json"
  ],
  "0d95bb9d-216c-4ef9-86ee-d1ea0d829e25": [
    13.8026823,
    100.3523604,
    "bma_school.json"
  ],
  "f02dc659-7a22-4af6-9ee1-ef413273225a": [
    13.8012417,
    100.3369944,
    "bma_school.json"
  ],
  "8fb662a7-69f9-4d75-a6df-a72562a364c8": [
    13.8015209,
    100.3352201,
    "bma_school.json"
  ],
  "b7fbc4ec-56dc-7900-ace2-5a8cb685c8d3": [
    13.6357191,
    100.514756,
    "bma_school.json"
  ],
  "53dda150-1b18-5d9a-b257-8a6ac2829450": [
    13.6571443,
    100.5095495,
    "bma_school.json"
  ],
  "7df1767c-2913-ffbe-3e81-865a4cbac662": [
    13.6476913,
    100.4950497,
    "bma_school.json"
  ],
  "cc3501f8-bf75-048f-f0ee-4727755df689": [
    13.654502,
    100.4716705,
    "bma_school.json"
  ],
  "00dd767b-4ec9-4c4e-c430-ada69841114c": [
    13.6347802,
    100.5031628,
    "bma_school.json"
  ],
  "5f3d517f-7411-6ec9-a5c9-a551da2a0905": [
    13.6192295,
    100.5120069,
    "bma_school.json"
  ],
  "79cc73f1-16f8-9235-2c4a-1f071b1038f9": [
    13.6457149,
    100.5113544,
    "bma_school.json"
  ],
  "aebb8f0d-7ac8-d49b-d135-593c2b1fdfd7": [
    13.7176477,
    100.4783538,
    "bma_school.json"
  ],
  "f67cbe20-e844-b6cd-7310-25d620ec280f": [
    13.7406484,
    100.4908449,
    "bma_school.json"
  ],
  "3b0e9445-1ce4-5723-1c23-da82162e37c8": [
    13.719847,
    100.4709283,
    "bma_school.json"
  ],
  "069ac5a8-91fe-780c-a74a-9ba5e0989daf": [
    13.7040946,
    100.4907039,
    "bma_school.json"
  ],
  "359aec1a-274a-d748-a423-5add85e49f90": [
    13.7003749,
    100.4883414,
    "bma_school.json"
  ],
  "f1300896-d216-7e56-6c87-240e8926a5fa": [
    13.7290148,
    100.4885865,
    "bma_school.json"
  ],
  "408c77d3-f1cb-ae83-42c8-10264d62b45b": [
    13.7621124,
    100.477667,
    "bma_school.json"
  ],
  "2d3f5e3a-ce0d-b5ea-d5ce-84df66b6c82a": [
    13.7412336,
    100.474829,
    "bma_school.json"
  ],
  "f756b6cc-f792-aa4b-4ec9-b06b801c2883": [
    13.7334763,
    100.4728119,
    "bma_school.json"
  ],
  "cff5b16f-1252-0b88-3a6f-4279772b7420": [
    13.7241142,
    100.4691135,
    "bma_school.json"
  ],
  "78d45971-6b69-1ddd-881c-c1136700e90f": [
    13.7357938,
    100.4850235,
    "bma_school.json"
  ],
  "f7f239f3-5482-e34f-2314-deb837b99281": [
    13.7411726,
    100.4822686,
    "bma_school.json"
  ],
  "057ef1e1-7837-f250-3c3e-3636b741f981": [
    13.8088566,
    100.5197171,
    "bma_school.json"
  ],
  "e8b14651-ee91-f6ce-c7e7-0b796b904096": [
    13.7319111,
    100.5286106,
    "bma_school.json"
  ],
  "8a1c081f-f06b-a37a-f746-76cee889174d": [
    13.7317807,
    100.5194975,
    "bma_school.json"
  ],
  "58d18f0f-184f-425a-b34c-ec7a042127a3": [
    13.6807733,
    100.5486882,
    "bma_school.json"
  ],
  "f18749f9-1bb1-fc13-0fd9-128f5bb46a9b": [
    13.7548505,
    100.8571279,
    "bma_school.json"
  ],
  "92ce774c-8709-f476-ce12-a42ab1d2f458": [
    13.7318374,
    100.8377682,
    "bma_school.json"
  ],
  "8bb3b656-819d-8ba2-5d1a-394d5600d7a8": [
    13.7426308,
    100.7557878,
    "bma_school.json"
  ],
  "1d4a03e3-61d7-ae7f-fd30-68dbd475d5a5": [
    13.7768417,
    100.7381436,
    "bma_school.json"
  ],
  "87957c08-9e83-fad5-051d-8173cd27bed6": [
    13.7269937,
    100.7524152,
    "bma_school.json"
  ],
  "f972891e-249a-d6ee-d41c-e53a087128d2": [
    13.7254454,
    100.7200408,
    "bma_school.json"
  ],
  "71c4ce5c-d133-efe4-0e62-58419ffc6266": [
    13.7263666,
    100.7377299,
    "bma_school.json"
  ],
  "8a114428-c8c2-f3fe-86a8-73bd768f9cdf": [
    13.7402499,
    100.7954481,
    "bma_school.json"
  ],
  "785e557e-e447-a3a7-6499-971bf3730fb6": [
    13.7657276,
    100.7304156,
    "bma_school.json"
  ],
  "73063bec-9106-8f60-9180-e25f2eaec5d4": [
    13.748239,
    100.7243466,
    "bma_school.json"
  ],
  "b5a72573-170d-53df-6af8-5d8ceb2e153e": [
    13.7127983,
    100.812968,
    "bma_school.json"
  ],
  "3f3b5a42-1de4-d401-613c-21be82ca8966": [
    13.8003197,
    100.6128105,
    "bma_school.json"
  ],
  "46ce6821-25ab-4575-ed92-b26fa4f869a5": [
    13.8403222,
    100.6324374,
    "bma_school.json"
  ],
  "210b3783-4da3-eae5-37cd-69104091b0c8": [
    13.8473866,
    100.6040203,
    "bma_school.json"
  ],
  "7656bb34-1b58-5bd3-6280-11379aac5fa5": [
    13.8031513,
    100.5902427,
    "bma_school.json"
  ],
  "7c341567-761f-bfa7-751f-b399f48363d8": [
    13.8322177,
    100.590927,
    "bma_school.json"
  ],
  "f5e6984e-42e7-218c-d4f7-c5d1f63f80b4": [
    13.8228948,
    100.6157542,
    "bma_school.json"
  ],
  "7f5f5105-0333-4b10-9153-1f419f53bdbc": [
    13.7196572,
    100.5866531,
    "bma_school.json"
  ],
  "f595791c-1730-ef8f-574d-4689a44f6c6f": [
    13.7398013,
    100.5662809,
    "bma_school.json"
  ],
  "ed3b58c3-55c8-4bee-7681-c29a1cf2dd20": [
    13.7154035,
    100.5969278,
    "bma_school.json"
  ],
  "2b9d72d0-ab1f-578c-d2e3-7205d40f2f4c": [
    13.7431516,
    100.5802374,
    "bma_school.json"
  ],
  "fefd59ba-944e-230c-db96-42bcf6831f43": [
    13.727914,
    100.5962,
    "bma_school.json"
  ],
  "012012bb-7bee-2d90-e5fe-c648e1b66142": [
    13.7391706,
    100.5877197,
    "bma_school.json"
  ],
  "e9209803-630c-4768-81ad-8da226b91c72": [
    13.7583472,
    100.6965257,
    "bma_school.json"
  ],
  "730c9de8-15b4-419d-afa7-6726a100827f": [
    13.7403079,
    100.6922842,
    "bma_school.json"
  ],
  "2bc70ccc-aa67-4dc5-ae69-b22d8f58bf94": [
    13.7803467,
    100.7016735,
    "bma_school.json"
  ],
  "8247b8db-8742-4645-a7be-e1e18036cf0a": [
    13.7691558,
    100.6948509,
    "bma_school.json"
  ],
  "296cf755-32af-482c-b455-6cb6b1cfabd3": [
    13.7436495,
    100.6996266,
    "bma_school.json"
  ],
  "c6aee575-ed2c-4ed4-aefb-1fce9936e1d0": [
    13.7698743,
    100.7134803,
    "bma_school.json"
  ],
  "d7ce38ae-dada-b91c-d326-c04d4be15c5a": [
    13.9041444,
    100.812104,
    "bma_school.json"
  ],
  "b4d829a9-ce79-ed07-8323-b7d37f76731b": [
    13.8734112,
    100.5532913,
    "bma_school.json"
  ],
  "fd747b69-e217-0d07-2f83-e21ae0e4312b": [
    13.8853393,
    100.5604221,
    "bma_school.json"
  ],
  "40fdb062-ea65-a686-4cbf-9cf2eef1bd0f": [
    13.8608221,
    100.5671252,
    "bma_school.json"
  ],
  "a38fdd2a-6876-5bb5-740f-50b294f14d4b": [
    13.889233,
    100.5824933,
    "bma_school.json"
  ],
  "03f082a0-8c14-8b45-6faf-02fe835f3a39": [
    13.9009975,
    100.5832113,
    "bma_school.json"
  ],
  "d82e09a3-e241-b961-bdde-b8af57f46921": [
    13.9022826,
    100.5785958,
    "bma_school.json"
  ],
  "12135531-bf8d-18d0-0d58-727f2f37a01e": [
    13.8200212,
    100.5775218,
    "nominatim_or_manual"
  ],
  "9f1c27dc-35ca-d9bf-1f98-89db992049b8": [
    13.8545494,
    100.5621327,
    "nominatim_or_manual"
  ],
  "866d79e5-6d6a-1532-3281-758768670715": [
    13.7812793,
    100.5156583,
    "nominatim_or_manual"
  ],
  "86b84da7-fd67-e137-13bc-1760c72970e7": [
    13.7771293,
    100.522973,
    "nominatim_or_manual"
  ],
  "88883e8b-442c-31fd-848a-d1b15046cc07": [
    13.7802808,
    100.5115001,
    "nominatim_or_manual"
  ],
  "10a55cee-cc6f-4f0a-a61e-eab585c09bd4": [
    13.76005,
    100.51616,
    "nominatim_or_manual"
  ],
  "e5ee61e4-9f67-ef99-64ab-7f36778882fd": [
    13.766,
    100.514,
    "nominatim_or_manual"
  ],
  "8f4df65b-c5a8-6569-50a5-112d3fe4a7b1": [
    13.7172432,
    100.6946855,
    "nominatim_or_manual"
  ],
  "64a84257-a1fc-9759-ad8d-1b0266abd743": [
    13.683518,
    100.6652647,
    "nominatim_or_manual"
  ],
  "5ac1597a-6790-d7a2-04c4-75d255fe2c21": [
    13.795578,
    100.5479366,
    "nominatim_or_manual"
  ],
  "ed542ef7-11b3-3d96-fa5f-fe027618ee14": [
    13.6936784,
    100.5938422,
    "nominatim_or_manual"
  ],
  "c40024d9-10b8-1ce2-4a5b-32a5139672e3": [
    13.6914189,
    100.6351071,
    "nominatim_or_manual"
  ],
  "4094bbd8-3137-4ccd-bf38-ae725cb44174": [
    13.7263458,
    100.7794033,
    "nominatim_or_manual"
  ],
  "ae48d8db-3682-063f-d0a0-c2f41011e2cf": [
    13.7414571,
    100.8530263,
    "nominatim_or_manual"
  ],
  "70e3808f-2cec-c049-6c34-f9252640f14f": [
    13.8465621,
    100.6047116,
    "nominatim_or_manual"
  ],
  "d9026e04-5cbd-b52d-fe4d-d8d150a4b6d2": [
    13.7303867,
    100.6514719,
    "nominatim_or_manual"
  ],
  "1532c37b-861f-9dc5-3729-daff0b15fd94": [
    13.7315471,
    100.5138159,
    "nominatim_or_manual"
  ],
  "3634a4d1-8d0a-5f3e-2500-7eb6b5e4c130": [
    13.7428564,
    100.503868,
    "nominatim_or_manual"
  ],
  "7c4c03f9-10bc-44f0-ad6a-b7c314ec8563": [
    13.7915347,
    100.3541175,
    "manual_approximate"
  ],
  "558ba1d1-b0ab-3071-1f0e-2a17bd80ad4f": [
    13.804868,
    100.537651,
    "manual_approximate"
  ],
  "23707524-79a4-8878-c056-8879498da0ee": [
    13.8115682,
    100.5284059,
    "manual_approximate"
  ],
  "ad3a1af1-7fed-4791-19dd-0371c220c153": [
    13.70425,
    100.39578,
    "manual_approximate"
  ],
  "f5313405-82de-a3c2-69fa-36b25f99866e": [
    13.68453,
    100.61367,
    "manual_approximate"
  ],
  "09a0444e-4181-c113-8486-412d5d65c3bb": [
    13.72251,
    100.7816,
    "manual_approximate"
  ],
  "ce5239a0-c88d-c6b6-2e50-8d3648d550be": [
    13.83272,
    100.62772,
    "manual_approximate"
  ],
  "92e9c61f-23ba-d76a-0d6b-afb89269c167": [
    13.7381,
    100.6267,
    "manual_approximate"
  ],
  "786a9010-5577-4011-90cb-f18ac61451af": [
    13.76632,
    100.69741,
    "manual_approximate"
  ],
  "0f7918ff-cedd-4203-a4bc-4a1c65644a95": [
    13.7374828,
    100.6865239,
    "manual_approximate"
  ],
  "7580563e-242d-a3c5-93a8-64fdba5806a5": [
    13.8055653,
    100.8358482,
    "manual_approximate"
  ]
};


// ดึงครั้งแรกสำเร็จก่อน จึงติดตั้ง Trigger ทุก 1 ชั่วโมงให้โดยอัตโนมัติ
function setupShelter() {
  updateShelter();
  installShelterTrigger();
  console.log('พร้อมใช้งาน: shelter_DB และ Trigger ทุก 1 ชั่วโมง');
}

function updateShelter() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('ระบบอื่นกำลังอัปเดต กรุณาลองรอบถัดไป');
  try {
    const response = UrlFetchApp.fetch(SHELTER_CONFIG.URL, {
      method:'get',followRedirects:true,muteHttpExceptions:true,
      headers:{Accept:'application/json'}
    });
    if (response.getResponseCode() !== 200) throw new Error('Flood Support HTTP ' + response.getResponseCode());
    const fetchedAt = new Date();
    const payload = JSON.parse(response.getContentText('UTF-8'));
    const rows = shelterBuildRows_(payload, fetchedAt);
    const ss = SpreadsheetApp.openById(SHELTER_CONFIG.SPREADSHEET_ID);
    let sheet = ss.getSheetByName(SHELTER_CONFIG.SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(SHELTER_CONFIG.SHEET_NAME);
    const width = SHELTER_HEADERS.length, oldRows = sheet.getLastRow();
    const oldWidth = sheet.getLastColumn();
    if (oldRows) {
      const expected = SHELTER_HEADERS.slice(0,oldWidth);
      if (![19,24,30,width].includes(oldWidth) || JSON.stringify(sheet.getRange(1,1,1,oldWidth).getValues()[0]) !== JSON.stringify(expected))
        throw new Error('shelter_DB มีหัวตารางอื่นอยู่ จึงไม่เขียนทับ');
    }
    const previous = oldRows > 1 ? sheet.getRange(2,1,oldRows-1,oldWidth).getValues() : [];
    shelterAddCoordinates_(rows, previous, fetchedAt);
    shelterFindMissingMaps_(rows, fetchedAt);
    rows.forEach(row => {
      const age = shelterAgeMinutes_(row[13], fetchedAt);
      row[30] = age;
      row[31] = age === '' ? 'ไม่ทราบเวลาข้อมูล' : age < 0 ? 'เวลาต้นทางอยู่ในอนาคต' : age > SHELTER_CONFIG.STALE_MINUTES ? 'ข้อมูลเก่าเกิน 24 ชั่วโมง' : 'ภายใน 24 ชั่วโมง';
    });
    const values = [SHELTER_HEADERS].concat(rows);
    if (sheet.getMaxRows() < values.length) sheet.insertRowsAfter(sheet.getMaxRows(),values.length-sheet.getMaxRows());
    if (sheet.getMaxColumns() < width) sheet.insertColumnsAfter(sheet.getMaxColumns(),width-sheet.getMaxColumns());
    sheet.getRange(1,1,values.length,width).setValues(values);
    if (oldRows > values.length) sheet.getRange(values.length+1,1,oldRows-values.length,width).clearContent();
    sheet.setFrozenRows(1);
    sheet.getRange(1,1,1,width).setFontWeight('bold').setBackground('#e8eef3');
    sheet.setColumnWidth(3,320);
    sheet.setColumnWidths(13,5,190);
    sheet.getRange(2,20,rows.length,2).setNumberFormat('0.000000');
    sheet.getRange('A1').setNote('ข้อมูลจาก BMA Flood Support เฉพาะศูนย์พักพิงชั่วคราว\nจำนวน '+rows.length+
      '\nรับข้อมูล '+shelterThaiTime_(fetchedAt)+'\nเวลา created/updated/generated เก็บตามต้นทาง ไม่แทนด้วยเวลาที่ดึง'+
      '\nsource_stale คือสถานะข้อมูลสำรองที่ API รายงาน ไม่ใช่การรับรองว่าทุกศูนย์อัปเดตล่าสุด'+
      '\nช่องว่างไม่ใช่ศูนย์ ที่ว่างและสถานะใช้ค่าต้นทาง ไม่คำนวณใหม่'+
      '\nmap_url_found มาจาก Google Geocoder โดยตรวจชื่อสถานที่และเขตตรงกันแบบเข้มงวด ไม่ใช่การยืนยันโดยเจ้าหน้าที่'+
      '\nmap_search_query_url เป็นเพียงลิงก์ค้นหา ไม่ใช่สถานที่ที่ยืนยันแล้ว');
    SpreadsheetApp.flush();
    console.log('อัปเดต shelter_DB สำเร็จ '+rows.length+' รายการ เวลา '+shelterThaiTime_(fetchedAt));
  } finally { lock.releaseLock(); }
}

function shelterBuildRows_(payload, fetchedAt) {
  if (!payload || !Array.isArray(payload.facilities) || !Array.isArray(payload.categories) ||
      !payload.categories.includes(SHELTER_CONFIG.CATEGORY)) throw new Error('รูปแบบ API เปลี่ยน ไม่เขียนทับข้อมูลเดิม');
  const records = payload.facilities.filter(r=>r && r.category === SHELTER_CONFIG.CATEGORY);
  if (!records.length) throw new Error('ต้นทางไม่มีศูนย์พักพิงในรอบนี้ คงข้อมูลเดิมไว้');
  const seen = new Set();
  return records.map(r=>{
    if (!r.id || !r.name || seen.has(String(r.id))) throw new Error('รหัสศูนย์พักพิงขาด/ซ้ำ ไม่เขียนข้อมูล');
    seen.add(String(r.id));
    const number = v => {
      if (v == null || v === '') return '';
      if (typeof v === 'boolean' || !Number.isFinite(Number(v)) || Number(v)<0) throw new Error('ตัวเลขความจุ/ผู้เข้าพักไม่ถูกต้อง: '+r.id);
      return Number(v);
    };
    const text = v => v == null ? '' : typeof v==='object' ? JSON.stringify(v) : String(v);
    return [r.id,r.district,r.name,r.category,number(r.capacity),number(r.occupied),number(r.available),
      r.unitType,r.status,r.link,text(r.additionalDetails),text(r.routeDetails),
      text(r.createdAt),text(r.updatedAt),text(payload.generatedAt),
      typeof payload.stale === 'boolean' ? payload.stale : '',
      shelterThaiTime_(fetchedAt),SHELTER_CONFIG.URL,JSON.stringify(r)
    ].map(v=>v == null ? '' : typeof v==='string' && /^[=+@-]/.test(v) ? "'"+v : v);
  });
}

function shelterThaiTime_(date) {
  return Utilities.formatDate(date,'Asia/Bangkok',"yyyy-MM-dd'T'HH:mm:ss")+'+07:00';
}

// ไม่ใช้ /@lat,lng เพราะเป็นจุดศูนย์กลางมุมมอง ซึ่งอาจไม่ใช่หมุดสถานที่
function shelterParseCoordinates_(value) {
  let text = String(value || '').replace(/&amp;/g,'&');
  try { text = decodeURIComponent(text); } catch (_) {}
  let m = /!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)/.exec(text);
  if (!m) m = /[?&](?:q|query)=\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)(?:[&#\s]|$)/.exec(text);
  if (!m) return null;
  const lat=Number(m[1]), lng=Number(m[2]);
  return Math.abs(lat)<=90 && Math.abs(lng)<=180 ? [lat,lng] : null;
}

function shelterMapUrlAllowed_(url) {
  return /^https:\/\/(?:maps\.app\.goo\.gl|goo\.gl|(?:www\.|maps\.)?google\.(?:com|co\.th))\//i.test(url);
}

function shelterResolveMap_(link) {
  let url=String(link || '').trim();
  for (let hop=0;hop<5;hop++) {
    if (!shelterMapUrlAllowed_(url)) return {status:'ลิงก์ไม่ใช่ Google Maps ที่รองรับ',url};
    const found=shelterParseCoordinates_(url);
    if (found) return {coords:found,status:'พบพิกัดจากลิงก์',url};
    const response=UrlFetchApp.fetch(url,{muteHttpExceptions:true,followRedirects:false});
    const code=response.getResponseCode();
    if (code>=300 && code<400) {
      const headers=response.getAllHeaders();
      const key=Object.keys(headers).find(k=>k.toLowerCase()==='location');
      let next=key ? String(headers[key]) : '';
      if (next.startsWith('/')) next=url.match(/^https:\/\/[^/]+/)[0]+next;
      if (!next) return {status:'ไม่พบลิงก์ปลายทาง',url};
      url=next; continue;
    }
    if (code!==200) return {status:'Google Maps HTTP '+code,url};
    // ใช้เฉพาะ canonical URL ไม่ค้นตัวเลขคู่ใด ๆ ในหน้าเว็บ
    const html=response.getContentText();
    const canonical=/<link\b[^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["']/i.exec(html);
    const coords=canonical && shelterParseCoordinates_(canonical[1]);
    return coords ? {coords,status:'พบพิกัดจาก canonical URL',url:canonical[1]} : {status:'ไม่พบพิกัดหมุดในลิงก์',url};
  }
  return {status:'เปลี่ยนเส้นทางเกิน 5 ครั้ง',url};
}

function shelterAddCoordinates_(rows, previous, fetchedAt) {
  const saved=new Map(previous.map(r=>[String(r[0]),r]));
  // Script Properties คงอยู่ข้ามการรัน แม้ศูนย์หายจากฟีดแล้วกลับมาใหม่
  const store=PropertiesService.getScriptProperties();
  let requests=0;
  const deadline=Date.now()+120000;
  rows.forEach(row=>{
    const id = String(row[0]);
    const link=String(row[9] || '').trim(), old=saved.get(id);
    if (typeof SHELTER_MANUAL_COORDS !== 'undefined' && SHELTER_MANUAL_COORDS[id]) {
      const mc = SHELTER_MANUAL_COORDS[id];
      row.push(mc[0], mc[1], 'มีข้อมูลพิกัด (ค้นหาจากชื่อ)', link, shelterThaiTime_(fetchedAt));
      return;
    }
    const key=shelterCoordinateKey_(id,link);
    const cached=store.getProperty(key);
    if (cached) {
      try {
        const entry=JSON.parse(cached);
        if (Array.isArray(entry) && entry.length===5 && entry[4]) {
          row.push(...entry); return;
        }
      } catch (_) { /* อ่านใหม่เมื่อข้อมูล cache ไม่สมบูรณ์ */ }
    }
    let result=null;
    if (old && old.length>=24 && String(old[9] || '').trim()===link) {
      const valid=typeof old[19]==='number' && typeof old[20]==='number' && Math.abs(old[19])<=90 && Math.abs(old[20])<=180;
      const checked=Date.parse(old[23]);
      // ย้ายผลเดิมทั้งที่พบ/ไม่พบเข้าสู่ความจำถาวร ไม่เรียก Maps ซ้ำ
      if (valid || Number.isFinite(checked)) {
        const entry=old.slice(19,24);
        if (!entry[4]) entry[4]=shelterThaiTime_(fetchedAt);
        store.setProperty(key,JSON.stringify(entry));
        row.push(...entry); return;
      }
    }
    if (!link) result={status:'ไม่มีลิงก์ Google Maps',url:''};
    else if (!shelterMapUrlAllowed_(link)) result={status:'ลิงก์ไม่ใช่ Google Maps ที่รองรับ',url:link};
    else {
      const direct=shelterParseCoordinates_(link);
      if (direct) result={coords:direct,status:'พบพิกัดจากลิงก์',url:link};
      else if (requests<30 && Date.now()<deadline) {
        requests++;
        try { result=shelterResolveMap_(link); }
        catch(e) { result={status:'อ่านลิงก์ไม่สำเร็จ',url:link}; }
      }
    }
    if (!result) { row.push('','','รออ่านพิกัดรอบถัดไป','',''); return; }
    const entry=[result.coords ? result.coords[0] : '',result.coords ? result.coords[1] : '',result.status,
      result.url,shelterThaiTime_(fetchedAt)];
    store.setProperty(key,JSON.stringify(entry));
    row.push(...entry);
  });
}

function shelterCoordinateKey_(id,link) {
  const digest=Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,
    JSON.stringify([String(id),String(link)]),Utilities.Charset.UTF_8);
  return 'SHELTER_GEO_V1_'+digest.map(b=>('0'+(b & 255).toString(16)).slice(-2)).join('');
}

// ค้นเฉพาะรายการที่ไม่มี Google Maps ต้นทาง ไม่แก้ไข map_url เดิม
function shelterFindMissingMaps_(rows, fetchedAt) {
  const store=PropertiesService.getScriptProperties();
  const deadline=Date.now()+60000;
  let count=0;
  rows.forEach(row=>{
    if (shelterMapUrlAllowed_(String(row[9] || '').trim()) || (row[19] !== '' && row[20] !== '')) {
      row.push('','มีลิงก์ต้นทาง หรือมีพิกัดแล้ว','','','',''); return;
    }
    const query=String(row[2])+' เขต'+String(row[1]).replace(/^เขต/,'')+' กรุงเทพมหานคร ประเทศไทย';
    const queryUrl='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(query);
    const key='SHELTER_SEARCH_V1_'+shelterCoordinateKey_(row[0],JSON.stringify([row[2],row[1]])).replace('SHELTER_GEO_V1_','');
    let result=null;
    try { result=JSON.parse(store.getProperty(key) || 'null'); } catch (_) {}
    if (!result && count<20 && Date.now()<deadline) {
      count++;
      try {
        const response=Maps.newGeocoder().setLanguage('th').setRegion('th').geocode(query);
        result=shelterSelectPlace_(response,row[2],row[1],queryUrl);
      } catch (error) {
        result={status:'ค้นหาไม่สำเร็จ: '+String(error.message).slice(0,160)};
      }
      result.checked=shelterThaiTime_(fetchedAt);
      store.setProperty(key,JSON.stringify(result));
    }
    if (!result) { row.push('','รอค้นรอบถัดไป',queryUrl,'','',''); return; }
    if (result.coords) {
      row[19]=result.coords[0];row[20]=result.coords[1];
      row[21]='ค้นด้วย Geocoder: ชื่อและเขตตรงกัน';
      row[22]=result.url;row[23]=result.checked;
    } else {
      // ไม่ใช้พิกัดจากชื่อเดิม ถ้าต้นทางเปลี่ยนชื่อ/เขตแล้วหาผลใหม่ไม่ตรง
      row[19]='';row[20]='';row[21]=result.status;row[22]='';row[23]=result.checked;
    }
    row.push(result.url || '',result.status,queryUrl,result.address || '',result.placeId || '',result.checked);
  });
}

function shelterSelectPlace_(response, name, district, queryUrl) {
  if (!response || !['OK','ZERO_RESULTS'].includes(response.status))
    return {status:'ค้นหาไม่สำเร็จ: '+String(response && response.status || 'invalid response')};
  const results=Array.isArray(response.results) ? response.results : [];
  const normalize=v=>String(v || '').replace(/[\s\u200b]/g,'').toLowerCase();
  const targetName=normalize(name), targetDistrict=normalize(String(district || '').replace(/^เขต/,''));
  const matches=results.filter(r=>{
    const parts=r.address_components || [], loc=r.geometry && r.geometry.location;
    const country=parts.some(p=>(p.types || []).includes('country') && p.short_name==='TH');
    const area=parts.some(p=>(p.types || []).includes('administrative_area_level_1') && /กรุงเทพ|Bangkok/i.test(p.long_name));
    const districtMatches=parts.some(p=>(p.types || []).some(t=>['sublocality_level_1','administrative_area_level_2'].includes(t)) &&
      normalize(String(p.long_name || '').replace(/^เขต/,''))===targetDistrict);
    // ไม่รับแค่ถนน/แขวง/เขต หรือผลประมาณที่อยู่ซึ่งไม่ได้ระบุชื่อสถานที่
    const named=parts.some(p=>(p.types || []).some(t=>['premise','establishment','point_of_interest'].includes(t)) && normalize(p.long_name)===targetName);
    const precise=r.geometry && ['ROOFTOP','GEOMETRIC_CENTER'].includes(r.geometry.location_type);
    return targetName && targetDistrict && !r.partial_match && country && area && districtMatches && named && precise &&
      r.place_id && loc && typeof loc.lat==='number' && typeof loc.lng==='number' && Math.abs(loc.lat)<=90 && Math.abs(loc.lng)<=180;
  });
  const unique=Array.from(new Map(matches.map(r=>[r.place_id,r])).values());
  if (unique.length!==1) return {status:results.length ? 'รอตรวจสอบ: ชื่อ/เขตไม่ชัดเจน หรือมีหลายแห่ง' : 'ไม่พบสถานที่'};
  const r=unique[0];
  return {status:'ชื่อและเขตตรงกันตาม Google Geocoder',
    url:queryUrl+'&query_place_id='+encodeURIComponent(r.place_id),
    coords:[r.geometry.location.lat,r.geometry.location.lng],address:r.formatted_address || '',placeId:r.place_id};
}
function installShelterTrigger() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('มีงานกำลังทำงาน กรุณารัน installShelterTrigger อีกครั้ง');
  try {
    SpreadsheetApp.openById(SHELTER_CONFIG.SPREADSHEET_ID);
    const previous = ScriptApp.getProjectTriggers().filter(t=>t.getHandlerFunction()==='updateShelter');
    // อัปเดตทุก 1 ชั่วโมง และสร้างสำเร็จก่อนลบ Trigger เดิม
    ScriptApp.newTrigger('updateShelter').timeBased().everyHours(1).create();
    previous.forEach(t=>ScriptApp.deleteTrigger(t));
    console.log('สร้าง Trigger updateShelter ทุก 1 ชั่วโมงแล้ว');
  } finally { lock.releaseLock(); }
}
function removeShelterTrigger() {
  ScriptApp.getProjectTriggers().forEach(t=>{
    if (t.getHandlerFunction()==='updateShelter') ScriptApp.deleteTrigger(t);
  });
}

// Compare the record update time, never the API cache generation time.
function shelterAgeMinutes_(value, fetchedAt) {
  if (!value) return '';
  let text = String(value).trim().replace(' ', 'T');
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(text)) return '';
  if (!/(Z|[+-]\d{2}:?\d{2})$/i.test(text)) text += '+07:00';
  const stamp = new Date(text).getTime();
  return Number.isFinite(stamp) ? (fetchedAt.getTime() - stamp) / 60000 : '';
}
