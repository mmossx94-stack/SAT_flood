import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove district fill
old_district_style = r"className:'bkk-district',color:active\?'#334155':'#94a3b8',weight:state\.district===name\?2\.5:1,fillColor:summary\.color,fillOpacity:summary\.color==='transparent'\?0:active\?\.7:\.12"
new_district_style = r"className:'bkk-district',color:active?'#334155':'#94a3b8',weight:state.district===name?2.5:1,fillColor:'transparent',fillOpacity:0"

content = re.sub(old_district_style, new_district_style, content)

# 2. Make station dots look more like a heatmap (larger, no border, overlapping)
# Currently: {radius:8,fillColor:c,color:c==='transparent'?'transparent':'#000',weight:c==='transparent'?0:0.5,fillOpacity:c==='transparent'?0:0.8,opacity:c==='transparent'?0:0.8}
old_dot = r"\{radius:8,fillColor:c,color:c==='transparent'\?'transparent':'#000',weight:c==='transparent'\?0:0\.5,fillOpacity:c==='transparent'\?0:0\.8,opacity:c==='transparent'\?0:0\.8\}"
# New dot: {radius:12,fillColor:c,color:'transparent',weight:0,fillOpacity:c==='transparent'?0:0.6}
new_dot = "{radius:12,fillColor:c,color:'transparent',weight:0,fillOpacity:c==='transparent'?0:0.65}"

content = re.sub(old_dot, new_dot, content)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated district and station styles")
