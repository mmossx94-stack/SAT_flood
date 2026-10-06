import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    for i, line in enumerate(html.split('\n')):
        if "classList.toggle('hidden'" in line:
            print(f"Line {i+1}: {line}")
