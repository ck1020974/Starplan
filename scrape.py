import urllib.request
import re

url = 'https://www.cac.edu.tw/star115/Classification_BriefForm.php'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
        try:
            html = html.decode('utf-8')
        except:
            html = html.decode('big5', errors='ignore')
        
    with open('source.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Try to find PDF links
    pdf_links = re.findall(r'href=[\'"]?([^\'" >]+?\.pdf)', html, re.IGNORECASE)
    print("Found PDF links directly:", pdf_links)
    
    # Also find links with "pdf" in the href or text
    all_links = re.findall(r'<a[^>]+href=[\'"]?([^\'" >]+)[\'"]?[^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
    pdf_related_links = [l for l in all_links if 'pdf' in l[0].lower() or 'pdf' in l[1].lower()]
    print("Found PDF related links:")
    for l in set(pdf_related_links):
        print(f"URL: {l[0]}")
        print(f"Text: {l[1].strip()}")
        print("---")
        
except Exception as e:
    print("Error:", e)
