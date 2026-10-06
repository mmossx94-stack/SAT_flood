import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("const failed=name=>DATA.sourceStatus[name]?.status==='error';", "function failed(name) { return DATA.sourceStatus[name]?.status==='error'; }")
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
