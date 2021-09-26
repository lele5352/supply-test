import pandas


def get_excel_data(file_name):
    df = pandas.read_excel(file_name)
    excel_data = []

    for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = df.loc[
            i,
            [
                'api',
                'num',
                'central_inventory_stock',
                'central_inventory_block',
                'central_inventory_sale_stock',
                'central_inventory_sale_block',
                'wares_inventory_stock',
                'wares_inventory_block',
                'wares_inventory_location_stock',
                'wares_inventory_location_block',
                'wares_inventory_dock_stock',
                'wares_inventory_dock_block',
                'goods_inventory_purchase_on_way',
                'goods_inventory_in_stock',
                'goods_inventory_transfer_on_way'
            ]
        ].to_dict()
        excel_data.append(row_data)
    return excel_data


if __name__ == '__main__':
    data = get_excel_data("../testcase/ims_stock_test.xlsx")
    print(data)
