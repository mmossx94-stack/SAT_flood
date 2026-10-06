import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update header 'แนวโน้ม' to 'น้ำ'
old_h = "const h=['จังหวัด','อำเภอ','ตำบล','ครัวเรือน','เสียชีวิต','แนวโน้ม'];"
new_h = "const h=['จังหวัด','อำเภอ','ตำบล','ครัวเรือน','เสียชีวิต','น้ำ'];"
if old_h in html:
    html = html.replace(old_h, new_h)
    print("Updated header to 'น้ำ'")

# 2. Update the td rendering for the trend badge
# old: <td style="padding:8px 4px;">${badge(x.Water_Level_Trend,x.Water_Level_Trend==='เพิ่มขึ้น'?'warn':x.Water_Level_Trend==='ลดลง'?'good':'')}</td>
old_td = "<td style=\"padding:8px 4px;\">${badge(x.Water_Level_Trend,x.Water_Level_Trend==='เพิ่มขึ้น'?'warn':x.Water_Level_Trend==='ลดลง'?'good':'')}</td>"
new_td = "<td style=\"padding:8px 4px;\"><span class=\"badge\" style=\"${x.Water_Level_Trend==='เพิ่มขึ้น'?'background:#082f6b;color:#fff':x.Water_Level_Trend==='ทรงตัว'?'background:#3b82f6;color:#fff':x.Water_Level_Trend==='ลดลง'?'background:#93c5fd;color:#082f6b':'background:#e2e8f0;color:#64748b'}\">${esc(x.Water_Level_Trend)}</span></td>"

if old_td in html:
    html = html.replace(old_td, new_td)
    print("Updated trend badge colors")
else:
    print("Could not find the trend td")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
