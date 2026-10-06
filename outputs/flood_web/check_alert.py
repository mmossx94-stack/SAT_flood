import sys, re
with open("outputs/flood_web/index.html", "r", encoding="utf-8") as f:
    html = f.read()
    match = re.search(r'<[^>]+id="alert"[^>]*>.*?</[^>]+>', html)
    print(match.group(0) if match else "Not found")
