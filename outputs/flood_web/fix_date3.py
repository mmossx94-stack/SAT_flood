import re

with open('outputs/flood_web/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace normalize entirely
new_normalize = r"""def normalize(key, value):
    value = value.strip() if isinstance(value, str) else value
    if value is None or value == '': return None
    if key in NUMERIC:
        try:
            n = float(str(value).replace(',', ''))
            if not math.isfinite(n): return None
            return int(n) if n.is_integer() else n
        except (ValueError, TypeError): return None
    if key in DATES:
        value = str(value).strip()
        m = re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?', value)
        if m:
            d, mth, y, h, mn, s = m.groups()
            y = int(y)
            if y > 2500: y -= 543
            value = f"{y:04d}-{int(mth):02d}-{int(d):02d}T{int(h or 0):02d}:{int(mn or 0):02d}:{int(s or 0):02d}+07:00"
        else:
            value = value.replace(' ', 'T', 1)
            value = re.sub(r'T(\d):', r'T0\1:', value)
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): value += 'T00:00:00'
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value): value += '+07:00'
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', value): value += ':00+07:00'
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
            return value
        except ValueError:
            raise ValueError(f'Invalid date format in column {key}: {value}')
    return value
"""

start_idx = content.find('def normalize(key, value):')
end_idx = content.find('def parse_sheet')
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_normalize + '\n' + content[end_idx:]

with open('outputs/flood_web/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced normalize")
