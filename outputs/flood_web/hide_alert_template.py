import sys

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<div id="alert" class="alert"></div>', '<div id="alert" class="alert" style="display:none;"></div>')

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
