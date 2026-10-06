import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace HTML
old_html = """<section class="panel">
  <div class="panel-head">
    <div><h2>กลุ่มเปราะบาง และผลกระทบ</h2><p class="sub" id="vulnerableSub"></p></div>
    <span class="badge">ฐานประชากรทั้งจังหวัด</span>
  </div>
  <div class="panel-body" style="display:flex; flex-direction:column; gap:20px; padding: 20px;">
    
    <div style="display:flex; gap:24px; align-items:center; min-height:220px; flex-wrap: wrap;">
      <!-- LEFT: Pie Chart -->
      <div style="flex: 1 1 300px; position: relative; height: 200px;">
        <canvas id="vulChart"></canvas>
        <div id="vulChartEmpty" class="hidden" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:#94a3b8; font-size:13px;">ไม่มีข้อมูลกลุ่มเปราะบาง</div>
      </div>
      
      <!-- RIGHT: DDPM Box -->
      <div style="flex: 1 1 200px; display: flex; flex-direction: column; gap: 12px; justify-content: center;">
        <div class="stat-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px; text-align:center;">
          <div style="font-size:14px; color:#475569; margin-bottom:8px; font-weight:600;">จำนวนครัวเรือนที่ได้รับผลกระทบ</div>
          <div style="font-size:36px; font-weight:700; color:#dc2626; line-height:1;" id="vulHouseholds">-</div>
          <div style="font-size:13px; color:#64748b; margin-top:12px;">ข้อมูลจาก กรมป้องกันและบรรเทาสาธารณภัย</div>
        </div>
      </div>
    </div>

    <div style="font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 12px;">
      <b>ที่มาข้อมูล:</b> ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ (HDC) กระทรวงสาธารณสุข และ กรมป้องกันและบรรเทาสาธารณภัย (ปภ.) กระทรวงมหาดไทย<br/>
      <span style="color:#94a3b8; font-size: 10px;">*จำนวนกลุ่มเปราะบางอ้างอิงจากฐานประชากรทั้งจังหวัด ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง</span>
    </div>
  </div>
</section>"""

new_html = """<section class="panel" id="nationalVulPanel">
  <div class="panel-head"><div><h2>กลุ่มเปราะบางเพื่อวางแผนรองรับ</h2><p class="sub" id="vulnerableSubNational"></p></div><span class="badge">ฐานประชากรทั้งจังหวัด</span></div>
  <div class="panel-body"><div class="vulnerable" id="vulnerableNational"></div><div class="table-wrap" id="vulTable" style="margin-top:20px;"></div><p class="mini-note" style="margin-top:12px;">ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง • ไฟล์ไม่ได้ระบุวันอ้างอิงฐานประชากร • ไม่รวมแถว “รวมทั้งหมด” ซ้ำ</p></div>
</section>

<section class="panel hidden" id="bkkVulPanel">
  <div class="panel-head">
    <div><h2>กลุ่มเปราะบาง และผลกระทบ</h2><p class="sub" id="vulnerableSubBkk"></p></div>
    <span class="badge">ฐานประชากร กทม.</span>
  </div>
  <div class="panel-body" style="display:flex; flex-direction:column; gap:20px; padding: 20px;">
    <div style="display:flex; gap:24px; align-items:center; min-height:220px; flex-wrap: wrap;">
      <div style="flex: 1 1 300px; position: relative; height: 200px;">
        <canvas id="vulChart"></canvas>
        <div id="vulChartEmpty" class="hidden" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:#94a3b8; font-size:13px;">ไม่มีข้อมูลกลุ่มเปราะบาง</div>
      </div>
      <div style="flex: 1 1 200px; display: flex; flex-direction: column; gap: 12px; justify-content: center;">
        <div class="stat-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px; text-align:center;">
          <div style="font-size:14px; color:#475569; margin-bottom:8px; font-weight:600;">จำนวนครัวเรือนที่ได้รับผลกระทบ</div>
          <div style="font-size:36px; font-weight:700; color:#dc2626; line-height:1;" id="vulHouseholds">-</div>
          <div style="font-size:13px; color:#64748b; margin-top:12px;">ข้อมูลจาก กรมป้องกันและบรรเทาสาธารณภัย</div>
        </div>
      </div>
    </div>
    <div style="font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 12px;">
      <b>ที่มาข้อมูล:</b> ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ (HDC) กระทรวงสาธารณสุข และ กรมป้องกันและบรรเทาสาธารณภัย (ปภ.) กระทรวงมหาดไทย<br/>
      <span style="color:#94a3b8; font-size: 10px;">*จำนวนกลุ่มเปราะบางอ้างอิงจากฐานประชากรทั้ง กทม. ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง</span>
    </div>
  </div>
</section>"""

if old_html in html:
    html = html.replace(old_html, new_html)
    print("Replaced HTML logic successfully")
else:
    print("Could not find HTML logic!")

# 2. Replace JS
old_js = """ const v=DATA.vulnerable.filter(r=>bkk?r.province==='กรุงเทพมหานคร':affected.includes(r.province));
 $('vulnerableSub').textContent=bkk?'ฐานประชากรทั้ง กทม. ไม่เปลี่ยนตามตัวกรองเขต เพราะยังไม่มีข้อมูลรายเขต':`ฐานประชากรใน ${fmt(v.length)} จังหวัดที่มีรายงานภัยตามตัวกรอง`;
 
 const vGroups = [
   { key: 'เด็ก 0-4 ปี', val: sum(v, 'children'), color: '#3b82f6' },
   { key: 'หญิงตั้งครรภ์', val: sum(v, 'pregnant'), color: '#f59e0b' },
   { key: 'ผู้สูงอายุ 60 ปีขึ้นไป', val: sum(v, 'elderly'), color: '#10b981' }
 ].filter(g => g.val > 0);
 
 if (window.vulChartInstance) {
   window.vulChartInstance.destroy();
 }
 const ctx = document.getElementById('vulChart');
 if (ctx && vGroups.length > 0) {
   $('vulChartEmpty').classList.add('hidden');
   window.vulChartInstance = new Chart(ctx, {
     type: 'doughnut',
     data: {
       labels: vGroups.map(g => g.key),
       datasets: [{
         data: vGroups.map(g => g.val),
         backgroundColor: vGroups.map(g => g.color),
         borderWidth: 1,
         borderColor: '#ffffff'
       }]
     },
     options: {
       responsive: true,
       maintainAspectRatio: false,
       cutout: '60%',
       plugins: {
         legend: { position: 'right', labels: { boxWidth: 12, font: { family: "'IBM Plex Sans Thai', sans-serif", size: 12 } } },
         tooltip: { titleFont: { family: "'IBM Plex Sans Thai', sans-serif" }, bodyFont: { family: "'IBM Plex Sans Thai', sans-serif" } }
       }
     }
   });
 } else if (ctx) {
   $('vulChartEmpty').classList.remove('hidden');
 }
 
 const currentHouseholds = sum(reports.filter(r=>allowed.includes(r.Province)), 'Affected_Households');
 $('vulHouseholds').textContent = currentHouseholds > 0 ? fmt(currentHouseholds) : '0';"""

new_js = """ if (bkk) {
   const vBkk = DATA.vulnerable.filter(r => r.province === 'กรุงเทพมหานคร');
   $('vulnerableSubBkk').textContent = 'ฐานประชากรทั้ง กทม. ไม่เปลี่ยนตามตัวกรองเขต เพราะยังไม่มีข้อมูลรายเขต';
   
   const vGroups = [
     { key: 'เด็ก 0-4 ปี', val: sum(vBkk, 'children'), color: '#3b82f6' },
     { key: 'หญิงตั้งครรภ์', val: val = sum(vBkk, 'pregnant'), color: '#f59e0b' },
     { key: 'ผู้สูงอายุ 60 ปีขึ้นไป', val: sum(vBkk, 'elderly'), color: '#10b981' }
   ].filter(g => g.val > 0);
   
   if (window.vulChartInstance) { window.vulChartInstance.destroy(); }
   const ctx = document.getElementById('vulChart');
   if (ctx && vGroups.length > 0) {
     $('vulChartEmpty').classList.add('hidden');
     window.vulChartInstance = new Chart(ctx, {
       type: 'doughnut',
       data: {
         labels: vGroups.map(g => g.key),
         datasets: [{ data: vGroups.map(g => g.val), backgroundColor: vGroups.map(g => g.color), borderWidth: 1, borderColor: '#ffffff' }]
       },
       options: {
         responsive: true, maintainAspectRatio: false, cutout: '60%',
         plugins: {
           legend: { position: 'right', labels: { boxWidth: 12, font: { family: "'IBM Plex Sans Thai', sans-serif", size: 12 } } },
           tooltip: { titleFont: { family: "'IBM Plex Sans Thai', sans-serif" }, bodyFont: { family: "'IBM Plex Sans Thai', sans-serif" } }
         }
       }
     });
   } else if (ctx) {
     $('vulChartEmpty').classList.remove('hidden');
   }
   
   const currentHouseholds = sum(reports.filter(r => r.Province === 'กรุงเทพมหานคร'), 'Affected_Households');
   $('vulHouseholds').textContent = currentHouseholds > 0 ? fmt(currentHouseholds) : '0';
 } else {
   const vNat = DATA.vulnerable.filter(r => affected.includes(r.province));
   $('vulnerableSubNational').textContent = `ฐานประชากรใน ${fmt(vNat.length)} จังหวัดที่มีรายงานภัยตามตัวกรอง`;
   const affectedProvs = new Set(reports.filter(r => r.Current_Status === 'กำลังประสบภัย').map(r => r.Province)).size; 
   $('vulnerableNational').innerHTML = card('จังหวัดที่ประสบภัย', affectedProvs, 'จังหวัด', '') + [['เด็ก 0-4 ปี', sum(vNat, 'children')], ['หญิงตั้งครรภ์', sum(vNat, 'pregnant')], ['ผู้สูงอายุ 60 ปีขึ้นไป', sum(vNat, 'elderly')]].map(([t, n]) => card(t, n, 'คน', '')).join(''); 
   const vulHeaders = ['จังหวัด', 'เขตสุขภาพ', '<div style="text-align:right">เด็ก 0-4 ปี</div>', '<div style="text-align:right">หญิงตั้งครรภ์</div>', '<div style="text-align:right">ผู้สูงอายุ 60 ปีขึ้นไป</div>', '<div style="text-align:right">รวมกลุ่มเปราะบาง</div>']; 
   const vulRows = vNat.slice().sort((a,b)=>((b.children||0)+(b.pregnant||0)+(b.elderly||0))-((a.children||0)+(a.pregnant||0)+(a.elderly||0))).map(r => {
     const c = (r.children||0) + (r.pregnant||0) + (r.elderly||0);
     return [ `<button class="linkbutton" data-province="${esc(r.province)}">${esc(r.province)}</button>`, esc(r.region||'-'), `<div style="text-align:right">${fmt(r.children||0)}</div>`, `<div style="text-align:right">${fmt(r.pregnant||0)}</div>`, `<div style="text-align:right">${fmt(r.elderly||0)}</div>`, `<div style="text-align:right;font-weight:bold">${fmt(c)}</div>` ];
   });
   $('vulTable').innerHTML = table(vulHeaders, vulRows);
 }"""

if old_js in html:
    html = html.replace(old_js, new_js)
    print("Replaced JS logic successfully")
else:
    print("Could not find JS logic!")
    
# Add toggle rules
old_toggle = "$('allSheltersPanel').classList.toggle('hidden',!bkk);"
new_toggle = "$('allSheltersPanel').classList.toggle('hidden',!bkk);\n$('nationalVulPanel').classList.toggle('hidden', bkk);\n$('bkkVulPanel').classList.toggle('hidden', !bkk);"
if old_toggle in html:
    html = html.replace(old_toggle, new_toggle)
    print("Added toggle logic")
else:
    print("Could not find toggle logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
