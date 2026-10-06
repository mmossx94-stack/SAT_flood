# ชุดข้อมูลหลังบ้าน ระดับน้ำ กทม. และสีรายเขต

ชุดส่งต่อสำหรับพัฒนาระบบเฝ้าระวัง: ข้อมูล JSON ต้นฉบับครบทุกฟิลด์จาก endpoint ที่ทดสอบได้จริง, CSV, ข้อมูลที่จัดรูปแบบ, สีรายเขตครบ 50 เขต, ทะเบียนสถานีสูบน้ำ และโปรแกรมดึงซ้ำ Python มาตรฐาน ไม่ต้องติดตั้งแพ็กเกจเพิ่ม

ขอบเขต: ครบทุก record ของ endpoint ระดับน้ำ ณ เวลาที่ดึง ไม่ใช่ข้อมูลทุกระบบของสำนักการระบายน้ำ ไม่ใช่ประวัติย้อนหลัง และยังไม่มีขอบเขตเขต GeoJSON, ปริมาณฝน, น้ำท่วมถนน หรือข้อมูลเดินเครื่องสูบแบบสด ไฟล์แต่ละ snapshot เก็บแยกกัน ไม่แก้ไฟล์งานเดิม

## แหล่งข้อมูลและสัญญาการเรียก

ระดับน้ำ:
POST https://weather.bangkok.go.th/water/PageMap/GoogleMap
Content-Type: application/x-www-form-urlencoded
Body: payload=TEST_DATA_GOES_HERE
Response: JSON array; ไม่มี pagination ที่พบ ทุกจุดมาในคำตอบเดียว
Authentication: ทดสอบได้โดยไม่ส่ง API key หรือบัญชี
สถานะ: เป็น endpoint ภายในที่เว็บใช้งาน ไม่พบเอกสาร API/SLA หรือเงื่อนไขการใช้ที่ยืนยันความถี่/ความต่อเนื่อง การอัปเดตต้องตรวจรูปแบบผลลัพธ์ทุกครั้ง

ทะเบียนสถานีสูบน้ำ:
GET https://data.bangkok.go.th/api/3/action/datastore_search?resource_id=0a30a58c-213f-4aec-bf16-7dd7f61fb5fd&limit=1000
Response: success, result.total, result.records
หาก result.total มากกว่าจำนวนแถว ต้องดึงหน้าถัดไปด้วย offset
หน้า catalog: https://data.bangkok.go.th/dataset/pumping-station
เป็นทะเบียน/ตำแหน่ง/เกณฑ์ ไม่ใช่สถานะเครื่องสูบปัจจุบัน และรหัส id ไม่ใช่ water_id หรือ water_code ห้าม join ด้วยเลข id โดยตรง

## ไฟล์ในแต่ละ snapshot

- stations_raw.json / .csv: ทุกสถานีและทุกฟิลด์จากระดับน้ำ JSON เป็นฉบับอ้างอิงสำหรับชนิดข้อมูลและ null
- raw_field_inventory.json: ฟิลด์ทั้งหมดพร้อมชนิดข้อมูลที่พบจริง ใช้ตรวจ schema drift
- stations_normalized.json / .csv: เวลาที่ตีความ อายุข้อมูล เหตุผลคัดออก และรหัสเขตสำหรับการนำไปใช้
- district_status.json / .csv: สีรายเขต 50 เขต พร้อมจำนวนสถานีที่ใช้ได้/คัดออกและสถานีที่ทำให้เกิดสี
- district_crosswalk.json: ชื่อเขต รหัสเขต 4 หลักและ district_id ภายในที่พบใน API
- pump_registry_response.json: คำตอบทะเบียนต้นฉบับ พร้อม total และ schema
- pump_registry_records.json: แถวทะเบียนสถานีสูบน้ำ
- metadata.json: แหล่งข้อมูล เวลา fetch สรุปจำนวน กติกาสี และข้อผิดพลาดแหล่งเสริม
- water_summary_source.html / waterSummaryList_raw.json / districtList_raw.json: สร้างได้เฉพาะเมื่อหน้า summary เข้าถึงและอ่านได้ ครั้งแรกหน้า /water/summary ตอบ 404 จึงไม่มีไฟล์เหล่านี้

## ฟิลด์หลักของระดับน้ำ

water_id: รหัสจุดภายในระบบ
water_code: รหัสสถานี เช่น WL.SSM.01; เก็บควบคู่ water_id ไม่รวมกับทะเบียนเครื่องสูบ
water_name / water_name_en: ชื่อจุด
water_system_id: ระบบต้นทางย่อย; เก็บไว้ตรวจความแตกต่างของการวัด
water_url: ลิงก์สถานีต้นทาง ถ้ามี
district_id / district_name: รหัสภายในและชื่อพื้นที่ มีพื้นที่นอก กทม. ด้วย
latitude / longitude: พิกัดจุดตรวจวัด
river_id / river_name: รหัสและชื่อคลอง/แม่น้ำ
site_timestamp / site_timestampTH / site_timestampEN: เวลาแหล่งข้อมูล
wl_in / wl_out01 / wl_out02: ระดับน้ำด้านใน/ด้านนอก มี null และบางระบบอาจมี sentinel; ตรวจหน่วยจากสถานีต้นทางก่อนรวมเชิงปริมาณ
left_bank / right_bank: ระดับตลิ่งตามข้อมูลต้นทาง ไม่ใช่ความลึกน้ำท่วมถนน
warning / critical: เกณฑ์ต้นทาง; ไม่ใช่เกณฑ์เดียวทั้งเมือง
warning_out01 / critical_out01 / warning_out02 / critical_out02: เกณฑ์ด้านนอก
max_in_day / max_in_yesterday / max_out01_day / max_out01_yesterday / max_out02_day / max_out02_yesterday: สูงสุดรายวันถ้ามี
colorStatus / txtStatus: สีและสถานะที่หน้าเว็บใช้ ใช้ txtStatus สรุป alert และแยกสถานะขัดข้อง
adjust / status / priorityStatus / statusColor: รหัสภายใน ยังไม่ยืนยันความหมายทั้งหมด ห้ามตีความเป็นระดับเตือนเอง
water_gate_count / watergate01 ถึง watergate06: เก็บต้นฉบับ ยังไม่ยืนยันว่าเป็นกำลังสูบหรือประตู จึงไม่ใช้คำนวณ
ฟิลด์อื่นทุกฟิลด์เก็บใน stations_raw.json และ raw_field_inventory.json

## เวลาและความสด

พบ site_timestamp ที่ลงท้าย Z แต่เวลาไม่ตรงกับ site_timestampTH จึงไม่ใช้ Z เป็น UTC โดยไม่ตรวจสอบ
โค้ดนี้เลือก site_timestampTH เช่น 03/10/2569 14:55 -> 2026-10-03T14:55:00+07:00 และเก็บทั้งค่าดิบและค่าที่ตีความไว้
เป็นสมมติฐานที่ตรงกับเวลาที่หน้าเว็บแสดง ต้องยืนยันกับเจ้าของข้อมูลก่อนใช้งานเตือนภัยจริง
fetched_at_utc คือเวลาที่ดึงเสร็จ ไม่ใช่เวลาวัด
ค่าเริ่มต้นความสด 15 นาทีเป็นนโยบายระบบนี้ ไม่ใช่เกณฑ์ทางการ เปลี่ยนได้ด้วย --stale-minutes
เวลาขาดหาย เวลาต้นทางอยู่ในอนาคต หรือเก่ากว่าเกณฑ์ ถูกคัดออก ไม่ปรับเวลาเงียบ ๆ
null/ค่าว่าง/-99 ห้ามตีความเป็นศูนย์; ข้อมูลดิบคงค่าเดิม โปรแกรมนี้ใช้สถานะต้นทางในการจัดสี ไม่คำนวณระดับน้ำใหม่

## กติกาสีรายเขต

ใช้สถานีที่ txtStatus = ปกติ/เตือนภัย/วิกฤต/วิกฤติ และเวลาอยู่ในช่วง 0 ถึง stale-minutes เท่านั้น
จัดสีจากสถานะสูงสุดของจุดที่ใช้ได้: critical #e85965 > warning #f4b05b > normal #24b295
ไม่มีจุดหรือไม่มีจุดที่ใช้ได้: unknown #676b6b
บางจุดคัดออก: partial_data=true และ coverage=partial แม้สีที่เหลือจะเป็นเขียว ต้องแสดงข้อจำกัดนี้
coverage=no_station ต่างจาก no_usable_data; ทั้งสองกรณีไม่ใช่ปกติ
trigger_station_codes: จุดที่มีสถานะเท่าระดับสูงสุด ใช้ tooltip/ตรวจสอบที่มาของสี
ข้อมูลนอก กทม. เก็บไว้ครบใน raw/normalized แต่ไม่นำมาจัดสี 50 เขต
สีเป็นการสรุปของระบบเรา ไม่ใช่ประกาศเตือนภัยรายเขตของ กทม. และไม่สรุปว่าทั้งเขตน้ำท่วม
ชื่อชั้นข้อมูล: สถานะระดับน้ำจากสถานีตรวจวัดรายเขต
คำอธิบาย: สีแสดงสถานะสูงสุดของจุดตรวจวัดที่ข้อมูลยังใช้ได้ในเขต

## การจับคู่แผนที่

district_id ของ DDS ไม่ใช่รหัสเขตทางปกครอง เช่น หนองจอก=3 ขณะที่ district_code=1003
district_code เป็นตารางรหัส 4 หลักที่ใส่ไว้ในโค้ด ต้องตรวจเทียบกับ schema/ชื่อเขตของ GeoJSON ที่เลือกก่อน join; ไม่มี geometry รวมมา
ใช้ district_name ตรวจชื่อและพิกัดเพื่อจับคู่รอบแรก อย่าสรุปว่าใช้ district_id+1000 ได้ทุกเขต
พิกัดเป็นสถานี ไม่ใช่ขอบเขตพื้นที่ผลกระทบ; เขตที่ไม่มีสถานีเป็นสีเทา

## วิธีดึงซ้ำ

python refresh.py
python refresh.py --stale-minutes 15

โปรแกรมสร้าง snapshot_YYYYMMDDTHHMMSS_microsecondsZ ใหม่ในโฟลเดอร์เดียวกับสคริปต์
ไม่มีการตั้ง scheduler หรือเรียกซ้ำอัตโนมัติไว้ให้
เริ่มตั้งรอบทุก 5-10 นาทีเป็นข้อเสนอการออกแบบ ไม่ใช่ความถี่ที่หน่วยงานรับรอง ใช้ server กลางและ cache อย่าให้ทุก browser ยิงตรง
ควรมี timeout, retry แบบ backoff จำนวนจำกัด, เก็บประวัติ, ตรวจ duplicate station ID และแจ้ง source error/schema drift
API ล้มเหลวต้องแสดง last successful fetch + source_error; ห้ามแสดงข้อมูลเก่าเป็น current หรือเปลี่ยนเป็นเขียว
ไม่ต้องยิง SQL หรือเขียนฐานข้อมูลเพื่อทดลอง; schema.sql เป็นข้อเสนอสำหรับ PostgreSQL

## แบบจำลองฐานข้อมูล

เก็บ raw snapshot พร้อม endpoint/fetched_at เพื่อ audit
แยก observations ต่อสถานีและเวลา, district_status ต่อเขตและเวลา, registry แยกต่างหาก
unique observation ใช้ source + water_id + interpreted observed_at; ห้ามใช้เวลา fetch เป็นเวลาวัด
เก็บหลักฐาน trigger stations, freshness policy และ aggregation version ให้ย้อนดูได้ว่าทำไมเขตเป็นสีใด
API ของระบบคุณอาจให้ GET /api/water/stations และ GET /api/water/districts พร้อม fetched_at, observed_at, source_error, partial_data
ตัวอย่าง schema ใน schema.sql ยังไม่ได้รันหรือ deploy

## ผลดึงครั้งแรก 3 ต.ค. 2569 เวลา 15:04 น.

311 จุดไม่ซ้ำ, 19 จุดนอก กทม., สถานะต้นทางปกติ 195 เตือนภัย 19 วิกฤต 40 ขัดข้อง 57
252 จุดผ่านเกณฑ์ความสด/สถานะ, 2 จุดเวลาอยู่ในอนาคตจึงคัดออก
50 เขต: เขียว 27 ส้ม 6 แดง 14 เทา 3 ตามนโยบายที่ระบุ ไม่ใช่ประกาศของหน่วยงาน
ทะเบียนสถานีสูบน้ำ 201 รายการ
ตัวเลขเป็น snapshot เท่านั้น ไม่ใช่สถานการณ์ปัจจุบันหลังจากเวลา fetch