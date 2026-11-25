import os
import re

fe_dir = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\frontend\src'
api_calls = set()

for root, _, files in os.walk(fe_dir):
    for f in files:
        if f.endswith(('.ts', '.tsx')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                matches = re.findall(r'(?:api\.(?:get|post|put|delete)|fetch)\s*\(\s*[\'`"]([^\'`"?\s]+)', content)
                for m in matches:
                    api_calls.add((f, m))

print("=== API ENDPOINTS CALLED IN FRONTEND ===")
for f, call in sorted(api_calls):
    print(f"  {f} -> {call}")
