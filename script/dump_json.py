import json

list = [
    [{"sku_code": "67330337129", "qty": 2, "bom": "A", "warehouse_id": "513"}]
]
for i in list:
    print(json.dumps(i))
