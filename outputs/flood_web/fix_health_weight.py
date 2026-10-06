import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current: className:'health-region-outline',color:'#475569',weight:1.5,opacity:1,fill:false
old_style = "className:'health-region-outline',color:'#475569',weight:1.5,opacity:1,fill:false"
new_style = "className:'health-region-outline',color:'#475569',weight:0.8,opacity:1,fill:false"

if old_style in html:
    html = html.replace(old_style, new_style)
    print("Updated health region line thickness to 0.8")
else:
    print("Could not find the style pattern.")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
