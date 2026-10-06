import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const src = 'C:/Users/admin/OneDrive/กลุ่มพยากรณ์สุขภาพ/2569_น้ำท่วม/SAT/ปภ/รายงานสถานการณ์สาธารณภัยรายจังหวัด.xlsx';
const outDir = 'outputs/flood_analysis';
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(src));
const old = wb.worksheets.getItemOrNullObject('Dashboard_Mockup');
if (!old.isNullObject) old.delete();
const s = wb.worksheets.add('Dashboard_Mockup');
const rows = [
 ['กรมอนามัย | Dashboard เฝ้าระวังน้ำ (Mockup)'],
 ['รอบข้อมูล', '1 ต.ค. 2569', 'แหล่งข้อมูลหลัก', 'ปภ. / ThaiWater / ศูนย์พักพิง'],
 ['วัตถุประสงค์', 'มองสถานการณ์น้ำ ผลกระทบต่อประชาชนกลุ่มเปราะบาง และความพร้อมรองรับในมุมสาธารณสุข'],
 [],
 ['ภาพรวมสถานการณ์'],
 ['จังหวัดที่มีรายงานภัย', '=COUNTA(Disaster_DB!D2:D1000)', 'ครัวเรือนที่ได้รับผลกระทบ', '=SUM(Disaster_DB!J2:J1000)', 'ผู้เสียชีวิต', '=SUM(Disaster_DB!K2:K1000)'],
 ['อำเภอที่ได้รับผลกระทบ', '=SUM(Disaster_DB!F2:F1000)', 'แนวโน้มน้ำเพิ่มขึ้น', '=COUNTIF(Disaster_DB!L2:L1000,"เพิ่มขึ้น")', 'รายการภัยที่กำลังประสบภัย', '=COUNTIF(Disaster_DB!M2:M1000,"กำลังประสบภัย")'],
 [],
 ['สัญญาณเฝ้าระวังน้ำจากสถานี ThaiWater'],
 ['ระดับวิกฤติ/ล้นตลิ่ง', '=COUNTIF(thai_water_DB!N2:N1000,"วิกฤติ")+COUNTIF(thai_water_DB!N2:N1000,"ล้นตลิ่ง")', 'ระดับเตือนภัย', '=COUNTIF(thai_water_DB!N2:N1000,"เตือนภัย")', 'ข้อมูลภายใน 24 ชั่วโมง', '=COUNTIFS(thai_water_DB!R2:R1000,">=0",thai_water_DB!R2:R1000,"<=1440",thai_water_DB!R2:R1000,"<>")'],
 ['สถานีทั้งหมด', '=COUNTA(thai_water_DB!A2:A1000)', 'ข้อมูลเกิน 24 ชั่วโมง', '=COUNTIF(thai_water_DB!R2:R1000,">1440")', 'สถานะเซนเซอร์ปกติ', '=COUNTIF(thai_water_DB!O2:O1000,"ปกติ")'],
 [],
 ['ประชากรกลุ่มเปราะบางในพื้นที่เสี่ยง'],
 ['เด็ก 0-4 ปี', '=SUM(Vulnerable_group!C2:C1000)', 'หญิงตั้งครรภ์', '=SUM(Vulnerable_group!D2:D1000)', 'ผู้สูงอายุ 60 ปีขึ้นไป', '=SUM(Vulnerable_group!E2:E1000)'],
 ['รวมกลุ่มเปราะบาง', '=SUM(Vulnerable_group!F2:F1000)', 'ศูนย์พักพิงทั้งหมด', '=COUNTA(shelter_DB!A2:A1000)', 'ผู้พักพิงปัจจุบัน', '=SUM(shelter_DB!F2:F1000)'],
 ['ความจุศูนย์พักพิง', '=SUM(shelter_DB!E2:E1000)', 'ที่ว่างคงเหลือ', '=SUM(shelter_DB!G2:G1000)', 'ศูนย์พักพิงเต็ม/ใกล้เต็ม', '=COUNTIF(shelter_DB!I2:I1000,"เต็ม")+COUNTIF(shelter_DB!I2:I1000,"ใกล้เต็ม")'],
 [],
 ['มุมมองที่ควรทำในเวอร์ชัน Google Sheets + Apps Script'],
 ['1. แผนที่สถานีและจังหวัด', 'แสดงจุดสถานีตามระดับ ปกติ/เฝ้าระวัง/เตือนภัย/วิกฤติ/ล้นตลิ่ง'],
 ['2. รายการต้องติดตาม', 'กรองเฉพาะข้อมูลสดภายใน 24 ชั่วโมง และรายการที่กระทบกลุ่มเปราะบางสูง'],
 ['3. การแจ้งเตือน', 'แจ้งเตือนเมื่อระดับวิกฤติ, น้ำเพิ่มขึ้นต่อเนื่อง, ข้อมูลเก่า หรือศูนย์พักพิงใกล้เต็ม'],
 ['4. Data quality', 'แสดงเวลาที่ดึงข้อมูลล่าสุด และแยกข้อมูลเก่าของ BKK_water_DB ออกจากข้อมูลปัจจุบัน'],
 [],
 ['ข้อค้นพบจาก mockup นี้'],
 ['- Disaster_DB มี 63 รายการภัย 33 จังหวัด โดยมีรายงาน 2 วัน และยอดครัวเรือนรวมจากข้อมูลดิบ 2,218,711 ครัวเรือน'],
 ['- thai_water_DB มี 807 สถานี: วิกฤติ 188, ล้นตลิ่ง 62, เตือนภัย 342, เฝ้าระวัง 152, ปกติ 48 และไม่ทราบ 15'],
 ['- ข้อมูลสถานีกรุงเทพฯ 282 รายการส่วนใหญ่เก่ากว่า 24 ชั่วโมง จึงไม่ควรนำไปรวมเป็นสัญญาณสดโดยไม่ติดป้าย freshness'],
 ['- shelter_DB มีความจุ 15,857 คน ใช้แล้ว 4,449 คน และว่าง 11,611 คน แต่พิกัดมีจำกัด จึงควรแยกตัวชี้วัดพิกัดพร้อมใช้งาน'],
];
s.getRangeByIndexes(0,0,rows.length,6).values = rows.map(r=>r.map(v=>typeof v==='string'&&v.startsWith('=')?null:v));
// Write formulas separately to avoid treating them as values.
for (let r=0;r<rows.length;r++) for (let c=0;c<Math.min(rows[r].length,6);c++) if (typeof rows[r][c]==='string'&&rows[r][c].startsWith('=')) s.getCell(r,c).formulas=[[rows[r][c]]];
s.getRange('A1:F1').merge();
s.getRange('A1:F1').format = { fill:'#0B4F6C', font:{bold:true,color:'#FFFFFF',size:16}, horizontalAlignment:'center', verticalAlignment:'center' };
for (const r of [4,8,12,18,24]) s.getRange(`A${r+1}:F${r+1}`).format={fill:'#D9EAF2',font:{bold:true,color:'#0B4F6C'}};
s.getRange('A6:F17').format={font:{size:11}};
s.getRange('A1:F35').format.wrapText=true;
s.getRange('A1:A35').format.columnWidth=230; s.getRange('B1:B35').format.columnWidth=220; s.getRange('C1:C35').format.columnWidth=180; s.getRange('D1:D35').format.columnWidth=150; s.getRange('E1:E35').format.columnWidth=180; s.getRange('F1:F35').format.columnWidth=150;
s.freezePanes.freezeRows(2);
wb.recalculate();
const check=await wb.inspect({kind:'table',range:'Dashboard_Mockup!A1:F18',include:'values,formulas',tableMaxRows:18,tableMaxCols:6});
console.log(check.ndjson);
await fs.mkdir(outDir,{recursive:true});
const blob=await SpreadsheetFile.exportXlsx(wb); await blob.save(`${outDir}/flood_dashboard_mockup.xlsx`);
