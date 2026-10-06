import sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("dashboard.js:", 'dashboard.js' in html)
    print("dashboard.css:", 'dashboard.css' in html)
    print("data-model.js:", 'data-model.js' in html)
