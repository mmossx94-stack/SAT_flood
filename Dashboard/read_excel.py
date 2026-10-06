import pandas as pd

try:
    xl = pd.ExcelFile('รายงานสถานการณ์สาธารณภัยรายจังหวัด.xlsx')
    with open('excel_head.txt', 'w', encoding='utf-8') as f:
        f.write('Sheets: ' + str(xl.sheet_names) + '\n\n')
        for s in xl.sheet_names:
            f.write('==========================\n')
            f.write(f'Sheet: {s}\n')
            f.write(xl.parse(s).head().to_string() + '\n\n')
except Exception as e:
    with open('excel_head.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
