with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    print("Length:", len(js))
    print("End of file:", js[-500:])
