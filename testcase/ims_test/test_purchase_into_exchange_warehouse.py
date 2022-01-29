import pytest

from testcase import *


class TestPurchaseIntoExchangeWarehouse(object):
    def setup_class(self):
        self.ims = ims
        self.sale_sku_code = sale_sku_code
        self.warehouse_id = exchange_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.bom_version = bom_version
        self.bom_detail = bom_detail
        self.sale_sku_count = 3
        self.sj_location_ids = zsj_location_ids
        self.ims.delete_ims_data(self.sale_sku_code)

    def test_1_purchase_create_order(self):
        res = self.ims.purchase_create_order(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id)
        expect_ims_inventory_data = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": 0,
            "central_inventory_sale_stock": self.sale_sku_count,
            "central_inventory_sale_block": 0,
            'goods_inventory_purchase_on_way_stock': self.sale_sku_count,
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
            self.sale_sku_count,
            self.sj_location_ids,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id)

        expect_ims_inventory_data = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": 0,
            "central_inventory_sale_stock": self.sale_sku_count,
            "central_inventory_sale_block": 0,
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': self.sale_sku_count,
            'goods_inventory_spot_goods_block': 0
        }
        for location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            # 构造仓库库存数据
            expect_ims_inventory_data[detail[0]] = {
                location_id: {
                    'block': 0, 'stock': detail[1] * self.sale_sku_count},
                'total': {'block': 0, 'stock': detail[1] * self.sale_sku_count}
            }

        assert res['code'] == 200
        assert current_inventory == expect_ims_inventory_data


if __name__ == '__main__':
    pytest.main()
