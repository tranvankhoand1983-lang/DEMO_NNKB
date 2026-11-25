import os
import re
import json
from decimal import Decimal

sql_path = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\database\web_trang_suc_db.sql'
with open(sql_path, 'r', encoding='utf-8') as f:
    text = f.read()

def parse_sql_values(val_block):
    """
    State-machine parser to parse a MySQL VALUES block into a list of tuples.
    Handles strings with single quotes, escaped quotes \', NULL, numbers, etc.
    """
    rows = []
    current_row = []
    current_val = []
    in_string = False
    escape = False
    in_row = False

    i = 0
    n = len(val_block)
    while i < n:
        ch = val_block[i]

        if not in_row:
            if ch == '(':
                in_row = True
                current_row = []
                current_val = []
            i += 1
            continue

        # Inside a row (...)
        if in_string:
            if escape:
                current_val.append(ch)
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == "'":
                # Check for double single quotes '' in SQL
                if i + 1 < n and val_block[i + 1] == "'":
                    current_val.append("'")
                    i += 1
                else:
                    in_string = False
            else:
                current_val.append(ch)
        else:
            if ch == "'":
                in_string = True
            elif ch == ',':
                # End of a column value
                raw = "".join(current_val).strip()
                current_row.append(interpret_val(raw))
                current_val = []
            elif ch == ')':
                # End of the row
                raw = "".join(current_val).strip()
                current_row.append(interpret_val(raw))
                rows.append(current_row)
                in_row = False
                current_row = []
                current_val = []
            else:
                current_val.append(ch)
        i += 1
    return rows

def interpret_val(val_str):
    if not val_str:
        return None
    val_str = val_str.strip()
    if val_str.upper() == 'NULL':
        return None
    # Check if string literal
    if (val_str.startswith("'") and val_str.endswith("'")) or (val_str.startswith('"') and val_str.endswith('"')):
        return val_str[1:-1]
    # Check boolean / int
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        return val_str

pattern = re.compile(r'INSERT INTO `(\w+)`\s*\((.*?)\)\s*VALUES\s*(.*?);', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(text)

raw_tables = {}
for table, cols, val_block in matches:
    col_names = [c.strip().strip('`') for c in cols.split(',')]
    parsed_rows = parse_sql_values(val_block)
    
    table_data = []
    for r in parsed_rows:
        if len(r) == len(col_names):
            row_dict = dict(zip(col_names, r))
            table_data.append(row_dict)
        else:
            print(f"Warning: column mismatch in {table}: expected {len(col_names)}, got {len(r)}")
            # Try to zip up to min len
            row_dict = dict(zip(col_names, r[:len(col_names)]))
            table_data.append(row_dict)
    raw_tables[table] = table_data
    print(f"Parsed table: {table} ({len(table_data)} rows)")

# Now construct MongoDB NoSQL Collections
seeds_dir = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\database\seeds'
os.makedirs(seeds_dir, exist_ok=True)

# 1. Categories
categories = raw_tables.get('categories', [])
with open(os.path.join(seeds_dir, 'categories.json'), 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

# 2. Materials
materials = raw_tables.get('materials', [])
with open(os.path.join(seeds_dir, 'materials.json'), 'w', encoding='utf-8') as f:
    json.dump(materials, f, ensure_ascii=False, indent=2)

# Quick lookup maps
cat_map = {c['id']: c for c in categories}
mat_map = {m['id']: m for m in materials}

# 3. Products (Embed Images and Variants)
products_raw = raw_tables.get('products', [])
product_images_raw = raw_tables.get('product_images', [])
product_variants_raw = raw_tables.get('product_variants', [])

# Group images by productId
images_by_prod = {}
for img in sorted(product_images_raw, key=lambda x: (x.get('productId'), x.get('displayOrder', 0))):
    p_id = img.get('productId')
    images_by_prod.setdefault(p_id, []).append(img)

# Group variants by productId
variants_by_prod = {}
for v in product_variants_raw:
    p_id = v.get('productId')
    # Clean booleans
    v['isSale'] = bool(v.get('isSale'))
    v['inStock'] = (v.get('stockQuantity', 0) or 0) > 0
    variants_by_prod.setdefault(p_id, []).append(v)

products_nosql = []
for p in products_raw:
    p_id = p['id']
    cat = cat_map.get(p.get('categoryId'), {})
    mat = mat_map.get(p.get('materialId'), {})
    
    imgs = images_by_prod.get(p_id, [])
    # string array of urls matching frontend types
    image_urls = [img['url'] for img in imgs]
    
    variants = variants_by_prod.get(p_id, [])
    available_sizes = [v['size'] for v in variants if v.get('size')]
    
    # Calculate inStock
    total_stock = p.get('stockQuantity') or sum((v.get('stockQuantity') or 0) for v in variants)
    in_stock = total_stock > 0

    p_doc = {
        "id": p_id,
        "sku": p.get('sku'),
        "name": p.get('name'),
        "price": p.get('price'),
        "originalPrice": p.get('originalPrice'),
        "category": cat.get('slug') or cat.get('name') or '',
        "categoryId": p.get('categoryId'),
        "categoryName": cat.get('name') or '',
        "material": mat.get('slug') or mat.get('name') or '',
        "materialId": p.get('materialId'),
        "materialName": mat.get('name') or '',
        "description": p.get('description'),
        "originStory": p.get('originStory'),
        "stockQuantity": total_stock,
        "rating": float(p.get('rating') or 5.0),
        "reviews": int(p.get('reviewCount') or 0),
        "isNew": bool(p.get('isNew')),
        "isSale": bool(p.get('isSale')),
        "inStock": in_stock,
        "availableSizes": available_sizes,
        "images": image_urls,
        "detailedImages": imgs,
        "variants": variants,
        "createdAt": p.get('createdAt')
    }
    products_nosql.append(p_doc)

with open(os.path.join(seeds_dir, 'products.json'), 'w', encoding='utf-8') as f:
    json.dump(products_nosql, f, ensure_ascii=False, indent=2)

# 4. Users
users_raw = raw_tables.get('users', [])
users_nosql = []
for u in users_raw:
    u_doc = {
        "id": u.get('id'),
        "fullName": u.get('fullName'),
        "name": u.get('fullName'),
        "email": u.get('email'),
        "password": u.get('password'),
        "avatar": u.get('avatar'),
        "role": u.get('role'),
        "provider": u.get('provider') or 'email',
        "phone": u.get('phone'),
        "address": u.get('defaultAddress'),
        "newsletterOptin": bool(u.get('newsletterOptin')),
        "isActive": bool(u.get('isActive')),
        "createdAt": u.get('createdAt')
    }
    users_nosql.append(u_doc)

with open(os.path.join(seeds_dir, 'users.json'), 'w', encoding='utf-8') as f:
    json.dump(users_nosql, f, ensure_ascii=False, indent=2)

# 5. Orders (Embed Items)
orders_raw = raw_tables.get('orders', [])
order_items_raw = raw_tables.get('order_items', [])

items_by_order = {}
for oi in order_items_raw:
    ord_id = oi.get('orderId')
    # Link basic product details for convenience
    matching_prod = next((p for p in products_nosql if p['id'] == oi.get('productId')), None)
    if matching_prod:
        oi['product'] = {
            "id": matching_prod['id'],
            "name": matching_prod['name'],
            "price": matching_prod['price'],
            "images": matching_prod['images']
        }
    items_by_order.setdefault(ord_id, []).append(oi)

orders_nosql = []
for o in orders_raw:
    ord_id = o.get('id')
    items = items_by_order.get(ord_id, [])
    
    o_doc = {
        "id": ord_id,
        "userId": o.get('userId'),
        "date": o.get('createdAt'),
        "createdAt": o.get('createdAt'),
        "paidAt": o.get('paidAt'),
        "paymentDate": o.get('paidAt'),
        "recipientName": f"{o.get('firstName', '')} {o.get('lastName', '')}".strip(),
        "firstName": o.get('firstName'),
        "lastName": o.get('lastName'),
        "email": o.get('email'),
        "phone": o.get('phone'),
        "company": o.get('company'),
        "address": o.get('address'),
        "apartment": o.get('apartment'),
        "city": o.get('city'),
        "country": o.get('country') or 'Việt Nam',
        "postalCode": o.get('postalCode'),
        "shippingMethod": o.get('shippingMethod'),
        "shippingFee": o.get('shippingFee'),
        "paymentMethod": o.get('paymentMethod'),
        "paymentStatus": o.get('paymentStatus'),
        "status": o.get('orderStatus'),
        "orderStatus": o.get('orderStatus'),
        "discountCode": o.get('discountCode'),
        "discountAmount": o.get('discountAmount'),
        "total": o.get('totalAmount'),
        "totalAmount": o.get('totalAmount'),
        "estimatedDelivery": o.get('estimatedDelivery'),
        "items": items
    }
    orders_nosql.append(o_doc)

with open(os.path.join(seeds_dir, 'orders.json'), 'w', encoding='utf-8') as f:
    json.dump(orders_nosql, f, ensure_ascii=False, indent=2)

# 6. Carts (Embed Items)
carts_raw = raw_tables.get('carts', [])
cart_items_raw = raw_tables.get('cart_items', [])

items_by_cart = {}
for ci in cart_items_raw:
    c_id = ci.get('cartId')
    matching_prod = next((p for p in products_nosql if p['id'] == ci.get('productId')), None)
    if matching_prod:
        ci['product'] = {
            "id": matching_prod['id'],
            "name": matching_prod['name'],
            "price": matching_prod['price'],
            "images": matching_prod['images']
        }
    items_by_cart.setdefault(c_id, []).append(ci)

carts_nosql = []
for c in carts_raw:
    c_id = c.get('id')
    items = items_by_cart.get(c_id, [])
    c_doc = {
        "id": c_id,
        "userId": c.get('userId'),
        "createdAt": c.get('createdAt'),
        "items": items
    }
    carts_nosql.append(c_doc)

with open(os.path.join(seeds_dir, 'carts.json'), 'w', encoding='utf-8') as f:
    json.dump(carts_nosql, f, ensure_ascii=False, indent=2)

# 7. Promotions / Vouchers
promotions_raw = raw_tables.get('promotions', [])
with open(os.path.join(seeds_dir, 'promotions.json'), 'w', encoding='utf-8') as f:
    json.dump(promotions_raw, f, ensure_ascii=False, indent=2)

# 8. User Vouchers
user_vouchers_raw = raw_tables.get('user_vouchers', [])
with open(os.path.join(seeds_dir, 'user_vouchers.json'), 'w', encoding='utf-8') as f:
    json.dump(user_vouchers_raw, f, ensure_ascii=False, indent=2)

# 9. Banners
banners_raw = raw_tables.get('banners', [])
with open(os.path.join(seeds_dir, 'banners.json'), 'w', encoding='utf-8') as f:
    json.dump(banners_raw, f, ensure_ascii=False, indent=2)

# 10. Reviews
reviews_raw = raw_tables.get('reviews', [])
with open(os.path.join(seeds_dir, 'reviews.json'), 'w', encoding='utf-8') as f:
    json.dump(reviews_raw, f, ensure_ascii=False, indent=2)

# 11. Shop Settings
shop_settings_raw = raw_tables.get('shop_settings', [])
with open(os.path.join(seeds_dir, 'shop_settings.json'), 'w', encoding='utf-8') as f:
    json.dump(shop_settings_raw, f, ensure_ascii=False, indent=2)

print("\n--- EXTRACTION COMPLETED SUCCESSFULLY ---")
print(f"Generated 11 seed files in: {seeds_dir}")
for f_name in os.listdir(seeds_dir):
    f_path = os.path.join(seeds_dir, f_name)
    with open(f_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        print(f"  - {f_name}: {len(data) if isinstance(data, list) else 1} documents")
