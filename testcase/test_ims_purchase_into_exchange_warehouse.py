import pytest

from data_helper.ims_data_helper import ImsDataHelper


class TestImsPurchaseIntoExchangeWarehouse(object):
    def setup_class(self):
        self.ims = ImsDataHelper()
        self.sale_sku_code = '11471839197'
        self.current_warehouse_id = 29
        self.target_warehouse_id = 31
        self.bom_version = "A"
        self.sale_sku_count = 1
        self.sj_location_ids = [147, 148, 149]
        self.ims.delete_ims_data(self.sale_sku_code, self.current_warehouse_id)

    def test_1_purchase_create_order(self):
        res = self.ims.purchase_create_order(
            self.sale_sku_code,
            self.sale_sku_count,
            self.current_warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.current_warehouse_id,
            self.target_warehouse_id
        )
        expect_ims_inventory_data = {
            "central_inventory_stock": 1,
            "central_inventory_block": 0,
            "central_inventory_sale_stock": 1,
            "central_inventory_sale_block": 0,
            'goods_inventory_purchase_on_way_stock': 1,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': 0,
            'goods_inventory_spot_goods_block': 0
        }

        assert res['code'] == 200
        assert current_inventory == expect_ims_inventory_data

    def test_2_purchase_into_warehouse(self):
        res = self.ims.purchase_into_warehouse(
            self.sale_sku_code,
            self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.current_warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.current_warehouse_id,
            self.target_warehouse_id
        )

        # 中央库存、销售商品总库存不变；销售商品采购在途转现货；仓库商品入库新增库位库存
        expect_ims_inventory_data = {
            "central_inventory_stock": 1,
            "central_inventory_block": 0,
            "central_inventory_sale_stock": 1,
            "central_inventory_sale_block": 0,
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': 1,
            'goods_inventory_spot_goods_block': 0,
            '19109732485A01': {self.sj_location_ids[0]: {'block': 0, 'stock': 1}, 'total': {'block': 0, 'stock': 1}},
            '19109732485A02': {self.sj_location_ids[1]: {'block': 0, 'stock': 3}, 'total': {'block': 0, 'stock': 3}},
            '19109732485A03': {self.sj_location_ids[2]: {'block': 0, 'stock': 2}, 'total': {'block': 0, 'stock': 2}}
        }

        assert res['code'] == 200
        assert current_inventory == expect_ims_inventory_data


if __name__ == '__main__':
    pytest.main()
