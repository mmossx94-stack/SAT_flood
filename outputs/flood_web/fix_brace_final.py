import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = "r?quality(r):'-'  ])];}"
new_str = "r?quality(r):'-'  ])];}}"

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed!")
else:
    print("Not found")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
