import json
import ast

text_file = r'c:\Users\李祐馨\Desktop\新增資料夾\18_groups_text.txt'
json_file = r'c:\Users\李祐馨\Desktop\新增資料夾\all_departments.json'

category_map = {}
with open(text_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith("[['"):
            try:
                arr = ast.literal_eval(line)
                for item in arr:
                    if len(item) == 3 and item[0]:
                        cat = item[0]
                        parts = [x for x in item[1:] if x]
                        if parts:
                            category_map[cat] = parts
            except:
                pass

fallback_map = {
    '外語': ['外語學群'], '外文': ['外語學群'], '英美': ['外語學群'], '外國語': ['外語學群'],
    '文學': ['文史哲學群'], '中文': ['文史哲學群'], '國文': ['文史哲學群'], '語文': ['文史哲學群'],
    '宗教': ['文史哲學群'], '哲學': ['文史哲學群'], '歷史': ['文史哲學群'],
    '資工': ['資訊學群', '工程學群'], '資訊': ['資訊學群'], '通訊': ['工程學群'],
    '機電': ['工程學群'], '光電': ['工程學群'], '材料': ['工程學群'], '動力': ['工程學群'],
    '土木': ['工程學群'], '化工': ['工程學群'], '機械': ['工程學群'], '營建': ['工程學群'],
    '醫藥': ['醫藥衛生學群'], '護理': ['醫藥衛生學群'], '長照': ['醫藥衛生學群'], '高齡': ['醫藥衛生學群'],
    '生技': ['生命科學學群'], '生科': ['生命科學學群'], '生物': ['生命科學學群'],
    '企管': ['管理學群'], '資管': ['管理學群'], '管理': ['管理學群'], '經營': ['管理學群'],
    '財金': ['財經學群'], '會計': ['財經學群'], '金融': ['財經學群'], '財政': ['財經學群'],
    '特教': ['教育學群'], '幼教': ['教育學群'], '師資': ['教育學群'], '教育': ['教育學群'],
    '傳播': ['大眾傳播學群'], '新聞': ['大眾傳播學群'], '視傳': ['大眾傳播學群'],
    '設計': ['建築設計學群', '藝術學群'], '建築': ['建築設計學群'], '景觀': ['建築設計學群'],
    '美術': ['藝術學群'], '藝術': ['藝術學群'], '音樂': ['藝術學群'], '舞蹈': ['藝術學群'],
    '休閒': ['遊憩運動學群'], '體育': ['遊憩運動學群'], '觀光': ['遊憩運動學群'],
    '動物': ['生物資源學群'], '植物': ['生物資源學群'], '農': ['生物資源學群'], '森林': ['生物資源學群'],
    '社工': ['社會心理學群'], '社會': ['社會心理學群'], '心理': ['社會心理學群'],
    '法律': ['法政學群'], '政治': ['法政學群'], '公衛': ['醫藥衛生學群'],
    '物理': ['數理化學群'], '化學': ['數理化學群'], '數學': ['數理化學群'], '科學': ['數理化學群'],
    '地質': ['地球環境學群'], '地理': ['地球環境學群'], '環境': ['地球環境學群'], '大氣': ['地球環境學群'],
    '海洋': ['地球環境學群']
}

std_keys = sorted(category_map.keys(), key=lambda x: len(x), reverse=True)
fall_keys = sorted(fallback_map.keys(), key=lambda x: len(x), reverse=True)

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

uncertain = []

for dept in data:
    dept_name = dept.get('dept_name', '')
    extracted = None
    
    for k in std_keys:
        if k in dept_name:
            extracted = True
            break
            
    if not extracted:
        for k in fall_keys:
            if k in dept_name:
                extracted = True
                break
                
    if not extracted:
        uncertain.append((dept_name, dept.get('eighteen_groups', [])))

with open('uncertain_departments.md', 'w', encoding='utf-8') as f:
    f.write("# 疑似需要人工判定之校系清單\n\n這些科系在第一次和第二次關鍵字掃描時都沒被打中，強迫使用了第三次保底規則。\n\n")
    for name, grp in uncertain:
        f.write(f"- {name} (目前保底分發至: {grp})\n")

print(f"Total uncertain: {len(uncertain)}")
for name, grp in uncertain[:10]:
    print(f"{name} -> {grp}")
