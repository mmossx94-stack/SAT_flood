import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

old_alert = "$('alert').textContent=bkk?`สถานีคลองในพื้นที่เลือกมีข้อมูลเก่า ${fmt(stale.length)} จาก ${fmt(currentStations.length)} แห่ง ณ เวลาอ่านข้อมูล — ตรวจเวลาวัดรายสถานีก่อนใช้งาน`:`ข้อมูล ณ เวลาอ่านข้อมูล: ${fmt(stale.length)} สถานีเกิน 24 ชั่วโมง และ ${fmt(future.length)} สถานีมีเวลาตรวจวัดอยู่ในอนาคต จึงไม่รวมในยอดสถานีวิกฤติ / ล้นตลิ่งข้อมูลสด`;"
new_alert = "$('alert').style.display='none';"
js = js.replace(old_alert, new_alert)

# Also ensure that if there's an error, it is shown
old_catch = "document.getElementById('alert').textContent=error.message+' — รีเฟรชเพื่อลองใหม่';"
new_catch = "document.getElementById('alert').style.display='block';document.getElementById('alert').textContent=error.message+' — รีเฟรชเพื่อลองใหม่';"
js = js.replace(old_catch, new_catch)

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
