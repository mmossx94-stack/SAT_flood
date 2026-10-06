import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("renderAreas")
    if idx == -1:
        print("renderAreas not found at all!")
    else:
        print(js[idx:idx+1500])
