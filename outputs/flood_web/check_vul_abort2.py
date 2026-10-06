import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("if (!vulData.length || failed('Vulnerable_group')) {", "console.log('vulData len:', vulData.length, 'failed:', failed('Vulnerable_group'), 'state.district:', state.district); if (!vulData.length || failed('Vulnerable_group')) {")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
