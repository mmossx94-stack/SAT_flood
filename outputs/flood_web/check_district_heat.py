import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find("if(window.L && L.heatLayer){")
    print(js[start:start+1200])
