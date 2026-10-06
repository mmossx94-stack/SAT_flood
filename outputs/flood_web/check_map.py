import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    
idx = js.find("if(bkk){")
if idx > -1:
    idx2 = js.find("map.", idx)
    print(js[idx2-100:idx2+200])
