import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = "    r?quality(r):'-'\n  ])];\n}"
new_str = "    r?quality(r):'-'\n  ])];\n}}"

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed missing brace!")
else:
    # maybe it was minified
    old_str2 = "r?quality(r):'-'])];}"
    new_str2 = "r?quality(r):'-'])];}}"
    if old_str2 in html:
        html = html.replace(old_str2, new_str2)
        print("Fixed missing brace (minified)!")
    else:
        print("Could not find brace to fix")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
