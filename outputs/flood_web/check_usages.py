import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    for i, line in enumerate(html.split('\n')):
        if "$('quality')" in line or "$('actions')" in line:
            print(f"Line {i+1}: {line[:120]}")
