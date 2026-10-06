import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update HTML
start_remove = '<section class="panel hidden" id="shelterPanel"'
end_remove = '<footer class="foot">'

if start_remove in html and end_remove in html:
    idx_start = html.find(start_remove)
    idx_end = html.find(end_remove)
    html = html[:idx_start] + html[idx_end:]
    print("Removed HTML after stationTable")
else:
    print("Could not find HTML to remove")

# 2. Update JS: Remove $('quality') and $('actions') and old shelter render logic
js_lines = html.split('\n')
new_lines = []
for line in js_lines:
    if "$('quality').innerHTML=" in line:
        # Keep everything up to the quality assignment, but remove quality and after on that line if they exist
        # Let's just do a string replace on the specific lines
        pass
    if "$('actions').innerHTML=" in line:
        pass

html_str = '\n'.join(js_lines)

# Safely replace the specific lines
old_q_line = " renderAreas(reports,allowed);$('quality').innerHTML=metric('รายงาน ปภ. ผ่านเกณฑ์ 24 ชั่วโมง',fmt(reports.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').length)+' / '+fmt(reports.length))+metric('รายงาน ปภ. ไม่ทราบเวลาข้อมูล',fmt(reports.filter(r=>quality(r)==='ไม่ทราบเวลาข้อมูล').length))+metric('เวลานำเข้าข้อมูล ปภ.', time(reports.map(r=>r.Ingested_At).filter(x=>x).sort().pop()))+metric('กลุ่มเปราะบาง','ไม่ทราบเวลาข้อมูล')+(bkk?metric('ศูนย์พักพิงภายใน 24 ชั่วโมง',fmt(currentShelters.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').length)+' / '+fmt(currentShelters.length)):'');"

new_q_line = " renderAreas(reports,allowed);"
if old_q_line in html_str:
    html_str = html_str.replace(old_q_line, new_q_line)
    print("Removed quality JS")

old_a_line = " $('actions').innerHTML=bkk?`<p>ตรวจสอบศูนย์ที่มีผู้พักเกินความจุ <b>${fmt(currentShelters.filter(r=>r.occupied>r.capacity).length)} แห่ง</b></p><p>ศูนย์ที่ไม่อัปเดตเกิน 3 วัน <b>${fmt(currentShelters.filter(r=>quality(r)==='ไม่ทราบเวลาข้อมูล').length)} แห่ง</b></p>`:`<p>รอการปรับโครงสร้างเพื่อแสดงพื้นที่รับน้ำหลักในภูมิภาค</p>`;"
if old_a_line in html_str:
    html_str = html_str.replace(old_a_line, "")
    print("Removed actions JS")

old_s_render = "renderShelterTableOld(currentShelters); "
if old_s_render in html_str:
    html_str = html_str.replace(old_s_render, "")
    print("Removed old shelter call")

# 3. Update Sort Logic in renderStations
old_sort = """const rows=currentStations.filter(r=>(!term||(r.station_name+' '+r.district_or_area).includes(term))&&(!status||r.flood_status_source===status)).sort((a,b)=>{let sev={ล้นตลิ่ง:5,วิกฤติ:4,เตือนภัย:3,เฝ้าระวัง:2,ปกติ:1};return (quality(b)==='ภายใน 24 ชั่วโมง')-(quality(a)==='ภายใน 24 ชั่วโมง')||(sev[b.flood_status_source]||0)-(sev[a.flood_status_source]||0)});"""

new_sort = """const rows=currentStations.filter(r=>(!term||(r.station_name+' '+r.district_or_area).includes(term))&&(!status||r.flood_status_source===status)).sort((a,b)=>{
    const sa = canonicalWaterStatus(a.flood_status_source);
    const sb = canonicalWaterStatus(b.flood_status_source);
    const rankA = WATER_STATUS[sa]?.rank || 0;
    const rankB = WATER_STATUS[sb]?.rank || 0;
    if (rankA !== rankB) return rankB - rankA;
    const timeA = new Date(a.updated_at_source || a.Ingested_At).getTime() || 0;
    const timeB = new Date(b.updated_at_source || b.Ingested_At).getTime() || 0;
    return timeB - timeA;
  });"""

if old_sort in html_str:
    html_str = html_str.replace(old_sort, new_sort)
    print("Replaced sort logic")
else:
    print("Could not find old sort logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html_str)
