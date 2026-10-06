import urllib.request, csv, sys
sys.stdout.reconfigure(encoding="utf-8")

url = "https://docs.google.com/spreadsheets/d/1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4/export?format=csv&gid=0"
with urllib.request.urlopen(url) as response:
    content = response.read().decode("utf-8")
    reader = csv.reader(content.splitlines())
    rows = list(reader)
    print("Headers:", rows[0])
    for r in rows[1:10]:
        print(r)
