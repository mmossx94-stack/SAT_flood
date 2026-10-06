import json
import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace data fetching logic
fetch_regex = r"async function load\(\)\{try\{const res=await fetch\('/api/data'\);DATA=await res\.json\(\);(.*?)const resGeo=await fetch\('/thai_provinces\.json'\);window\.PROVINCES_GEOJSON=resGeo\.ok\?await resGeo\.json\(\):null;catch\(e\)\{window\.PROVINCES_GEOJSON=null\}"
# Wait, let's just replace the exact lines
html = html.replace("const res=await fetch('/api/data');DATA=await res.json();", "DATA = JSON.parse(await new Promise((resolve, reject) => google.script.run.withSuccessHandler(resolve).withFailureHandler(reject).getDashboardData()));")

# Remove the fetch for GeoJSON since we will embed it
html = re.sub(r"const resGeo=await fetch\('/thai_provinces\.json'\);\s*window\.PROVINCES_GEOJSON=resGeo\.ok\?await resGeo\.json\(\):null;\s*\}catch\(e\)\{\s*window\.PROVINCES_GEOJSON=null;\s*\}", "", html)
# Let's just use string replace if it's there
html = html.replace("const resGeo=await fetch('/thai_provinces.json');window.PROVINCES_GEOJSON=resGeo.ok?await resGeo.json():null;}catch(e){window.PROVINCES_GEOJSON=null}", "")

# We will inject the GeoJSON before the load script
script_start = "<script>"
injection = "<?!= HtmlService.createHtmlOutputFromFile('GeoJSON').getContent(); ?>"
html = html.replace(script_start, script_start + "\n" + injection + "\n", 1)

with open('outputs/flood_apps_script/Index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
# Now write GeoJSON.html
with open('outputs/flood_web/thai_provinces.json', 'r', encoding='utf-8') as f:
    geojson = f.read()

with open('outputs/flood_apps_script/GeoJSON.html', 'w', encoding='utf-8') as f:
    f.write("<script>window.PROVINCES_GEOJSON = " + geojson + ";</script>")

print("Generated Index.html and GeoJSON.html")
