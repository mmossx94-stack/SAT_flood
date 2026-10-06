# 🚀 คู่มือการตั้งค่า Apache Airflow + Google Sheets + Google Apps Script Web App

ระบบตั้งเวลารันอัตโนมัติด้วย **Apache Airflow** เพื่อดึงข้อมูล Google Trends และข้อมูลอุทกภัย ส่งขึ้น **Google Sheets** เพื่อเปิดใช้งานบน **Google Apps Script (GAS) Web App**

---

## 🛠️ ขั้นตอนที่ 1: เตรียม Google Service Account & Google Sheet

1. เข้าไปที่ [Google Cloud Console](https://console.cloud.google.com/)
2. สร้าง Project ใหม่ และเปิดใช้งาน **Google Sheets API** และ **Google Drive API**
3. สร้าง **Service Account** และดาวน์โหลดไฟล์คีย์ **service_account.json**
4. นำไฟล์ service_account.json มาวางที่โฟลเดอร์หลักของโปรเจกต์ (C:\xampp\htdocs\SAT\service_account.json)
5. เปิด Google Sheet ที่คุณต้องการใช้ คัดลอก **Spreadsheet ID** จาก URL:
   https://docs.google.com/spreadsheets/d/**<SPREADSHEET_ID>**/edit
6. กดปุ่ม **Share** ใน Google Sheet แล้วเพิ่มอีเมลของ Service Account (เช่น xxx@xxx.iam.gserviceaccount.com) ให้สิทธิ์เป็น **Editor**

---

## 🐍 ขั้นตอนที่ 2: ติดตั้ง Python Dependencies

ติดตั้งไลบรารีที่จำเป็นสำหรับ Airflow และ Google Sheets:

`ash
pip install gspread google-auth pytrends apache-airflow
`

---

## 🧪 ขั้นตอนที่ 3: ทดสอบการรัน Python ETL (Upload ขึ้น Google Sheet)

สามารถทดสอบรันสคริปต์ดึงข้อมูลและอัปเดตขึ้น Google Sheets โดยตรงด้วยคำสั่ง:

`ash
python scripts/upload_to_gspread.py --spreadsheet-id YOUR_SPREADSHEET_ID --creds-file service_account.json
`

เมื่อสคริปต์ทำงานสำเร็จ ใน Google Sheet จะปรากฏ Tab **Google_Trends_DB** ที่มีข้อมูล JSON ใน Cell A1 และตารางสรุปคำค้นหา

---

## 🌀 ขั้นตอนที่ 4: ตั้งค่า Apache Airflow DAG

1. คัดลอกโฟลเดอร์ DAG ไปยัง Airflow DAGs folder (หรือตั้งค่า AIRFLOW__CORE__DAGS_FOLDER ชี้มาที่ C:\xampp\htdocs\SAT\airflow\dags)
2. กำหนด Environment Variables ให้ Airflow:
   * SPREADSHEET_ID = <YOUR_SPREADSHEET_ID>
   * GOOGLE_APPLICATION_CREDENTIALS = C:\xampp\htdocs\SAT\service_account.json
3. สั่งรัน Airflow Scheduler:
   `ash
   airflow db init
   airflow scheduler
   `
4. DAG ชื่อ **sat_flood_pipeline** จะรันอัตโนมัติทุกๆ 2 ชั่วโมงเพื่ออัปเดตข้อมูลสดสดเข้า Google Sheets

---

## 📜 ขั้นตอนที่ 5: ตั้งค่า Google Apps Script (GAS)

1. เปิด Google Sheet ของคุณขึ้นมา เลือกเมนู **Extensions (ส่วนขยาย) > Apps Script**
2. คัดลอกโค้ดจากไฟล์ Dashboard/Code.gs ไปวางใน Code.gs บน Apps Script Editor
3. คัดลอกไฟล์ Dashboard/index.html ไปสร้างเป็นไฟล์ index.html ใน Apps Script Editor
4. กดปุ่ม **Deploy > New deployment** Select type **Web app**:
   * **Execute as**: Me
   * **Who has access**: Anyone
5. กด **Deploy** ท่านจะได้ URL สำหรับเปิดดู Dashboard บน Google Apps Script ที่ข้อมูลอัปเดตสดจาก Airflow อัตโนมัติ!