import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_status = "const WATER_STATUS={ล้นตลิ่ง:{rank:5,color:'#581c87'},วิกฤต:{rank:4,color:'#9333ea'},เตือนภัย:{rank:3,color:'#f97316'},เฝ้าระวัง:{rank:2,color:'#facc15'},ปกติ:{rank:1,color:'#22c55e'}};"
new_status = "const WATER_STATUS={ล้นตลิ่ง:{rank:5,color:'#991b1b'},วิกฤต:{rank:4,color:'#dc2626'},เตือนภัย:{rank:3,color:'#f97316'},เฝ้าระวัง:{rank:2,color:'#facc15'},ปกติ:{rank:1,color:'#22c55e'}};"

if old_status in html:
    html = html.replace(old_status, new_status)
    print("Replaced WATER_STATUS colors")
else:
    print("Could not find WATER_STATUS string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
