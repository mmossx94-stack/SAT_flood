import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    print("Total length:", len(js))
    # print lines around line 1
    lines = js.splitlines()
    for i, l in enumerate(lines):
        if "function render" in l:
            print("Line", i, ":", l[:100])
