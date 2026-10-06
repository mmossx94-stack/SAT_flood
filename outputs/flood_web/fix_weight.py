import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current: color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12
old_style = "color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12"
new_style = "color:householdBorderColor(n),weight:n>0?3.5:1.2,opacity:n>0?1:.5,fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12"

if old_style in html:
    html = html.replace(old_style, new_style)
    print("Updated line thickness")
else:
    print("Could not find the style pattern.")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
