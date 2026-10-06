import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add scroll to sideBody
html = html.replace('id="sideBody" class="panel-body"', 'id="sideBody" class="panel-body" style="max-height: 510px; overflow-y: auto; padding-right: 12px;"')

# Ensure the track is visible
# Let's adjust padding slightly if needed
html = html.replace('.panel-body{padding:4px 22px 20px}', '.panel-body{padding:4px 22px 20px}')

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added scrollbar")
