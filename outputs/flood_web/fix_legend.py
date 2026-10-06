import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_css = ".border-key i{width:26px;border-top:3px solid;display:inline-block}"
new_css = ".border-key i{width:26px;border-top:3px dashed;display:inline-block}"

html = html.replace(old_css, new_css)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Fixed legend CSS")
