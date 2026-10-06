import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

start = html.find('<div class="detailgrid">')
end = html.find('<section class="panel"><div class="panel-head"><div><h2>รายละเอียดสถานีระดับน้ำ</h2>')

print("Start:", start)
print("End:", end)
print("Between:", repr(html[end-30:end]))
