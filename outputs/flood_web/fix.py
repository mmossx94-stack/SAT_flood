import sys

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken tooltips
html = html.replace('layer.bindTooltip(<b></b><br>ผลกระทบ:  ครัวเรือน);', 'layer.bindTooltip(<b>\</b><br>ผลกระทบ: \ ครัวเรือน);')
html = html.replace('layer.bindTooltip(<b></b>);', 'layer.bindTooltip(<b>\</b>);')

# There might be some broken encoded strings, let's just restore the whole JS logic properly.
