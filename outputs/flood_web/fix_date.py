import re

with open('outputs/flood_web/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix normalize function to handle "DD/MM/YYYY HH:MM" where YYYY could be Buddhist (e.g. 2569)
# The current normalize block for dates:
old_date_block = """    if key in DATES:
        # Sheets stores this workbook's dates as ISO dates or Bangkok wall time.
        value = str(value).replace(' ', 'T', 1)
        value = re.sub(r'T(\d):', r'T0\1:', value)
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): value += 'T00:00:00'
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value): value += '+07:00'
        try: datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError: raise ValueError(f'รูปแบบวันที่ไม่รองรับในคอลัมน์ {key}')"""

new_date_block = """    if key in DATES:
        value = str(value).strip()
        # Handle DD/MM/YYYY or DD/MM/YYYY HH:MM (potentially Thai Buddhist year)
        m = re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?', value)
        if m:
            d, mth, y, h, mn, s = m.groups()
            y = int(y)
            if y > 2500: y -= 543  # Convert Buddhist to Gregorian
            value = f"{y:04d}-{int(mth):02d}-{int(d):02d}T{int(h or 0):02d}:{int(mn or 0):02d}:{int(s or 0):02d}+07:00"
        else:
            value = value.replace(' ', 'T', 1)
            value = re.sub(r'T(\d):', r'T0\1:', value)
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): value += 'T00:00:00'
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value): value += '+07:00'
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', value): value += ':00+07:00'
        try: datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError: raise ValueError(f'รูปแบบวันที่ไม่รองรับในคอลัมน์ {key}')"""

content = content.replace(old_date_block, new_date_block)

with open('outputs/flood_web/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated server.py to handle Thai dates")
