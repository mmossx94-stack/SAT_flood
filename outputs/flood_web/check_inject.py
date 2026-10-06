import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('const distStats=new Map();for(const r of currentStations)')
    print(html[max(0, idx-100):idx+50])
