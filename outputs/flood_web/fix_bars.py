import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the bars function
old_bars = "function bars(rows){let max=Math.max(...rows.map(r=>r.value),1);return rows.map(r=>`<div class=\"barrow\"><button data-province=\"${esc(r.name)}\" title=\"ดูจังหวัด ${esc(r.name)}\">${esc(r.name)}</button><div class=\"bartrack\"><div class=\"bar\" style=\"width:${r.value/max*100}%\"></div></div><strong>${fmt(r.value)}</strong></div>`).join('')||'<p class=\"empty\">ไม่มีรายงานในขอบเขตที่เลือก</p>'}"
new_bars = "function bars(rows){let max=Math.max(...rows.map(r=>r.value),1);return rows.map(r=>{let color='#087873';if(r.value>=100000)color='#800000';else if(r.value>=10000)color='#ea3c24';else if(r.value>=1000)color='#f3b052';else if(r.value>=1)color='#f9e79f';return `<div class=\"barrow\"><button data-province=\"${esc(r.name)}\" title=\"ดูจังหวัด ${esc(r.name)}\">${esc(r.name)}</button><div class=\"bartrack\"><div class=\"bar\" style=\"width:${r.value/max*100}%;background:${color}\"></div></div><strong>${fmt(r.value)}</strong></div>`}).join('')||'<p class=\"empty\">ไม่มีรายงานในขอบเขตที่เลือก</p>'}"
html = html.replace(old_bars, new_bars)

# 2. Update subtitle text
html = html.replace("8 อันดับตามรายงานในขอบเขตที่เลือก · หน่วย: ครัวเรือน", "ทุกอันดับตามรายงานในขอบเขตที่เลือก · หน่วย: ครัวเรือน")

# 3. Remove .slice(0,8)
html = html.replace(".slice(0,8).map", ".map")

# Update heights for the side panel so it scrolls properly if there are many provinces
# It already has <div class="table-wrap"> ? No, wait. The side panel doesn't have a max-height?
# Let's add max-height and overflow to the sideBody if it doesn't have it, or it will stretch the whole page.
# Actually, the page can just scroll, that's fine.

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated bars successfully")
