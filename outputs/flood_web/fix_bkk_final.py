import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Move failed function
js = js.replace("function finishRender(){\n renderSourceStatus();\n function failed(name) { return DATA.sourceStatus[name]?.status==='error'; }", "function failed(name) { return DATA.sourceStatus[name]?.status==='error'; }\nfunction finishRender(){\n renderSourceStatus();")

# 2. Fix ID
js = js.replace("$('bkkAffectedHouseholds').textContent", "$('vulHouseholds').textContent")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
