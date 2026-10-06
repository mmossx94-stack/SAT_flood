import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("if(bkk) {")
    end_idx = js.find("}", idx + 500)
    print(js[end_idx:end_idx+600])
