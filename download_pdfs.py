import urllib.request
import re
import os
import time

html_path = 'source.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<td class="CNY_center">(\d+)</td><td>([^<]+)</td><td class=\'CNY_center\'><A href=\'(Classification_readfile\.php\?fileid=\d+)\'')
matches = pattern.findall(html)

base_url = 'https://www.cac.edu.tw/star115/'
output_dir = r'c:\Users\李祐馨\Desktop\新增資料夾\PDFs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Found {len(matches)} files to download.")

for school_id, school_name, link in matches:
    url = base_url + link
    filename = f"{school_id}_{school_name}.pdf"
    filepath = os.path.join(output_dir, filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filepath, 'wb') as out_f:
                out_f.write(response.read())
        time.sleep(0.5) # respect server limits
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Download complete.")
