import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    
idx = html.find("barChart")
print(html[idx:idx+1500])

idx2 = html.find("$('barChart')")
if idx2 != -1:
    print("\n--- RENDER ---")
    print(html[idx2-50:idx2+1000])
