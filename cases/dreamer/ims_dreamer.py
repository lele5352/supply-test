class IMSDreamer():
    def __init__(self):
        pass

    def add_location_stock(self, wares_inventory, ware_sku_kw_qty_list):
        pass

    def reduce_location_stock(self, wares_inventory, ware_sku_kw_qty_list):
        pass

    def add_location_block(self, wares_inventory, ware_sku_kw_qty_list):
        pass

    def reduce_location_block(self, wares_inventory, ware_sku_kw_qty_list):
        pass

    def add_stock(self, wares_inventory, ware_sku_qty_list):
        pass

    def reduce_stock(self, wares_inventory, ware_sku_qty_list):
        pass

    def get_add_kw_stock_expect_inventory(self, ware_inventory, ware_sku_qty_list, change_type):
        """获取带库位的库存增减期望结果
        @param ware_inventory: 原始库位级库存
        @param ware_sku_qty_list: 变更列表，格式：[(ware_sku,qty),...]
        @param change_type: 1-增加库存，2-减少库存
        """
        pass

    def get_change_stock_expect_inventory(self, ware_inventory, ware_sku_qty_list, change_type):
        """获取不带库位的库存增减期望结果
        @param ware_inventory: 原始库位级库存
        @param ware_sku_qty_list: 变更列表，格式：[(ware_sku,qty),...]
        @param change_type: 1-增加库存，2-减少库存
        """
        pass

    def get_change_on_way_expect_inventory(self, ware_inventory, ware_sku_qty_list, change_type):
        """获取在途库存增减期望结果
        @param ware_inventory: 原始库存
        @param ware_sku_qty_list: 变更列表，格式：[(ware_sku,qty),...]
        @param change_type: 1-增加库存，2-减少库存
        """
        pass
