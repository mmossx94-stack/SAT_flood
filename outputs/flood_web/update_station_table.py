import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update statusBadge
old_status_badge = "const statusBadge=s=>badge(s,['ล้นตลิ่ง','วิกฤติ'].includes(s)?'bad':['เตือนภัย','เฝ้าระวัง'].includes(s)?'warn':s==='ปกติ'?'good':'');"
new_status_badge = "const statusBadge=s=>{const c=canonicalWaterStatus(s);const color=WATER_STATUS[c]?.color;return color?`<span class=\"badge\" style=\"background-color:${color};color:${color==='#facc15'?'#000':'#fff'}\">${esc(s)}</span>`:badge(s);};"
js = js.replace(old_status_badge, new_status_badge)

# 2. Remove 'ความสด' column from renderStations
old_render = "$('stationTable').innerHTML=table(['สถานี',state.tab==='bkk'?'เขต':'พื้นที่','ระดับน้ำ (ม. รทก.)','สถานะต้นทาง','ความสด','เวลาตรวจวัด'],rows.map(r=>[esc(r.station_name),esc(r.district_or_area),typeof r.water_in_m_msl==='number'?r.water_in_m_msl.toFixed(2):'ไม่มีข้อมูล',statusBadge(r.flood_status_source),qualityBadge(r),time(r.observed_at_th)]));"
new_render = "$('stationTable').innerHTML=table(['สถานี',state.tab==='bkk'?'เขต':'พื้นที่','ระดับน้ำ (ม. รทก.)','สถานะต้นทาง','เวลาตรวจวัด'],rows.map(r=>[esc(r.station_name),esc(r.district_or_area),typeof r.water_in_m_msl==='number'?r.water_in_m_msl.toFixed(2):'ไม่มีข้อมูล',statusBadge(r.flood_status_source),time(r.observed_at_th)]));"
js = js.replace(old_render, new_render)

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
