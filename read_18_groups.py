import pdfplumber
import os

pdf_path = r'c:\Users\李祐馨\Desktop\新增資料夾\十八學群及其學類對照表.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # Print the text from the first few pages
    with open('18_groups_text.txt', 'w', encoding='utf-8') as f:
        for page in pdf.pages:
            f.write(page.extract_text() + "\n\n")
            
            tables = page.extract_tables()
            for t in tables:
                f.write(str(t) + "\n")
print("Extraction saved to 18_groups_text.txt")
