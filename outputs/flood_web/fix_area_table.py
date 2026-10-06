import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update `function table(headers,rows)` to NOT auto right-align
old_table = 'function table(headers,rows){return `<table><thead><tr>${headers.map((h,i)=>`<th class="${i?\'num\':\'\'}">${h}</th>`).join(\'\')}</tr></thead><tbody>${rows.length?rows.map(row=>`<tr>${row.map((v,i)=>`<td class="${i?\'num\':\'\'}">${v}</td>`).join(\'\')}</tr>`).join(\'\'):`<tr><td colspan="${headers.length}" class="empty">ไม่มีข้อมูลในขอบเขตที่เลือก</td></tr>`}</tbody></table>`}'
new_table = 'function table(headers,rows){return `<table><thead><tr>${headers.map((h,i)=>`<th>${h}</th>`).join(\'\')}</tr></thead><tbody>${rows.length?rows.map(row=>`<tr>${row.map((v,i)=>`<td>${v}</td>`).join(\'\')}</tr>`).join(\'\'):`<tr><td colspan="${headers.length}" class="empty">ไม่มีข้อมูลในขอบเขตที่เลือก</td></tr>`}</tbody></table>`}'
if old_table in html:
    html = html.replace(old_table, new_table)
    print("Fixed table function to stop auto right-align")

# 2. Update the `areaTable` rendering
old_area = "else{$('areaTitle').textContent='รายละเอียดจังหวัดตามจำนวนครัวเรือนที่ประสบภัย และแนวโน้มรายจังหวัด';const headers=['จังหวัด','เขตสุขภาพ','ครัวเรือน','แนวโน้มน้ำ','สถานะรายงาน','ความสด ณ นำเข้า'];const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ยังไม่เชื่อมข้อมูล'}}).sort((a,b)=>(b.r?.Affected_Households||0)-(a.r?.Affected_Households||0));$('areaTable').innerHTML=table(headers,rows.map(({p,r,region})=>[`<button class=\"linkbutton\" data-province=\"${esc(p)}\">${esc(p)}</button>`,esc(region),r?fmt(r.Affected_Households):'ไม่มีรายงาน',r?badge(r.Water_Level_Trend,r.Water_Level_Trend==='เพิ่มขึ้น'?'warn':''):'—',r?badge(r.Current_Status,'warn'):badge('ไม่มีรายงานในวันที่เลือก'),r?qualityBadge(r):'—']));csvRows=[headers,...rows.map(({p,r,region})=>[p,region,r?.Affected_Households??'ไม่มีรายงาน',r?.Water_Level_Trend??'',r?.Current_Status??'ไม่มีรายงานในวันที่เลือก',r?quality(r):'ไม่ทราบเวลาข้อมูล'])];}}"

new_area = """else{
  $('areaTitle').textContent='รายละเอียดตารางสถานการณ์ภัย (อิงรายงาน ปภ.)';
  const headers=['จังหวัด','เขตสุขภาพ','อำเภอ','ตำบล','หมู่บ้าน','ครัวเรือน','เสียชีวิต','น้ำ','สถานะ','หมายเหตุ','อัปเดต'];
  const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ไม่มีข้อมูล'}}).sort((a,b)=>(b.r?.Affected_Households||0)-(a.r?.Affected_Households||0));
  $('areaTable').innerHTML=table(headers,rows.map(({p,r,region})=>[
    `<button class="linkbutton" data-province="${esc(p)}">${esc(p)}</button>`,
    esc(region),
    r ? `<div style="max-width:140px;white-space:normal;font-size:13px">${esc(r.District_Names||r.Affected_Districts_Count||'-')}</div>` : '—',
    r ? `<div style="text-align:right">${esc(r.Affected_Subdistricts_Count||'-')}</div>` : '—',
    r ? `<div style="text-align:right">${esc(r.Affected_Villages_Count||'-')}</div>` : '—',
    r ? `<div style="text-align:right;font-weight:bold;color:#991b1b">${fmt(r.Affected_Households)}</div>` : '—',
    r ? `<div style="text-align:right">${r.Casualties_Deaths==null?'-':fmt(r.Casualties_Deaths)}</div>` : '—',
    r ? `<span class="badge" style="${r.Water_Level_Trend==='เพิ่มขึ้น'?'background:#082f6b;color:#fff':r.Water_Level_Trend==='ทรงตัว'?'background:#3b82f6;color:#fff':r.Water_Level_Trend==='ลดลง'?'background:#93c5fd;color:#082f6b':'background:#e2e8f0;color:#64748b'}">${esc(r.Water_Level_Trend)}</span>` : '—',
    r ? badge(r.Current_Status, r.Current_Status==='กำลังประสบภัย'?'warn':'') : badge('ไม่มีรายงาน'),
    r ? `<div style="max-width:240px;white-space:normal;font-size:12px;line-height:1.4;color:#475569">${esc(r.Remarks||'-')}</div>` : '—',
    r ? qualityBadge(r) : '—'
  ]));
  csvRows=[headers,...rows.map(({p,r,region})=>[
    p, region, 
    r?.District_Names||r?.Affected_Districts_Count||'-', 
    r?.Affected_Subdistricts_Count||'-', 
    r?.Affected_Villages_Count||'-', 
    r?.Affected_Households??'-', 
    r?.Casualties_Deaths??'-', 
    r?.Water_Level_Trend??'-', 
    r?.Current_Status??'ไม่มีรายงาน', 
    r?.Remarks??'-', 
    r?quality(r):'-'
  ])];
}"""

if old_area in html:
    html = html.replace(old_area, new_area.replace('\n', ''))
    print("Replaced areaTable rendering logic")
else:
    print("Could not find areaTable logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
