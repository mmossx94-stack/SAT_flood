import re

# 1. Read bkk_districts.geojson
with open('outputs/flood_web/bkk_districts.geojson', 'r', encoding='utf-8') as f:
    bkk_geojson = f.read()

with open('outputs/flood_apps_script/BkkGeoJSON.html', 'w', encoding='utf-8') as f:
    f.write("<script>window.BKK_DISTRICTS_GEOJSON = " + bkk_geojson + ";</script>")

# 2. Update Index.html to embed BkkGeoJSON.html and remove fetch
with open('outputs/flood_apps_script/Index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove fetch for bkk_districts
fetch_str = "const districtResponse=await fetch('/bkk_districts.geojson');window.BKK_DISTRICTS_GEOJSON=districtResponse.ok?await districtResponse.json():null;}catch(e){window.BKK_DISTRICTS_GEOJSON=null;}"
html = html.replace(fetch_str, "}catch(e){}") # keep the catch block valid just in case
# Or safer, replace it completely using regex:
html = re.sub(r"const districtResponse=await fetch\('/bkk_districts\.geojson'\);.*?catch\(e\)\s*\{\s*window\.BKK_DISTRICTS_GEOJSON=null;\s*\}", "", html)

# Also need to inject BkkGeoJSON.html alongside GeoJSON.html
bkk_injection = "<?!= HtmlService.createHtmlOutputFromFile('BkkGeoJSON').getContent(); ?>"
# Find the previous injection and put it next to it
html = html.replace("<?!= HtmlService.createHtmlOutputFromFile('GeoJSON').getContent(); ?>", "<?!= HtmlService.createHtmlOutputFromFile('GeoJSON').getContent(); ?>\n" + bkk_injection)

with open('outputs/flood_apps_script/Index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated GAS files for BkkGeoJSON")
