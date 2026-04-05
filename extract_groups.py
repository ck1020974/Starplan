import json
import os
import glob
import pdfplumber

json_path = r'c:\Users\李祐馨\Desktop\新增資料夾\all_departments.json'
pdf_dir = r'c:\Users\李祐馨\Desktop\新增資料夾\PDFs'

# 1. Build a lookup dictionary: dept_code string -> department_group string
# Example: "00101" -> "第一類學群"
dept_groups = {}

pdf_files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
print(f"Found {len(pdf_files)} PDF files to process.")

for pdf_file in pdf_files:
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Ensure row has at least 3 columns to avoid index errors
                        if len(row) >= 3:
                            dept_code = row[0]
                            group_name = row[2]
                            
                            if dept_code and dept_code.isdigit() and len(dept_code) >= 5:
                                # Sometimes the text has newlines or spaces
                                group_name = group_name.replace('\n', '') if group_name else ""
                                dept_groups[dept_code.strip()] = group_name.strip()
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")

print(f"Successfully extracted {len(dept_groups)} department mappings.")

# 2. Update all_departments.json
with open(json_path, 'r', encoding='utf-8') as f:
    departments = json.load(f)

update_count = 0
for dept in departments:
    code = dept.get('dept_code', '')
    if code in dept_groups:
        dept['department_group'] = dept_groups[code]
        update_count += 1
    else:
        dept['department_group'] = "" # Default if not found

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(departments, f, ensure_ascii=False, indent=2)

print(f"Updated {update_count} out of {len(departments)} departments in JSON.")
