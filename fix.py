import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'layer\.bindTooltip\(<b></b>.*?;\s*', 'layer.bindTooltip(`<b>${prov}</b><br>ผลกระทบ: ${fmt(households)} ครัวเรือน`);\n            ', html)
html = html.replace('layer.bindTooltip(<b></b>);', 'layer.bindTooltip(`<b>${prov}</b>`);')

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
