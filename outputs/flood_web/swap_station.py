import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's see the order of sections:
# 1. <section class="panel"><div class="panel-head"><div><h2>กลุ่มเปราะบางเพื่อวางแผนรองรับ</h2>
# 2. <div class="detailgrid">
# 3. <div class="section-title" id="stationListTitle">

idx_vul = html.find('<h2>กลุ่มเปราะบางเพื่อวางแผนรองรับ</h2>')
idx_grid = html.find('<div class="detailgrid">')
idx_station = html.find('<div class="section-title" id="stationListTitle">')

if idx_station == -1:
    idx_station = html.find('<section class="panel"><div class="panel-head" style="flex-wrap:wrap;gap:12px"><div><h2>รายละเอียดสถานีระดับน้ำ</h2>')

print(f"Vul: {idx_vul}")
print(f"Grid: {idx_grid}")
print(f"Station: {idx_station}")
