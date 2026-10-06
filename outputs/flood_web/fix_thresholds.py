import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update thresholds in JS
html = html.replace("if (households >= 100000) { color = '#c85850'; fillOpacity = 0.5; } // Red", "if (households >= 100000) { color = '#800000'; fillOpacity = 0.85; } // Dark Red")
html = html.replace("else if (households >= 10000) { color = '#d57b4a'; fillOpacity = 0.5; } // Orange", "else if (households >= 10000) { color = '#ea3c24'; fillOpacity = 0.85; } // Red-Orange")
html = html.replace("else if (households >= 1000) { color = '#d5a34a'; fillOpacity = 0.5; } // Yellow", "else if (households >= 1000) { color = '#f3b052'; fillOpacity = 0.85; } // Yellow-Orange")
html = html.replace("else if (households > 0) { color = '#087873'; fillOpacity = 0.5; } // Green", "else if (households >= 1) { color = '#f9e79f'; fillOpacity = 0.85; } // Light Yellow")

# 2. Add legend
old_legend = '<div class="map-legend"><span><i class="dot" style="background:#00008B; border: 1px solid #333"></i>วิกฤติ / ล้นตลิ่ง (ข้อมูลสด)</span><span><i class="dot" style="background:#4169E1; border: 1px solid #333"></i>เตือนภัย / เฝ้าระวัง</span><span><i class="dot" style="background:#75858b"></i>ข้อมูลเก่า / เวลาไม่ผ่านเกณฑ์</span><span><i class="dot" style="background:#ffffff; border: 1px solid #333"></i>ศูนย์พักพิง / สถานีปกติ</span></div>'
new_legend = old_legend + '<div class="map-legend" style="padding-top:0"><span><i class="dot" style="background:#800000; border-radius:3px"></i>มากกว่า 100,000 หลัง</span><span><i class="dot" style="background:#ea3c24; border-radius:3px"></i>10,000 - 99,999 หลัง</span><span><i class="dot" style="background:#f3b052; border-radius:3px"></i>1,000 - 9,999 หลัง</span><span><i class="dot" style="background:#f9e79f; border-radius:3px"></i>1 - 999 หลัง</span></div>'

html = html.replace(old_legend, new_legend)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated thresholds and legend")
