import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find("renderAreas(); paginateTables();requestAnimationFrame(updateTableHints);")
    print(js[start-300:start+300])
