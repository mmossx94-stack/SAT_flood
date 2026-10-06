import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("$('areaTable').innerHTML=")
    end = js.find("];}}", idx)
    print("Start:", idx)
    print("End:", end)
    print(js[idx:idx+100])
    print(js[end-100:end+4])
