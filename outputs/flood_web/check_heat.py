import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find("safeHeatLayer(")
    end = js.find(")", start)
    print("BKK:", js[start:end+20])
    
    start2 = js.find("safeHeatLayer(", end)
    end2 = js.find(")", start2)
    print("Nat:", js[start2:end2+20])
