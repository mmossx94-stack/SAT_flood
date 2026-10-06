import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make the label preview a solid line instead of dashed, and use the new color #475569
old_label = '<span style="display:inline-block;width:36px;height:3px;background:repeating-linear-gradient(to right,#111 0 3px,transparent 3px 12px)" aria-hidden="true"></span>'
new_label = '<span style="display:inline-block;width:36px;height:2px;background:#475569" aria-hidden="true"></span>'

html = html.replace(old_label, new_label)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated label")
