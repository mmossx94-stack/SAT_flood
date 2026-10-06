import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to find where the metrics are generated.
# metric('รายงาน ปภ. ผ่านเกณฑ์ 24 ชั่วโมง',fmt(reports.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').length)+' / '+fmt(reports.length))+metric('รายงาน ปภ. ไม่ทราบเวลาข้อมูล',fmt(reports.filter(r=>quality(r)==='ไม่ทราบเวลาข้อมูล').length))

old_code = "metric('รายงาน ปภ. ผ่านเกณฑ์ 24 ชั่วโมง',fmt(reports.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').length)+' / '+fmt(reports.length))+metric('รายงาน ปภ. ไม่ทราบเวลาข้อมูล',fmt(reports.filter(r=>quality(r)==='ไม่ทราบเวลาข้อมูล').length))"
new_code = "metric('รายงาน ปภ. ผ่านเกณฑ์ 24 ชั่วโมง',fmt(reports.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').length)+' / '+fmt(reports.length))+metric('รายงาน ปภ. ไม่ทราบเวลาข้อมูล',fmt(reports.filter(r=>quality(r)==='ไม่ทราบเวลาข้อมูล').length))+metric('เวลานำเข้าข้อมูล ปภ.', time(reports.map(r=>r.Ingested_At).filter(x=>x).sort().pop()))"

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Added DDPM time metric")
else:
    print("Could not find metric code")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
