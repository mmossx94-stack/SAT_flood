import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_block = "const activeStatuses=new Set(rows.map(r=>canonicalWaterStatus(r.flood_status_source))); const knownLegend=Object.entries(WATER_STATUS).filter(([label])=>activeStatuses.has(label)).map(([label,value])=>`<span><i class=\"dot\" style=\"border-radius:2px;background:${value.color}\"></i>${label}</span>`).join(''); const unknownStatuses=Array.from(activeStatuses).filter(s=>s&&!WATER_STATUS[s]); const unknownLegend=unknownStatuses.length?`<span><i class=\"dot\" style=\"border-radius:2px;background:#94a3b8\"></i>${unknownStatuses.join(' / ')}</span>`:''; $('districtWaterLegend').innerHTML=knownLegend+unknownLegend+'<span>ไม่ระบายสี: ไม่มีสถานีในข้อมูล</span>';"

# Remove it from where it is
html = html.replace(bad_block, "")

# Insert it AFTER const rows=...
target = "const rows=DATA.bkkStations.filter(r=>r.province==='กรุงเทพมหานคร'),summaries=new Map();"
html = html.replace(target, target + bad_block)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Fixed JS order!")
