import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    lines = js.split("\n")
    for i, line in enumerate(lines):
        if "$('search')" in line:
            print(f"Line {i+1}: {line.strip()}")
