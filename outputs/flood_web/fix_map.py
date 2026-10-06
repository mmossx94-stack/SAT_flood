import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reduce shelter pin size
content = content.replace("?14:18;", "?10:14;")

# 2. Update circleMarker for stations to use WATER_STATUS colors
# Original line:
# const pts=[];currentStations.forEach(r=>{if(typeof r.latitude!=='number'||typeof r.longitude!=='number')return;let q=quality(r),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':['วิกฤติ','ล้นตลิ่ง'].includes(r.flood_status_source)?'#00008B':['เตือนภัย','เฝ้าระวัง'].includes(r.flood_status_source)?'#4169E1':'#ffffff';L.circleMarker([r.latitude,r.longitude],{radius: 1.5,fillColor:c,color:'#333',weight:0.5,fillOpacity:1})
# Replace the `let q=quality(r),c=...` with logic that uses WATER_STATUS

old_marker_logic = r"let q=quality(r),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':\['วิกฤติ','ล้นตลิ่ง'\].includes\(r\.flood_status_source\)\?'#00008B':\['เตือนภัย','เฝ้าระวัง'\].includes\(r\.flood_status_source\)\?'#4169E1':'#ffffff';L\.circleMarker\(\[r\.latitude,r\.longitude\],\{radius: 1\.5,fillColor:c,color:'#333',weight:0\.5,fillOpacity:1\}\)"

# Notice I increased radius to 3 to act more like a heatmap point.
new_marker_logic = r"let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');L.circleMarker([r.latitude,r.longitude],{radius: 2.5,fillColor:c,color:'#333',weight:0.5,fillOpacity:1})"

content = re.sub(old_marker_logic, new_marker_logic, content)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed map")
