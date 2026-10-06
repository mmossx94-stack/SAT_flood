import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

dedup_code = """
function indexSources(){
    for(const [name,key] of Object.entries(SOURCES))for(const row of DATA[key])rowSources.set(row,name);
    
    // Deduplicate stations by name keeping the latest
    function dedup(arr) {
        const map = new Map();
        for (const r of arr) {
            const key = r.station_name;
            if (!key) continue;
            if (!map.has(key)) {
                map.set(key, r);
            } else {
                const existing = map.get(key);
                const t1 = new Date(r.observed_at_th || r.updated_at_source || r.Ingested_At).getTime() || 0;
                const t2 = new Date(existing.observed_at_th || existing.updated_at_source || existing.Ingested_At).getTime() || 0;
                if (t1 > t2) {
                    map.set(key, r);
                }
            }
        }
        return Array.from(map.values());
    }
    if (DATA.stations) DATA.stations = dedup(DATA.stations);
    if (DATA.bkkStations) DATA.bkkStations = dedup(DATA.bkkStations);
}
"""

js = js.replace("function indexSources(){for(const [name,key] of Object.entries(SOURCES))for(const row of DATA[key])rowSources.set(row,name)}", dedup_code.strip())

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
