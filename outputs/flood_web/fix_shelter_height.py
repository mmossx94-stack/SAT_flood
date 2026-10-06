import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = '<div id="shelterMap" class="map" aria-label="แผนที่ศูนย์พักพิง กรุงเทพมหานคร" style="flex: 1 1 auto; height: 100%;"></div>'
new_str = '<div id="shelterMap" class="map" aria-label="แผนที่ศูนย์พักพิง กรุงเทพมหานคร" style="min-height: 480px; flex: 1 1 auto; height: 100%;"></div>'

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed shelter map height")
else:
    print("Could not find old string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
