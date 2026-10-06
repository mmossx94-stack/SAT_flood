import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const dir='outputs/flood_analysis';
const source='C:/Users/admin/OneDrive/กลุ่มพยากรณ์สุขภาพ/2569_น้ำท่วม/SAT/ปภ/รายงานสถานการณ์สาธารณภัยรายจังหวัด.xlsx';
const d=JSON.parse(await fs.readFile(`${dir}/source_data.json`,'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
const national=wb.worksheets.getItem('Dashboard');
try {const before=await wb.render({sheetName:'Dashboard',range:'A1:J13',scale:1}); await fs.writeFile(`${dir}/before.png`,new Uint8Array(await before.arrayBuffer()));}catch(e){console.log('Before render',e.message)}
const bkk=wb.worksheets.add('Dashboard_BKK');
const prov=wb.worksheets.add('Province_Summary');
const district=wb.worksheets.add('BKK_Districts');
const guide=wb.worksheets.add('Definitions_Plan');
national.getUsedRange().clear({applyTo:'all'}); national.deleteAllDrawings();
const C={navy:'#153E50',teal:'#087F8C',pale:'#EAF4F5',gray:'#64748B',amber:'#FFF1CD',red:'#FDE7E7'};
function value(s,a,v){s.getRange(a).values=[[v]];}
function formula(s,a,v){s.getRange(a).formulas=[[v]];}
function span(s,a,v){s.getRange(a).merge();value(s,a.split(':')[0],v);}
function base(s,end='L75'){s.showGridLines=false;s.getRange(`A1:${end}`).format={font:{name:'Tahoma',size:11,color:'#233746'},rowHeight:25,verticalAlignment:'center'};s.getRange('A:L').format.columnWidthPx=102;s.tabColor=C.teal;}
function title(s,t,sub){span(s,'A2:L2',t);s.getRange('A2:L2').format.font={name:'Tahoma',size:17,bold:true,color:C.navy};span(s,'A3:L3',sub);s.getRange('A3:L3').format.font.color=C.gray;}
function band(s,r,t){span(s,`A${r}:L${r}`,t);s.getRange(`A${r}:L${r}`).format={fill:C.pale,font:{bold:true,color:C.navy}};}
function note(s,r,t){span(s,`A${r}:L${r}`,t);s.getRange(`A${r}:L${r}`).format={wrapText:true,rowHeight:38,font:{name:'Tahoma',size:10,color:C.gray}};}
function card(s,col,row,label,f){const cols=['A','D','G','J'];const ends=['C','F','I','L'];const a=cols[col],b=ends[col];span(s,`${a}${row}:${b}${row}`,label);span(s,`${a}${row+1}:${b}${row+2}`,'');formula(s,`${a}${row+1}`,f);s.getRange(`${a}${row+1}:${b}${row+2}`).format={fill:C.pale,font:{name:'Tahoma',size:17,bold:true,color:C.navy},numberFormat:'#,##0'};}
function table(s,row,headers,rows){s.getRangeByIndexes(row-1,0,1,headers.length).values=[headers];if(rows.length)s.getRangeByIndexes(row,0,rows.length,headers.length).values=rows;s.getRangeByIndexes(row-1,0,1,headers.length).format={fill:C.navy,font:{name:'Tahoma',color:'#FFFFFF',bold:true},wrapText:true,rowHeight:44};s.freezePanes.freezeRows(row);}
const dr=wb.worksheets.getItem('Disaster_DB'), vg=wb.worksheets.getItem('Vulnerable_group'),bw=wb.worksheets.getItem('BKK_water_DB'),tw=wb.worksheets.getItem('thai_water_DB'),sh=wb.worksheets.getItem('shelter_DB');
// Retain original fields; append explicit, auditable normalization fields.
value(dr,'Q1','Report_Day');for(let i=0;i<d.Disaster_DB.length;i++)formula(dr,`Q${i+2}`,`=INT(B${i+2})`);dr.getRange('Q2:Q64').setNumberFormat('yyyy-mm-dd');
value(bw,'X1','Province_from_raw');bw.getRange('X2:X283').values=d.BKK_water_DB.map(r=>[JSON.parse(r.raw_station_json).geocode.province_name.th]);
value(bw,'Y1','Time_quality');value(tw,'X1','Time_quality');
for(const [s,n,col] of [[bw,282,'Y'],[tw,807,'X']])for(let i=2;i<=n+1;i++)formula(s,`${col}${i}`,`=IF(ISNUMBER(R${i}),IF(R${i}<0,"เวลาอนาคต",IF(R${i}<=1440,"ภายใน 24 ชั่วโมง","เกิน 24 ชั่วโมง")),"ไม่มีเวลา")`);
value(sh,'Y1','Capacity_check');value(sh,'Z1','Has_coordinates');for(let i=2;i<=208;i++){formula(sh,`Y${i}`,`=IF(F${i}>E${i},"เกินความจุ",IF(E${i}-F${i}<>G${i},"ยอดไม่ตรง","ยอดตรง"))`);formula(sh,`Z${i}`,`=IF(AND(ISNUMBER(T${i}),ISNUMBER(U${i})),1,0)`);}
// Preserve raw timestamps; normalize supported ISO timestamps to Thai serial time.
function thaiSerial(v){if(!v)return null;let t=String(v).trim().replace(' ','T');if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(t))return null;if(!/(Z|[+-]\d{2}:?\d{2})$/i.test(t))t+='+07:00';const n=Date.parse(t);return Number.isFinite(n)?(n+7*3600000)/86400000+25569:null;}
value(sh,'AA1','Updated_at_Thai');value(sh,'AB1','Fetched_at_Thai');value(sh,'AC1','Age_minutes');value(sh,'AD1','Time_quality_24h');
for(let i=0;i<d.shelter_DB.length;i++){const row=i+2,r=d.shelter_DB[i];value(sh,`AA${row}`,thaiSerial(r.updated_at_source));value(sh,`AB${row}`,thaiSerial(r.fetched_at_th));formula(sh,`AC${row}`,`=IF(AND(ISNUMBER(AA${row}),ISNUMBER(AB${row})),(AB${row}-AA${row})*1440,"")`);formula(sh,`AD${row}`,`=IF(ISNUMBER(AC${row}),IF(AC${row}<0,"เวลาอนาคต",IF(AC${row}<=1440,"ภายใน 24 ชั่วโมง","เกิน 24 ชั่วโมง")),"ไม่ทราบเวลาข้อมูล")`);}
sh.getRange('AA2:AB208').setNumberFormat('yyyy-mm-dd hh:mm');sh.getRange('AC2:AC208').setNumberFormat('0.0');sh.getRange('AD:AD').format.columnWidthPx=190;
value(dr,'R1','Time_quality_24h');for(let i=0;i<d.Disaster_DB.length;i++)value(dr,`R${i+2}`,'ไม่ทราบเวลาข้อมูล');
value(vg,'G1','Time_quality_24h');for(let i=0;i<d.Vulnerable_group.length;i++)value(vg,`G${i+2}`,'ไม่ทราบเวลาข้อมูล');
base(national);title(national,'กรมอนามัย | เฝ้าระวังน้ำและผลกระทบ','MOCKUP จากไฟล์ Excel • ภาพรวมประเทศรวม กทม. • เปิด Dashboard_BKK เพื่อดูรายละเอียด กทม.');
value(national,'A5','วันรายงาน');value(national,'C5',463?new Date('2026-10-01T00:00:00Z'):null);national.getRange('C5').setNumberFormat('dd/mm/yyyy');national.getRange('C5').format.fill=C.amber;
national.getRange('C5').dataValidation={rule:{type:'list',formula1:'Definitions_Plan!$A$29:$A$30'}};
span(national,'E5:L5','เปลี่ยนวันที่ช่องสีเหลือง | วันรายงานภัยมี 30 ก.ย. และ 1 ต.ค. 2569');
base(prov,'L80');const ps=d.Vulnerable_group.filter(r=>r['จังหวัด']);const pe=ps.length+1;
table(prov,1,['จังหวัด','เขตสุขภาพ','รายงานวันที่เลือก','ครัวเรือนตามรายงาน','แนวโน้มเพิ่มขึ้น','เด็ก 0–4 ปีทั้งจังหวัด','หญิงตั้งครรภ์ทั้งจังหวัด','ผู้สูงอายุทั้งจังหวัด','รวมฐานประชากร','แถวรายงานซ้ำ','สถานะข้อมูล'],ps.map(r=>[r['จังหวัด'],r['เขตสุขภาพ'],null,null,null,null,null,null,null,null,null]));
prov.getRange('A:B').format.columnWidthPx=165;prov.getRange('C:K').format.columnWidthPx=140;
for(let i=2;i<=pe;i++){
 formula(prov,`C${i}`,`=COUNTIFS(Disaster_DB!$D$2:$D$64,A${i},Disaster_DB!$Q$2:$Q$64,Dashboard!$C$5,Disaster_DB!$M$2:$M$64,"กำลังประสบภัย")`);
 formula(prov,`D${i}`,`=IF(C${i}=0,"ไม่มีรายงาน",IF(C${i}>1,"ตรวจรายงานซ้ำ",SUMIFS(Disaster_DB!$J$2:$J$64,Disaster_DB!$D$2:$D$64,A${i},Disaster_DB!$Q$2:$Q$64,Dashboard!$C$5)))`);
 formula(prov,`E${i}`,`=COUNTIFS(Disaster_DB!$D$2:$D$64,A${i},Disaster_DB!$Q$2:$Q$64,Dashboard!$C$5,Disaster_DB!$L$2:$L$64,"เพิ่มขึ้น")`);
 for(const [dst,src] of [['F','C'],['G','D'],['H','E']])formula(prov,`${dst}${i}`,`=SUMIFS(Vulnerable_group!$${src}$2:$${src}$78,Vulnerable_group!$B$2:$B$78,A${i})`);
 formula(prov,`I${i}`,`=SUM(F${i}:H${i})`);formula(prov,`J${i}`,`=IF(C${i}>1,1,0)`);formula(prov,`K${i}`,`=IF(C${i}=0,"ไม่มีรายงานวันที่เลือก",IF(C${i}>1,"ตรวจรายงานซ้ำ","มีรายงานภัย"))`);
}prov.getRange(`C2:J${pe}`).setNumberFormat('#,##0');prov.tables.add(`A1:K${pe}`,true,'ProvinceSummary');
card(national,0,7,'จังหวัดมีรายงานภัย (จังหวัด)',`=COUNTIFS(Province_Summary!C2:C${pe},">0")`);
card(national,1,7,'ครัวเรือนตามรายงาน (ครัวเรือน)',`=IF(SUM(Province_Summary!J2:J${pe})>0,"ตรวจรายงานซ้ำ",SUM(Province_Summary!D2:D${pe}))`);
card(national,2,7,'จังหวัดน้ำเพิ่มขึ้น (จังหวัด)',`=COUNTIFS(Province_Summary!E2:E${pe},">0")`);
card(national,3,7,'กทม. ตามรายงาน (ครัวเรือน)',`=Dashboard_BKK!A8`);
note(national,11,'ยอดตามวันรายงานที่เลือก ไม่รวมยอดข้ามวัน • จังหวัดที่ไม่มีรายงานในวันนั้นยังสรุปว่าไม่มีภัยไม่ได้');
band(national,13,'สถานีระดับน้ำทั่วประเทศ | ณ เวลานำเข้า 1 ต.ค. 2569 เวลา 15:22 น.');
card(national,0,14,'สถานีในชุดข้อมูล (แห่ง)','=COUNTA(thai_water_DB!A2:A808)');
card(national,1,14,'ข้อมูลอายุ 0–24 ชั่วโมง (แห่ง)','=COUNTIFS(thai_water_DB!X2:X808,"ภายใน 24 ชั่วโมง")');
card(national,2,14,'วิกฤติ/ล้นตลิ่ง อายุ 0–24 ชั่วโมง','=COUNTIFS(thai_water_DB!X2:X808,"ภายใน 24 ชั่วโมง",thai_water_DB!N2:N808,"วิกฤติ")+COUNTIFS(thai_water_DB!X2:X808,"ภายใน 24 ชั่วโมง",thai_water_DB!N2:N808,"ล้นตลิ่ง")');
card(national,3,14,'เวลาตรวจวัดอยู่ในอนาคต','=COUNTIFS(thai_water_DB!X2:X808,"เวลาอนาคต")');
note(national,18,'ความสดคำนวณเทียบเวลานำเข้าในไฟล์ ไม่ใช่เวลาปัจจุบัน • แยกเวลาอนาคตออกจากข้อมูลสด • ระดับเตือนเป็นสถานะจากแหล่งข้อมูล');
band(national,20,'ฐานกลุ่มเปราะบางในจังหวัดที่มีรายงานภัย | จำนวนประชากรทั้งจังหวัด');
card(national,0,21,'เด็ก 0–4 ปี (คน)',`=SUMIFS(Province_Summary!F2:F${pe},Province_Summary!C2:C${pe},">0")`);
card(national,1,21,'หญิงตั้งครรภ์ (คน)',`=SUMIFS(Province_Summary!G2:G${pe},Province_Summary!C2:C${pe},">0")`);
card(national,2,21,'ผู้สูงอายุ 60 ปีขึ้นไป (คน)',`=SUMIFS(Province_Summary!H2:H${pe},Province_Summary!C2:C${pe},">0")`);
card(national,3,21,'จังหวัดมีข้อมูลฐานประชากร',`=COUNTIFS(Province_Summary!C2:C${pe},">0")`);
note(national,25,'ตัวเลขฐานประชากรไม่ใช่จำนวนผู้ได้รับผลกระทบจริง • ยังไม่มีวันอ้างอิงประชากร/ข้อมูลระดับพื้นที่น้ำท่วม • ตัดแถวรวมทั้งหมดออกแล้ว');
band(national,27,'เปรียบเทียบครัวเรือนตามรายงาน | กทม. และพื้นที่อื่น');
table(national,29,['วันที่รายงาน','กทม.','พื้นที่อื่น'],[]);
for(const [i,date] of [[30,'2026-09-30'],[31,'2026-10-01']]){value(national,`A${i}`,new Date(date+'T00:00:00Z'));formula(national,`B${i}`,`=SUMIFS(Disaster_DB!$J$2:$J$64,Disaster_DB!$Q$2:$Q$64,A${i},Disaster_DB!$D$2:$D$64,"กรุงเทพมหานคร")`);formula(national,`C${i}`,`=SUMIFS(Disaster_DB!$J$2:$J$64,Disaster_DB!$Q$2:$Q$64,A${i})-B${i}`);}national.getRange('A30:A31').setNumberFormat('dd/mm/yyyy');national.getRange('B30:C31').setNumberFormat('#,##0');national.freezePanes.unfreeze();
const chart=national.charts.add('bar',national.getRange('A29:C31'));chart.title='ครัวเรือนตามวันรายงาน';chart.setPosition('E29','L43');chart.titleTextStyle.typeface='Tahoma';chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Tahoma',fontSize:11}};chart.yAxis={numberFormatCode:'#,##0',numberFormatSourceLinked:false,textStyle:{typeface:'Tahoma'}};
base(bkk);title(bkk,'กรมอนามัย | เฝ้าระวังน้ำ กรุงเทพมหานคร','MOCKUP • รายงานภัยระดับจังหวัด + สถานีคลองใน กทม. + ศูนย์พักพิงตามเขต');
value(bkk,'A5','วันรายงาน');formula(bkk,'C5','=Dashboard!C5');bkk.getRange('C5').setNumberFormat('dd/mm/yyyy');span(bkk,'E5:L5','วันรายงานเปลี่ยนตาม Dashboard | สถานีและศูนย์พักพิงเป็นภาพ ณ เวลานำเข้า');
card(bkk,0,7,'ครัวเรือนตามรายงาน ปภ.', '=IF(COUNTIFS(Disaster_DB!D2:D64,"กรุงเทพมหานคร",Disaster_DB!Q2:Q64,C5)=1,SUMIFS(Disaster_DB!J2:J64,Disaster_DB!D2:D64,"กรุงเทพมหานคร",Disaster_DB!Q2:Q64,C5),"ตรวจรอบรายงาน")');
card(bkk,1,7,'สถานีคลองใน กทม. (แห่ง)','=COUNTIFS(BKK_water_DB!X2:X283,"กรุงเทพมหานคร")');
card(bkk,2,7,'สถานี กทม. อายุ 0–24 ชั่วโมง','=COUNTIFS(BKK_water_DB!X2:X283,"กรุงเทพมหานคร",BKK_water_DB!Y2:Y283,"ภายใน 24 ชั่วโมง")');
card(bkk,3,7,'สถานี กทม. ข้อมูลเก่า','=COUNTIFS(BKK_water_DB!X2:X283,"กรุงเทพมหานคร",BKK_water_DB!Y2:Y283,"เกิน 24 ชั่วโมง")');
note(bkk,11,'รายงาน ปภ. ยังไม่แจกแจงครัวเรือนรายเขต • สถานีคลอง กทม. ทั้งหมดข้อมูลเก่า ณ นำเข้า 1 ต.ค. 2569 เวลา 15:57 น. จึงยังสรุปสถานการณ์น้ำปัจจุบันไม่ได้');
band(bkk,13,'ศูนย์พักพิง กทม. | ณ นำเข้า 1 ต.ค. 2569 เวลา 16:01 น.');
card(bkk,0,14,'ศูนย์พักพิงในชุดข้อมูล (แห่ง)','=COUNTA(shelter_DB!A2:A208)');
card(bkk,1,14,'ผู้พักพิงตามรายงาน (คน)','=SUM(shelter_DB!F2:F208)');
card(bkk,2,14,'ที่ว่างตามแหล่งข้อมูล (คน)','=SUM(shelter_DB!G2:G208)');
card(bkk,3,14,'ศูนย์มีผู้พักเกินความจุ (แห่ง)','=COUNTIFS(shelter_DB!Y2:Y208,"เกินความจุ")');
note(bkk,18,'ข้อมูลศูนย์พักพิงครอบคลุม 35 เขต • ความจุรวม 15,857 คน • ที่ว่างเป็นยอดต้นทาง จึงไม่เท่ากับความจุรวมลบผู้พักเมื่อบางศูนย์เกินความจุ');
band(bkk,20,'ฐานกลุ่มเปราะบาง กทม. | ประชากรทั้งจังหวัด ไม่ใช่ผู้ประสบภัยที่ยืนยัน');
for(const [j,col,label] of [[0,'C','เด็ก 0–4 ปี (คน)'],[1,'D','หญิงตั้งครรภ์ (คน)'],[2,'E','ผู้สูงอายุ 60 ปีขึ้นไป (คน)']])card(bkk,j,21,label,`=SUMIFS(Vulnerable_group!${col}2:${col}78,Vulnerable_group!B2:B78,"กรุงเทพมหานคร")`);
card(bkk,3,21,'ศูนย์พักพิงมีพิกัด (แห่ง)','=SUM(shelter_DB!Z2:Z208)');
note(bkk,25,'ยังไม่มีฐานประชากรแยกรายเขตและวันอ้างอิง • มีพิกัดศูนย์พักพิงเพียงบางแห่ง แผนที่ต้องแสดงจำนวนที่ไม่มีพิกัดด้วย');
band(bkk,27,'รายการติดตามและหน้ารายละเอียด');
note(bkk,29,'1. เปิด BKK_Districts เพื่อกรองรายเขต: สถานีข้อมูลเก่า ผู้พักพิง ที่ว่าง และศูนย์ที่เกินความจุ');
note(bkk,31,'2. เปิด shelter_DB แล้วกรอง Capacity_check = เกินความจุ เพื่อตรวจสอบ 4 แห่งกับผู้รับผิดชอบ');
note(bkk,33,'3. สถานีรอบข้าง 10 แห่งเก็บไว้ในข้อมูลต้นทาง แต่ไม่รวมในยอดสถานี กทม.');
note(bkk,35,'4. ตำแหน่งสถานีช่วยติดตามระดับน้ำ ไม่ใช้ยืนยันขอบเขตน้ำท่วมหรือจำนวนประชากรที่ได้รับผลกระทบ');
const districts='คลองสาน คลองสามวา คลองเตย คันนายาว จตุจักร จอมทอง ดอนเมือง ดินแดง ดุสิต ตลิ่งชัน ทวีวัฒนา ทุ่งครุ ธนบุรี บางกอกน้อย บางกอกใหญ่ บางกะปิ บางขุนเทียน บางคอแหลม บางซื่อ บางนา บางบอน บางพลัด บางรัก บางเขน บางแค บึงกุ่ม ปทุมวัน ประเวศ ป้อมปราบศัตรูพ่าย พญาไท พระนคร พระโขนง ภาษีเจริญ มีนบุรี ยานนาวา ราชเทวี ราษฎร์บูรณะ ลาดกระบัง ลาดพร้าว วังทองหลาง วัฒนา สวนหลวง สะพานสูง สัมพันธวงศ์ สาทร สายไหม หนองจอก หนองแขม หลักสี่ ห้วยขวาง'.split(' ');
base(district,'L54');table(district,1,['เขต กทม.','สถานีคลอง','สด 0–24 ชั่วโมง','ข้อมูลเก่า','ศูนย์ในข้อมูล','ความจุ (คน)','ผู้พัก (คน)','ที่ว่างต้นทาง (คน)','เกินความจุ (แห่ง)','มีพิกัด (แห่ง)','ข้อควรติดตาม'],districts.map(x=>[x,null,null,null,null,null,null,null,null,null,null]));district.getRange('A:A').format.columnWidthPx=160;district.getRange('B:J').format.columnWidthPx=115;district.getRange('K:K').format.columnWidthPx=280;
for(let i=2;i<=51;i++){
 formula(district,`B${i}`,`=COUNTIFS(BKK_water_DB!$D$2:$D$283,A${i},BKK_water_DB!$X$2:$X$283,"กรุงเทพมหานคร")`);
 for(const [c,status] of [['C','ภายใน 24 ชั่วโมง'],['D','เกิน 24 ชั่วโมง']])formula(district,`${c}${i}`,`=COUNTIFS(BKK_water_DB!$D$2:$D$283,A${i},BKK_water_DB!$X$2:$X$283,"กรุงเทพมหานคร",BKK_water_DB!$Y$2:$Y$283,"${status}")`);
 formula(district,`E${i}`,`=COUNTIFS(shelter_DB!$B$2:$B$208,A${i})`);
 for(const [c,src] of [['F','E'],['G','F'],['H','G'],['J','Z']])formula(district,`${c}${i}`,`=IF(E${i}=0,"ไม่มีข้อมูล",SUMIFS(shelter_DB!$${src}$2:$${src}$208,shelter_DB!$B$2:$B$208,A${i}))`);
 formula(district,`I${i}`,`=IF(E${i}=0,"ไม่มีข้อมูล",COUNTIFS(shelter_DB!$B$2:$B$208,A${i},shelter_DB!$Y$2:$Y$208,"เกินความจุ"))`);
 formula(district,`K${i}`,`=IF(E${i}=0,"ไม่มีข้อมูลศูนย์พักพิง",IF(I${i}>0,"ตรวจผู้พักเกินความจุ",IF(D${i}>0,"ติดตามข้อมูลสถานีเก่า",IF(B${i}=0,"ไม่มีสถานีในชุดข้อมูล","ตรวจสถานะรายสถานี"))))`);
}district.getRange('B2:J51').setNumberFormat('#,##0');district.tables.add('A1:K51',true,'BKKDistrictSummary');district.getRange('I2:I51').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:0,format:{fill:C.red,font:{color:'#9C2525',bold:true}}});
base(guide,'L60');title(guide,'นิยามข้อมูลและแผนพัฒนา','รอบ mockup: 1 ต.ค. 2569 • เกณฑ์และข้อจำกัดสำหรับย้ายไป Google Sheets / Apps Script');
const notes=[
 ['โครงสร้างหน้า','Dashboard ประเทศรวม กทม. / Dashboard_BKK เฉพาะ กทม. / Province_Summary และ BKK_Districts สำหรับกรองข้อมูล'],
 ['วันรายงาน','ใช้วันเดียวจาก Dashboard!C5; นับจังหวัดไม่ซ้ำ; ไม่บวกยอดครัวเรือนหรือผู้เสียชีวิตสะสมข้ามวัน'],
 ['ไม่มีรายงาน','ไม่มีแถวในวันเลือก = ไม่มีรายงาน ไม่ได้หมายความว่าไม่มีภัยหรือสถานการณ์คลี่คลาย'],
 ['การเชื่อมประชากร','จับคู่ชื่อจังหวัดกับ Vulnerable_group ได้; เพิ่มรหัสจังหวัดในระบบจริง; ตัดแถวรวมทั้งหมดออก'],
 ['กลุ่มเปราะบาง','แสดงฐานประชากรทั้งจังหวัดที่มีรายงานภัย; ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง; ยังขาดวันอ้างอิง'],
 ['ความสดสถานี','อายุ 0–24 ชั่วโมงเทียบ fetched_at; ค่าติดลบ = เวลาอนาคต แยกตรวจ; เกิน 24 ชั่วโมง = เก่า; เป็นเกณฑ์ mockup จากไฟล์'],
 ['ระดับสถานี','ใช้สถานะต้นทาง โดยคำนวณยอดวิกฤติ/ล้นตลิ่งเฉพาะเวลาที่ผ่านเกณฑ์; ไม่สร้างเกณฑ์ระดับน้ำสากล'],
 ['ขอบเขต กทม.','BKK_water_DB มี 282 แถว แต่จังหวัดจาก raw_station_json เป็น กทม. 272; อีก 10 อยู่นอก กทม.'],
 ['ศูนย์พักพิง','207 แห่งใน 35 เขต; ใช้ shelter_id เป็น key; ชื่อซ้ำไม่แปลว่าเป็นศูนย์เดียวกัน'],
 ['ความจุและที่ว่าง','แสดงความจุ ผู้พัก และที่ว่างตามต้นทางแยกกัน; บางศูนย์ผู้พักเกินความจุจึงทำให้ยอดรวมต่างกัน'],
 ['พิกัด','ใช้พิกัดจริงที่มีเท่านั้น; ไม่วางศูนย์ที่พิกัดหายบนจุดกลางเขต เพราะทำให้ดูเหมือนตำแหน่งจริง'],
 ['ตารางฐานข้อมูล','Disaster: วันที่+จังหวัด+ประเภทภัย | Station: แหล่ง+รหัสสถานี+เวลาวัด | Shelter: รหัสศูนย์+รอบรายงาน'],
 ['ข้อมูลอ้างอิง','เพิ่ม Province_Master / District_Master: รหัสจังหวัด รหัสเขต เขตสุขภาพ; Source_Log: รอบดึง สำเร็จ/ล้มเหลว เวลาต้นทาง'],
 ['ข้อมูลกรมอนามัยที่ต้องเพิ่ม','ผลประเมินน้ำอุปโภคบริโภค สุขาภิบาลศูนย์พักพิง กลุ่มเปราะบางที่ได้รับผลกระทบจริง การสนับสนุนและผู้รับผิดชอบ'],
 ['ขั้น 1: ตกลงนิยาม','ทวนรายงาน ปภ. และที่มาประชากร; ยืนยันพื้นที่/หน่วย/รอบรายงาน; ตรวจเวลาอนาคต 28 สถานีและศูนย์เกินความจุ 4 แห่ง'],
 ['ขั้น 2: mockup','ใช้สองหน้าภาพรวมพร้อมตารางเจาะจังหวัด/เขต; ทดลองเปลี่ยนวันที่และกรองเขต; ตรวจยอดรวมเทียบต้นทาง'],
 ['ขั้น 3: Google Sheets','ย้าย raw และ master; เก็บประวัติแบบเพิ่มรอบ ไม่ทับข้อมูลย้อนหลัง; ป้องกัน key ซ้ำ; บันทึก source และเวลาตรวจวัด'],
 ['ขั้น 4: Apps Script','หน้าเว็บ 2 แท็บ; ตัวกรองวัน จังหวัด เขตสุขภาพ และเขต กทม.; อ่านข้อมูลเป็นชุดผ่าน google.script.run และ cache'],
 ['ขั้น 5: แผนที่/ติดตาม','ชั้นจังหวัด สถานีน้ำ และศูนย์พักพิง; แสดงรายการไม่มีพิกัด; สีความสดแยกจากระดับเตือน; แสดงเวลาแต่ละแหล่ง'],
 ['ขั้น 6: ทดลองใช้งาน','ตรวจหน้า กทม. รวมย้อนกลับประเทศได้; ไม่มีข้อมูล/ข้อมูลเก่าไม่เป็นสถานะปกติ; ทดสอบรอบนำเข้าล้มเหลวและข้อมูลซ้ำ'],
 ['การแจ้งเตือน','เริ่มเป็นรายการบนหน้าเว็บก่อน; ภายหลังค่อยกำหนดผู้รับ ช่องทางและกติกาซ้ำ โดยให้ผู้รับผิดชอบยืนยันเกณฑ์'],
 ['ขอบเขตรอบนี้','Excel mockup และแผนข้อมูล; ยังไม่ได้สร้าง Google Sheets, deploy Apps Script, ดึงข้อมูลสด หรือส่งแจ้งเตือน'],
];
notes.forEach(([a,b],i)=>{value(guide,`A${i+5}`,a);span(guide,`D${i+5}:L${i+5}`,b);guide.getRange(`A${i+5}:C${i+5}`).merge();guide.getRange(`A${i+5}:L${i+5}`).format={wrapText:true,rowHeight:45};});
value(guide,'A28','วันที่มีรายงาน (ค.ศ.)');value(guide,'A29',new Date('2026-09-30T00:00:00Z'));value(guide,'A30',new Date('2026-10-01T00:00:00Z'));guide.getRange('A29:A30').setNumberFormat('dd/mm/yyyy');
note(guide,33,'เอกสาร Google: https://developers.google.com/apps-script/guides/html');note(guide,35,'แนวทางประสิทธิภาพ: https://developers.google.com/apps-script/guides/support/best-practices');
// Final verification and export.
wb.recalculate();
for(const [s,cells] of [['Dashboard',['A8','D8','G8','J8','D15','J15']],['Dashboard_BKK',['A8','D8','G8','J8','A15','D15','G15','J15','A22','D22','G22','J22']]])console.log(s,Object.fromEntries(cells.map(c=>[c,wb.worksheets.getItem(s).getRange(c).values[0][0]])));
for(const [s,range] of [['Dashboard','A1:L43'],['Dashboard_BKK','A1:L36'],['Province_Summary','A1:K12'],['BKK_Districts','A1:K15'],['Definitions_Plan','A1:L16']]){try{const img=await wb.render({sheetName:s,range,scale:1});await fs.writeFile(`${dir}/${s}.png`,new Uint8Array(await img.arrayBuffer()));}catch(e){console.log('RENDER_ERROR',s,e.message)}}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},summary:'formula errors'});console.log(errors.ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/flood_dashboard_mockup.xlsx`);
