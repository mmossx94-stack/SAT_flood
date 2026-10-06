import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update WATER_STATUS
old_water = "const WATER_STATUS={ล้นตลิ่ง:{rank:5,color:'#991b1b'},วิกฤต:{rank:4,color:'#dc2626'},เตือนภัย:{rank:3,color:'#f97316'},เฝ้าระวัง:{rank:2,color:'#facc15'},ปกติ:{rank:1,color:'#22c55e'}};"
new_water = "const WATER_STATUS={ล้นตลิ่ง:{rank:5,color:'#581c87'},วิกฤต:{rank:4,color:'#9333ea'},เตือนภัย:{rank:3,color:'#f97316'},เฝ้าระวัง:{rank:2,color:'#facc15'},ปกติ:{rank:1,color:'transparent'}};"

content = content.replace(old_water, new_water)

# 2. Hide dots completely if they are transparent
# L.circleMarker([r.latitude,r.longitude],{radius:6,fillColor:c,color:'#000',weight:0.5,fillOpacity:0.9})
# Change to: let op = c==='transparent' ? 0 : 0.9; let stroke = c==='transparent' ? 0 : 0.5; ... fillOpacity: op, opacity: stroke

dot_regex = r"L\.circleMarker\(\[r\.latitude,r\.longitude\],\{radius:6,fillColor:c,color:'#000',weight:0\.5,fillOpacity:0\.9\}\)"
new_dot = "L.circleMarker([r.latitude,r.longitude],{radius:8,fillColor:c,color:c==='transparent'?'transparent':'#000',weight:c==='transparent'?0:0.5,fillOpacity:c==='transparent'?0:0.8,opacity:c==='transparent'?0:0.8})"

content = re.sub(dot_regex, new_dot, content)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied Heatmap settings")
