import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = "$('shelterMapLegend2').innerHTML=districtWaterLegendHTML();"
new_str = """
 const waterRows2=DATA.bkkStations.filter(r=>r.province==='กรุงเทพมหานคร');
 const activeStatuses2=new Set(waterRows2.map(r=>canonicalWaterStatus(r.flood_status_source)));
 $('shelterMapLegend2').innerHTML='<span style="font-weight:bold;margin-right:8px">สถานะน้ำสูงสุดรายเขต:</span>'+['วิกฤต','เตือนภัย','ปกติ','ขัดข้อง / ขัดข้องชั่วคราว'].filter(s=>activeStatuses2.has(s)).map(s=>`<span><i class="dot" style="background:${WATER_STATUS[s]?.color||'#94a3b8'}"></i>${s}</span>`).join('')+'<span>ไม่ระบายสี: ไม่มีสถานีในข้อมูล</span>';
"""

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed shelter legend")
else:
    print("Could not find old string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
