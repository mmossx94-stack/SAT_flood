import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_bkk_legend = "$('districtWaterLegend').innerHTML=Object.entries(WATER_STATUS).map(([label,value])=>`<span><i class=\"dot\" style=\"border-radius:2px;background:${value.color}\"></i>${label}</span>`).join('')+'<span><i class=\"dot\" style=\"border-radius:2px;background:#94a3b8\"></i>ขัดข้อง / ไม่ทราบสถานะ</span><span>ไม่ระบายสี: ไม่มีสถานีในข้อมูล</span>';"

new_bkk_legend = """const activeStatuses=new Set(rows.map(r=>canonicalWaterStatus(r.flood_status_source)));
const knownLegend=Object.entries(WATER_STATUS).filter(([label])=>activeStatuses.has(label)).map(([label,value])=>`<span><i class="dot" style="border-radius:2px;background:${value.color}"></i>${label}</span>`).join('');
const unknownStatuses=Array.from(activeStatuses).filter(s=>s&&!WATER_STATUS[s]);
const unknownLegend=unknownStatuses.length?`<span><i class="dot" style="border-radius:2px;background:#94a3b8"></i>${unknownStatuses.join(' / ')}</span>`:'';
$('districtWaterLegend').innerHTML=knownLegend+unknownLegend+'<span>ไม่ระบายสี: ไม่มีสถานีในข้อมูล</span>';"""

if old_bkk_legend in html:
    html = html.replace(old_bkk_legend, new_bkk_legend.replace('\n', ' '))
    print("Replaced BKK legend")
else:
    print("Could not find old BKK legend")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
