import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current style:
# return {className:'national-province',color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:false};
old_style = "return {className:'national-province',color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:false};"
new_style = "return {className:'national-province',color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12};"

if old_style in html:
    html = html.replace(old_style, new_style)
    print("Updated province style to include light fill")
else:
    print("Could not find the style pattern.")
    # fallback regex
    fallback_old = r"className:'national-province'.*?fill:false\}"
    fallback_new = r"className:'national-province',color:householdBorderColor(n),weight:n>0?2.5:.8,opacity:n>0?1:.5,dashArray:'4 4',fill:n>0,fillColor:householdBorderColor(n),fillOpacity:0.12}"
    html = re.sub(fallback_old, fallback_new, html)
    print("Used regex fallback")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)

