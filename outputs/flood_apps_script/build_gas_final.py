import re, shutil

# 1. Read files
with open('outputs/flood_web/thai_provinces.json', 'r', encoding='utf-8') as f:
    prov_geo = f.read()
with open('outputs/flood_web/bkk_districts.geojson', 'r', encoding='utf-8') as f:
    bkk_geo = f.read()
with open('outputs/flood_web/regions.geojson', 'r', encoding='utf-8') as f:
    reg_geo = f.read()
with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. Write GeoJSON HTMLs
with open('outputs/flood_apps_script/GeoJSON.html', 'w', encoding='utf-8') as f:
    f.write("<script>window.PROVINCES_GEOJSON = " + prov_geo + ";</script>")
with open('outputs/flood_apps_script/BkkGeoJSON.html', 'w', encoding='utf-8') as f:
    f.write("<script>window.BKK_DISTRICTS_GEOJSON = " + bkk_geo + ";</script>")
with open('outputs/flood_apps_script/RegionsGeoJSON.html', 'w', encoding='utf-8') as f:
    f.write("<script>window.HEALTH_REGIONS_GEOJSON = " + reg_geo + ";</script>")

# 3. Process Index.html
# Remove the fetch for thai_provinces
html = re.sub(r"const mapResponse=await fetch\('/thai_provinces\.json'\);.*?catch\(e\) \{ window\.PROVINCES_GEOJSON=null; \}", "} catch(e) {}", html, flags=re.DOTALL)
# Remove the fetch for bkk_districts
html = re.sub(r"const districtResponse=await fetch\('/bkk_districts\.geojson'\);.*?catch\(e\) \{ window\.BKK_DISTRICTS_GEOJSON=null; \}", "} catch(e) {}", html, flags=re.DOTALL)
# Remove the fetch for regions
html = re.sub(r"try\{const res=await fetch\('/regions\.geojson'\);.*?catch\(e\)\{window\.HEALTH_REGIONS_GEOJSON=null\}", "", html, flags=re.DOTALL)

# Inject HtmlService tags at the very end, right before </body>
injections = """
<?!= HtmlService.createHtmlOutputFromFile('GeoJSON').getContent(); ?>
<?!= HtmlService.createHtmlOutputFromFile('BkkGeoJSON').getContent(); ?>
<?!= HtmlService.createHtmlOutputFromFile('RegionsGeoJSON').getContent(); ?>
"""
html = html.replace("</body>", injections + "\n</body>")

# Replace `/api/data` fetch with `google.script.run`
old_load = """  async function load(){
   try{
    $('lastUpdate').textContent='กำลังโหลดข้อมูล...';
    const res=await fetch('/api/data');
    if(!res.ok) throw new Error('HTTP '+res.status);
    const data=await res.json();
    if(data.error) throw new Error(data.error);
    DATA=data;
    if(!state.date && DATA.disasters.length){
      state.date = uniq(DATA.disasters.map(r=>r.Report_Date.slice(0,10))).sort().at(-1);
    }
    render();
   }catch(err){
    $('lastUpdate').textContent='โหลดข้อมูลไม่สำเร็จ: '+err.message;
    console.error(err);
   }
  }"""

new_load = """  function load() {
    $('lastUpdate').textContent='กำลังโหลดข้อมูล...';
    google.script.run.withSuccessHandler(function(data) {
      if(data.error) {
        $('lastUpdate').textContent='โหลดข้อมูลไม่สำเร็จ: '+data.error;
        return;
      }
      DATA=data;
      if(!state.date && DATA.disasters.length){
        state.date = uniq(DATA.disasters.map(r=>r.Report_Date.slice(0,10))).sort().at(-1);
      }
      render();
    }).withFailureHandler(function(err) {
      $('lastUpdate').textContent='โหลดข้อมูลไม่สำเร็จ: '+err.message;
      console.error(err);
    }).readData();
  }"""

if old_load in html:
    html = html.replace(old_load, new_load)
else:
    # Use regex if spacing differs
    html = re.sub(r"async function load\(\)\s*\{.*?catch\(err\)\{.*?\}\s*\}", new_load, html, flags=re.DOTALL)

with open('outputs/flood_apps_script/Index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("GAS files rebuilt successfully!")
