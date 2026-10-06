import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/server.py", "r", encoding="utf-8") as f:
    code = f.read()
    idx = code.find("def do_GET")
    print(code[idx:idx+1500])
