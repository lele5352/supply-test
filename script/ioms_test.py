from dbo.ioms_dbo import IOMSDBOperator as IOMS


data = IOMS.get_origin_ware_sku_data()

for i in data :
    print(i)