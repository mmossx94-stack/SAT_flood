import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find("function renderAreas()")
    end = js.find("function renderStations()", start)
    print(js[start:end])
