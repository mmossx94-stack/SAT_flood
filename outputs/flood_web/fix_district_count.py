import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current: <td style="padding:8px 4px;max-width:120px;overflow:hidden;text-overflow:ellipsis;" title="${esc(x.District_Names||x.Affected_Districts_Count||'-')}">${esc(x.District_Names||x.Affected_Districts_Count||'-')}</td>
old_td = '<td style="padding:8px 4px;max-width:120px;overflow:hidden;text-overflow:ellipsis;" title="${esc(x.District_Names||x.Affected_Districts_Count||\'-\')}">${esc(x.District_Names||x.Affected_Districts_Count||\'-\')}</td>'
new_td = '<td style="padding:8px 4px;text-align:right">${esc(x.Affected_Districts_Count||\'-\')}</td>'

if old_td in html:
    html = html.replace(old_td, new_td)
    print("Updated District column to show count instead of names")
else:
    print("Could not find the district td")

# Also update the header alignment for อำเภอ (index 1 is now aligned right)
old_th = '<th style="padding:8px 4px;${i>=2&&i<=4?\'text-align:right\':\'\'}">${x}</th>'
new_th = '<th style="padding:8px 4px;${i>=1&&i<=4?\'text-align:right\':\'\'}">${x}</th>'
if old_th in html:
    html = html.replace(old_th, new_th)
    print("Updated header alignment")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
