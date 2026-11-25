import os
import re
import json

sql_path = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\database\web_trang_suc_db.sql'
with open(sql_path, 'r', encoding='utf-8') as f:
    sql_text = f.read()

# Parse CREATE TABLE to get columns for each table
table_cols = {}
create_tables = re.findall(r'CREATE TABLE `(\w+)`\s*\((.*?)\)\s*ENGINE', sql_text, re.DOTALL | re.IGNORECASE)
for t, body in create_tables:
    cols = []
    for line in body.strip().split('\n'):
        line = line.strip()
        m = re.match(r'^`(\w+)`', line)
        if m:
            cols.append(m.group(1))
    table_cols[t] = cols

seeds_dir = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\database\seeds'
print(f"Total tables found in SQL: {len(table_cols)}")

# Load all seeds
seed_data = {}
for f in os.listdir(seeds_dir):
    if f.endswith('.json'):
        with open(os.path.join(seeds_dir, f), 'r', encoding='utf-8') as jf:
            seed_data[f.replace('.json', '')] = json.load(jf)

print("\n=== DETAILED VERIFICATION FOR EACH TABLE ===")
for t, cols in sorted(table_cols.items()):
    if t in seed_data:
        docs = seed_data[t]
        first_doc = docs[0] if docs else {}
        missing = [c for c in cols if c not in first_doc]
        extra = [k for k in first_doc.keys() if k not in cols]
        print(f"Table '{t}': {len(docs)} docs. SQL cols: {len(cols)}, JSON keys: {len(first_doc)}")
        if missing:
            print(f"   Missing cols: {missing}")
        else:
            print(f"   -> 100% SQL columns present!")
        if extra:
            print(f"   -> Enhanced NoSQL fields: {extra}")
    elif t in ['product_images', 'product_variants']:
        # Embedded in products
        prods = seed_data.get('products', [])
        sample = prods[0] if prods else {}
        if t == 'product_images':
            imgs = sample.get('detailedImages', [])
            first_img = imgs[0] if imgs else {}
            missing = [c for c in cols if c not in first_img]
            print(f"Table '{t}': Embedded in products. Total imgs across all prods: {sum(len(p.get('detailedImages', [])) for p in prods)}")
            print(f"   -> Missing: {missing}")
        else:
            vars_ = sample.get('variants', [])
            first_v = vars_[0] if vars_ else {}
            missing = [c for c in cols if c not in first_v]
            print(f"Table '{t}': Embedded in products. Total vars across all prods: {sum(len(p.get('variants', [])) for p in prods)}")
            print(f"   -> Missing: {missing}")
    elif t == 'order_items':
        orders = seed_data.get('orders', [])
        first_item = orders[0].get('items', [])[0] if orders and orders[0].get('items') else {}
        missing = [c for c in cols if c not in first_item]
        print(f"Table '{t}': Embedded in orders. Total items: {sum(len(o.get('items', [])) for o in orders)}")
        print(f"   -> Missing: {missing}")
    elif t == 'cart_items':
        carts = seed_data.get('carts', [])
        first_item = carts[0].get('items', [])[0] if carts and carts[0].get('items') else {}
        missing = [c for c in cols if c not in first_item]
        print(f"Table '{t}': Embedded in carts. Total items: {sum(len(c.get('items', [])) for c in carts)}")
        print(f"   -> Missing: {missing}")
    else:
        print(f"Table '{t}': 0 rows in SQL dump (empty table).")
