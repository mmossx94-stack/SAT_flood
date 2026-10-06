import sys, re
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# find all panels that have a table-wrap
for panel in html.split('<section class="panel"'):
    if 'class="table-wrap"' in panel:
        print("PANEL:", panel[:200])
