import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

old_code = "card('เขตไม่มีศูนย์ตามตัวกรอง/เต็มหมด', noShelterOrFullDistricts, 'เขต', `จาก ${targetDistricts.length} เขต`);"
new_code = "card('เขตที่ไม่มีศูนย์พักพิง', noShelterOrFullDistricts, 'เขต', `จาก ${targetDistricts.length} เขต`);"

js = js.replace(old_code, new_code)

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
