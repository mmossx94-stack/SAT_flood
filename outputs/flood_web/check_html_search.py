import sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    import re
    matches = re.findall(r'.{0,50}ค้นหา.{0,50}', html)
    for m in matches: print(m)
