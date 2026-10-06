import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Select HTML
old_title = '<div class="section-title"><h2 id="areaTitle"></h2><button class="lightbtn" id="export">ดาวน์โหลดตาราง CSV</button></div>'
new_title = """<div class="section-title">
  <h2 id="areaTitle"></h2>
  <div style="display:flex; gap:8px">
    <select id="tableSort" style="padding:6px 12px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; background:#fff">
      <option value="households">เรียงตาม: ครัวเรือน (มากไปน้อย)</option>
      <option value="deaths">เรียงตาม: ผู้เสียชีวิต (มากไปน้อย)</option>
      <option value="districts">เรียงตาม: จำนวนอำเภอ (มากไปน้อย)</option>
      <option value="subdistricts">เรียงตาม: จำนวนตำบล (มากไปน้อย)</option>
      <option value="villages">เรียงตาม: จำนวนหมู่บ้าน (มากไปน้อย)</option>
      <option value="trend">เรียงตาม: แนวโน้มน้ำ</option>
      <option value="status">เรียงตาม: สถานะรายงาน</option>
      <option value="province">เรียงตาม: ชื่อจังหวัด (ก-ฮ)</option>
      <option value="region">เรียงตาม: เขตสุขภาพ</option>
    </select>
    <button class="lightbtn" id="export">ดาวน์โหลดตาราง CSV</button>
  </div>
</div>"""

if old_title in html:
    html = html.replace(old_title, new_title)
    print("Added select HTML")
else:
    print("Could not find title HTML")

# 2. Add event listener and state
old_event = "$('reportDate').addEventListener('change',e=>{state.date=e.target.value;render()});"
new_event = "$('reportDate').addEventListener('change',e=>{state.date=e.target.value;render()});\n$('tableSort').addEventListener('change',e=>{state.tableSort=e.target.value;render()});"

if old_event in html:
    html = html.replace(old_event, new_event)
    print("Added event listener")
else:
    print("Could not find event listener")

# 3. Update sorting logic
old_js = """  const headers=['จังหวัด','เขตสุขภาพ','อำเภอ','ตำบล','หมู่บ้าน','ครัวเรือน','เสียชีวิต','น้ำ','สถานะ'];
  const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ไม่มีข้อมูล'}}).sort((a,b)=>(b.r?.Affected_Households||0)-(a.r?.Affected_Households||0));"""

new_js = """  const headers=['จังหวัด','เขตสุขภาพ','อำเภอ','ตำบล','หมู่บ้าน','ครัวเรือน','เสียชีวิต','น้ำ','สถานะ'];
  let sortKey = state.tableSort || 'households';
  const getNum = (str) => parseInt(String(str||'0').replace(/[^0-9]/g, '')) || 0;
  const trendVal = t => t==='เพิ่มขึ้น'?3:t==='ทรงตัว'?2:t==='ลดลง'?1:0;
  
  const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ไม่มีข้อมูล'}}).sort((a,b)=>{
    if (sortKey === 'province') return a.p.localeCompare(b.p, 'th');
    if (sortKey === 'region') return getNum(a.region) - getNum(b.region);
    if (sortKey === 'districts') return getNum(b.r?.Affected_Districts_Count) - getNum(a.r?.Affected_Districts_Count);
    if (sortKey === 'subdistricts') return getNum(b.r?.Affected_Subdistricts_Count) - getNum(a.r?.Affected_Subdistricts_Count);
    if (sortKey === 'villages') return getNum(b.r?.Affected_Villages_Count) - getNum(a.r?.Affected_Villages_Count);
    if (sortKey === 'deaths') return getNum(b.r?.Casualties_Deaths) - getNum(a.r?.Casualties_Deaths);
    if (sortKey === 'trend') return trendVal(b.r?.Water_Level_Trend) - trendVal(a.r?.Water_Level_Trend);
    if (sortKey === 'status') return String(b.r?.Current_Status||'').localeCompare(String(a.r?.Current_Status||''), 'th');
    return (b.r?.Affected_Households||0)-(a.r?.Affected_Households||0);
  });
  if ($('tableSort')) $('tableSort').value = sortKey;
"""

if old_js in html:
    html = html.replace(old_js, new_js)
    print("Updated sorting logic")
else:
    print("Could not find JS logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
