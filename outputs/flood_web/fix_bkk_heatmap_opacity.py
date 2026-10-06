import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_bkk_heat = "L.heatLayer(heatData,{radius:40,blur:20,maxZoom:14,max:0.6,minOpacity:0.5,gradient:{.15:'#93c5fd',.4:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}})"
new_bkk_heat = "L.heatLayer(heatData,{radius:40,blur:20,maxZoom:14,max:1.0,minOpacity:0.05,gradient:{.15:'#93c5fd',.4:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}})"

if old_bkk_heat in html:
    html = html.replace(old_bkk_heat, new_bkk_heat)
    print("Replaced BKK heatmap visual config")
else:
    print("Could not find old config")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
