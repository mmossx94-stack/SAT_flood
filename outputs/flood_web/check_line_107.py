import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    lines = js.split('\n')
    print("\n".join(lines[100:115]))
