import json
from bs4 import BeautifulSoup

html_file = r'c:\Users\李祐馨\Desktop\新增資料夾\page.html'
json_file = r'c:\Users\李祐馨\Desktop\新增資料夾\all_departments.json'

with open(html_file, 'r', encoding='utf-16') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

uni_map = {}
# Find all rows in the table
rows = soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 3:
        # Expected structure: td1 = 代碼, td2 = 大學名稱
        code_td = cols[0]
        name_td = cols[1]
        
        c = code_td.get_text(strip=True)
        # e.g "001"
        if c.isdigit() and len(c) == 3:
            n = name_td.get_text(strip=True)
            uni_map[c] = n

print(f"Loaded {len(uni_map)} universities.")

# Update JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for dept in data:
    dcode = dept.get('dept_code', '')
    if len(dcode) >= 3:
        uni_code = dcode[:3]
        if uni_code in uni_map:
            dept['school_name'] = uni_map[uni_code]
        else:
            dept['school_name'] = "未知學校"

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Injected school names to JSON!")
