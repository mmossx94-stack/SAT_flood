import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

start = html.find('<section class="panel"><div class="panel-head"><div><h2>กลุ่มเปราะบาง')
end = html.find('</section>', start) + 10
vul_block = html[start:end]

start2 = html.find('<div class="section-title"><h2 id="areaTitle">')
end2 = html.find('</section>', start2) + 10
area_block = html[start2:end2]

between = html[end:start2]
print("BETWEEN:")
print(repr(between))
