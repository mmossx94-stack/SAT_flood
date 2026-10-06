import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Revert panes z-index so Health Region is on top
old_panes = "map.getPane('nationalBoundaries').style.zIndex=650;map.createPane('healthRegionBoundaries');map.getPane('healthRegionBoundaries').style.zIndex=450"
new_panes = "map.getPane('nationalBoundaries').style.zIndex=450;map.createPane('healthRegionBoundaries');map.getPane('healthRegionBoundaries').style.zIndex=650"

if old_panes in html:
    html = html.replace(old_panes, new_panes)
    print("Swapped panes")

# 2. Revert province style to solid (remove dashArray)
old_prov = "color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12"
new_prov = "color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12"

if old_prov in html:
    html = html.replace(old_prov, new_prov)
    print("Restored solid line for provinces")

# 3. Revert the legend CSS to solid
old_css = ".border-key i{width:26px;border-top:3px dashed;display:inline-block}"
new_css = ".border-key i{width:26px;border-top:3px solid;display:inline-block}"

if old_css in html:
    html = html.replace(old_css, new_css)
    print("Restored legend CSS to solid")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
