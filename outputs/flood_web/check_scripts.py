import re
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
head_end = html.find("</head>")
head = html[:head_end]
for m in re.finditer(r"<script[^>]*>", head):
    print(m.start(), repr(m.group(0)[:120]))
print("---")
for m in re.finditer(r"leaflet[a-zA-Z0-9./\-@_]{0,40}\.js", html):
    print(m.start(), m.group(0))
