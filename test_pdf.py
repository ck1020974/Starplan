import pdfplumber
import os

pdf_path = r'c:\Users\李祐馨\Desktop\新增資料夾\PDFs\001_國立臺灣大學.pdf'

with open('pdf_output.txt', 'w', encoding='utf-8') as f:
    with pdfplumber.open(pdf_path) as pdf:
        f.write(f"Total pages: {len(pdf.pages)}\n")
        for i, page in enumerate(pdf.pages[:2]):
            f.write(f"\n--- Page {i+1} ---\n")
            text = page.extract_text()
            f.write(text[:1000] if text else "No text found")
            f.write("\n\n-- Tables --\n")
            tables = page.extract_tables()
            for t in tables:
                for row in t[:15]: # first 15 rows
                    f.write(str(row) + "\n")
