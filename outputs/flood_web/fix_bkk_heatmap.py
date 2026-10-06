import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_bkk_heat = "gradient:{0.0:'#3b82f6',0.3:'#22c55e',0.55:'#facc15',0.75:'#f97316',1.0:'#9333ea'}"
new_bkk_heat = "gradient:{.15:'#93c5fd',.4:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}"

if old_bkk_heat in html:
    html = html.replace(old_bkk_heat, new_bkk_heat)
    print("Replaced BKK heatmap gradient")
else:
    print("Could not find BKK heatmap gradient string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
