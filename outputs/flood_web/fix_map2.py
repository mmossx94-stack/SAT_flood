with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace National map logic:
old_nat = "let q=quality(r),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':['วิกฤติ','ล้นตลิ่ง'].includes(r.flood_status_source)?'#00008B':['เตือนภัย','เฝ้าระวัง'].includes(r.flood_status_source)?'#4169E1':'#ffffff';L.circleMarker([r.latitude,r.longitude],{radius: 1.5,fillColor:c,color:'#333',weight:0.5,fillOpacity:1})"
new_nat = "let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');L.circleMarker([r.latitude,r.longitude],{radius: 2.5,fillColor:c,color:'#333',weight:0.5,fillOpacity:1})"

if old_nat in content:
    content = content.replace(old_nat, new_nat)
    print("Replaced National map logic")
else:
    print("Could not find National map logic")

# Ensure BKK map logic is correct.
old_bkk = "let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');\n  L.circleMarker([r.latitude,r.longitude],{radius: 2.5,fillColor:c,color:'#fff',weight:0.5,fillOpacity:1})"

new_bkk = "let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');\n  L.circleMarker([r.latitude,r.longitude],{radius: 3,fillColor:c,color:'#fff',weight:0.8,fillOpacity:1})"

if old_bkk in content:
    content = content.replace(old_bkk, new_bkk)
    print("Replaced BKK map logic")
else:
    print("Could not find BKK map logic")

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
