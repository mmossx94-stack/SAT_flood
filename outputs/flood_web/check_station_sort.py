import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find("let stRows = currentStations")
    print(html[idx:idx+400])
