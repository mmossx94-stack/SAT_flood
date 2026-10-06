import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Swap z-index for panes
old_panes = "map.getPane('nationalBoundaries').style.zIndex=450;map.createPane('healthRegionBoundaries');map.getPane('healthRegionBoundaries').style.zIndex=650"
new_panes = "map.getPane('nationalBoundaries').style.zIndex=650;map.createPane('healthRegionBoundaries');map.getPane('healthRegionBoundaries').style.zIndex=450"

if old_panes in html:
    html = html.replace(old_panes, new_panes)
else:
    print("Could not find pane setup")

# 2. Make health regions solid and thinner
old_health_style = "className:'health-region-outline',color:'#111111',weight:2.5,opacity:1,dashArray:'3 9',fill:false,lineCap:'butt'"
new_health_style = "className:'health-region-outline',color:'#475569',weight:1.5,opacity:1,fill:false"

if old_health_style in html:
    html = html.replace(old_health_style, new_health_style)
else:
    print("Could not find health region style")

# 3. Make household boundaries (province outline) dashed
old_prov_style = "color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,fill:false"
new_prov_style = "color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:false"

if old_prov_style in html:
    html = html.replace(old_prov_style, new_prov_style)
else:
    print("Could not find province style")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
