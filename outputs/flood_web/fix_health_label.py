import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_label = '<span style="display:inline-block;width:36px;height:2px;background:#475569" aria-hidden="true"></span>'
new_label = '<span style="display:inline-block;width:36px;height:1px;background:#475569" aria-hidden="true"></span>'

if old_label in html:
    html = html.replace(old_label, new_label)
    print("Updated label icon thickness")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
