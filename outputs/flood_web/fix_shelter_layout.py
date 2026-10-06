import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = '<div class="split-layout hidden" id="shelterMapPanel">'
new_str = '<div class="hidden" id="shelterMapPanel" style="display: flex; gap: 24px; align-items: stretch; margin-bottom: 24px">'

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed layout class!")
else:
    print("Could not find old string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
