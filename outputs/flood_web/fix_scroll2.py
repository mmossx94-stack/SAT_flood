import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The actual HTML has: <div class="panel-body" id="sideBody">
html = html.replace('<div class="panel-body" id="sideBody"></div>', '<div class="panel-body" id="sideBody" style="max-height: 520px; overflow-y: auto; padding-right: 12px;"></div>')

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Scrollbar added successfully")
