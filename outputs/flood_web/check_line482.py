import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    for i in range(475, 485):
        if i < len(lines):
            print(f"Line {i+1}: {lines[i]}")
