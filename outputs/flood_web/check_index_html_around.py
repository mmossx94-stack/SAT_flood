import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/index.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("--- TableSort ---")
    print(html[9100:9400])
    print("--- Search & Status ---")
    print(html[12700:13200])
