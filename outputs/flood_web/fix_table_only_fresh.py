import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# Modify renderStations to filter out old data before sorting
old_render = "function renderStations(){const rows=currentStations.sort((a,b)=>{"
new_render = "function renderStations(){const rows=currentStations.filter(r=>quality(r)!=='ข้อมูลเก่าเกิน 24 ชั่วโมง').sort((a,b)=>{"

js = js.replace(old_render, new_render)

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
