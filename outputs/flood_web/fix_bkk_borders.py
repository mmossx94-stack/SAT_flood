import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current:
# return {className:'bkk-district',color:active?'#334155':'#94a3b8',weight:state.district===name?2.5:1,fillColor:summary.status?summary.color:'transparent',fillOpacity:summary.status?0.4:0}

old_style = "return {className:'bkk-district',color:active?'#334155':'#94a3b8',weight:state.district===name?2.5:1,fillColor:summary.status?summary.color:'transparent',fillOpacity:summary.status?0.4:0}"
new_style = "return {className:'bkk-district',color:summary.status?summary.color:(active?'#334155':'#94a3b8'),weight:summary.status?3:(state.district===name?2.5:1),fillColor:'transparent',fillOpacity:0}"

if old_style in html:
    html = html.replace(old_style, new_style)
    print("Replaced polygon styles")
else:
    print("Could not find old_style")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
