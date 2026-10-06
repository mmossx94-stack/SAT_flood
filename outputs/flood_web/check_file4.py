import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    lines = js.splitlines()
    for i in range(35, 75):
        if i < len(lines):
            print(f"Line {i}: {lines[i][:150]}")
