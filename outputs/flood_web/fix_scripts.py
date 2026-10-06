import re

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove misplaced script tag before <!doctype html>
html = re.sub(r'^<script[^>]+></script>', '', html.lstrip())
html = html.strip()

# Find where the single <script> tag is (the main JS block)
main_script_idx = html.find("<script>")

# Check if Leaflet JS CDN is already in there
if "leaflet@1.9.4/dist/leaflet.js" not in html:
    leaflet_tags = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>\n'
else:
    # Just add heat after existing leaflet.js script tag
    existing = re.search(r'<script src="[^"]*leaflet[^"]*leaflet\.js"[^>]*></script>', html)
    if existing:
        insert_at = existing.end()
        heat_tag = '\n<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>'
        html = html[:insert_at] + heat_tag + html[insert_at:]
        print("Added heat after leaflet.js")
        with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Done")
        exit(0)

# Insert before main <script> block
html = html[:main_script_idx] + leaflet_tags + html[main_script_idx:]
print("Inserted script tags before main script block")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
