import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_apps_script/Index.html", "r", encoding="utf-8") as f:
    js = f.read()
    idx = js.find("function renderAreas")
    if idx != -1:
        # Check around the definition to see what calls it
        print("AROUND DEF:")
        print(js[max(0, idx-300):idx+300])
        
    call_idx = js.find("renderAreas(", idx + 50)
    if call_idx != -1:
        print("\n\nAROUND CALL:")
        print(js[call_idx-200:call_idx+200])
