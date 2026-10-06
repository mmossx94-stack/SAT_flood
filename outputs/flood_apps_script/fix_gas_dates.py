with open('outputs/flood_apps_script/Code.gs', 'r', encoding='utf-8') as f:
    content = f.read()

old_loop = """    headers.forEach((header, i) => {
      // Format dates properly
      if (row[i] instanceof Date) {
        // Adjust to GMT+7 string
        obj[header] = Utilities.formatDate(row[i], "GMT+07:00", "yyyy-MM-dd'T'HH:mm:ssXXX");
      } else {
        obj[header] = row[i];
      }
    });"""

new_loop = """    headers.forEach((header, i) => {
      let val = row[i];
      if (val instanceof Date) {
        obj[header] = Utilities.formatDate(val, "GMT+07:00", "yyyy-MM-dd'T'HH:mm:ssXXX");
      } else if (typeof val === 'string' && /^\d{1,2}\/\d{1,2}\/\d{4}/.test(val.trim())) {
        // Handle Thai string dates like "03/10/2569 03:15"
        let m = val.trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?/);
        if (m) {
          let y = parseInt(m[3], 10);
          if (y > 2500) y -= 543; // Convert Buddhist to Gregorian
          let d = m[1].padStart(2, '0');
          let mth = m[2].padStart(2, '0');
          let h = (m[4] || '0').padStart(2, '0');
          let mn = (m[5] || '0').padStart(2, '0');
          let s = (m[6] || '0').padStart(2, '0');
          obj[header] = `${y}-${mth}-${d}T${h}:${mn}:${s}+07:00`;
        } else {
          obj[header] = val;
        }
      } else {
        obj[header] = val;
      }
    });"""

content = content.replace(old_loop, new_loop)
with open('outputs/flood_apps_script/Code.gs', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed GAS dates")
