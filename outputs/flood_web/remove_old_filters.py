import re, sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# The user plan: "รวมช่องค้นหาและสถานะเดิมของตารางสถานีน้ำเข้าในแผงเดียวกับตัวกรองใหม่ ย้ายตัวเลือกเรียงลำดับตารางจังหวัดเข้าแผงด้วย"
# So I should remove old .table-tools in template.html

# Look for <div class="table-tools"> ... </div> in the HTML.
parts = html.split('<div class="table-tools">')
if len(parts) > 1:
    new_html = parts[0]
    for part in parts[1:]:
        # Find the closing </div> of table-tools
        end_idx = part.find('</div>')
        new_html += part[end_idx+6:]
    print("Found and removed", len(parts)-1, "table-tools blocks.")
    with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
        f.write(new_html)
else:
    print("No table-tools found.")
