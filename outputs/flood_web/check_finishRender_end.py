import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("function finishRender")
    end_idx = js.find("}", idx)
    print(js[idx+1000:idx+2500])
