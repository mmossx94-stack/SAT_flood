import re

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

renderAreas_code = """function renderAreas(reports,allowed){
  if(state.tab==='bkk'){
    $('areaTitle').textContent='ข้อมูลผู้มาใช้ศูนย์พักพิงรายเขต';
    const rows=districts.filter(x=>!state.district||x===state.district).map(x=>{
      let s=currentShelters.filter(r=>r.district===x),w=DATA.bkkStations.filter(r=>r.province==='กรุงเทพมหานคร'&&r.district_or_area===x);
      return {name:x,stations:w.length,old:w.filter(r=>quality(r)==='ข้อมูลเก่าเกิน 24 ชั่วโมง').length,centers:s.length,occupied:s.length?sum(s,'occupied'):null,available:s.length?sum(s,'available'):null,over:s.length?s.filter(r=>r.occupied>r.capacity).length:null}
    }).sort((a,b)=>(b.over||0)-(a.over||0)||(b.occupied||0)-(a.occupied||0));
    const headers=['เขต','ศูนย์พักพิงที่มีรายงาน (แห่ง)','ผู้พัก (คน)','ที่ว่าง (คน)','เกินความจุ (แห่ง)'];
    $('areaTable').innerHTML=table(headers,rows.map(r=>[`<button class="linkbutton" data-district="${esc(r.name)}">${esc(r.name)}</button>`,fmt(r.centers),fmt(r.occupied),fmt(r.available),r.over?badge(fmt(r.over),'bad'):fmt(r.over)]));
    csvRows=[headers,...rows.map(r=>[r.name,r.centers,r.occupied??'ไม่มีข้อมูล',r.available??'ไม่มีข้อมูล',r.over??'ไม่มีข้อมูล'])];
  } else {
    $('areaTitle').textContent='รายละเอียดจังหวัดตามจำนวนครัวเรือนที่ประสบภัย และแนวโน้มรายจังหวัด';
    const headers=['จังหวัด','เขตสุขภาพ','อำเภอ','ตำบล','หมู่บ้าน','ครัวเรือน','เสียชีวิต','น้ำ','สถานะ'];
    const rows=allowed.map(p=>{
      const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);
      return {p,r,region:v?.region||'ไม่มีข้อมูล'}
    }).filter(row => row.r && row.r.Current_Status === 'กำลังประสบภัย').sort((a,b) => (b.r?.Affected_Households||0) - (a.r?.Affected_Households||0));
    $('areaTable').innerHTML=table(headers,rows.map(({p,r,region})=>[
      `<button class="linkbutton" data-province="${esc(p)}">${esc(p)}</button>`, esc(region),
      r ? `<div style="max-width:140px;white-space:normal;font-size:13px">${esc(r.District_Names||(r.Affected_Districts_Count??'-'))}</div>` : '—',
      r ? `<div style="text-align:right">${esc(r.Affected_Subdistricts_Count??'-')}</div>` : '—',
      r ? `<div style="text-align:right">${esc(r.Affected_Villages_Count??'-')}</div>` : '—',
      r ? `<div style="text-align:right;font-weight:bold;color:#991b1b">${fmt(r.Affected_Households)}</div>` : '—',
      r ? `<div style="text-align:right">${r.Casualties_Deaths==null?'-':fmt(r.Casualties_Deaths)}</div>` : '—',
      r ? `<span class="badge" style="${r.Water_Level_Trend==='เพิ่มขึ้น'?'background:#082f6b;color:#fff':r.Water_Level_Trend==='ทรงตัว'?'background:#3b82f6;color:#fff':r.Water_Level_Trend==='ลดลง'?'background:#93c5fd;color:#082f6b':'background:#e2e8f0;color:#64748b'}">${esc(r.Water_Level_Trend)}</span>` : '—',
      r ? badge(r.Current_Status, r.Current_Status==='กำลังประสบภัย'?'warn':'') : badge('ไม่มีรายงาน')
    ]));
    csvRows=[headers,...rows.map(({p,r,region})=>[
      p, region, r?.District_Names||(r?.Affected_Districts_Count??'-'), r?.Affected_Subdistricts_Count??'-', r?.Affected_Villages_Count??'-', r?.Affected_Households??'-', r?.Casualties_Deaths??'-', r?.Water_Level_Trend??'-', r?.Current_Status??'ไม่มีรายงาน'
    ])];
  }
}
"""

js = js.replace("function renderStations(){", renderAreas_code + "\nfunction renderStations(){")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Restored renderAreas!")
