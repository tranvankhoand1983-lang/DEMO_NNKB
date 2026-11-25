import re
import json

sql_path = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\database\web_trang_suc_db.sql'
with open(sql_path, 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'INSERT INTO `(\w+)`\s*\((.*?)\)\s*VALUES\s*(.*?);', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(text)
print(f'Total INSERT blocks found: {len(matches)}')
for table, cols, val_block in matches:
    col_names = [c.strip().strip('`') for c in cols.split(',')]
    print(f'Table: {table}, Columns ({len(col_names)}): {col_names}')
