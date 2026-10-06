import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("renderAreas(reports, allowed);")
    if idx != -1:
        print(js[idx-200:idx+200])
