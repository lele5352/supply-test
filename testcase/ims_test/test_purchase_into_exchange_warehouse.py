import pytest

from testcase import *


class TestPurchaseIntoExchangeWarehouse(object):
    def setup_class(self):
        self.warehouse_id = exchange_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.sale_sku_count = 3
        self.sj_kw_ids = zsj_kw_ids
        ims.delete_qualified_inventory(sale_sku)

    def test_1_purchase_create_order(self):
        res = ims.purchase_create_order(
            sale_sku,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)
        expect_ims_inventory_data = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": 0,
            "central_warehouse_stock": self.sale_sku_count,
            "central_warehouse_block": 0,
            'purchase_on_way_stock': self.sale_sku_count,
            'purchase_on_way_block': 0,
            'transfer_on_way_stock': 0,
            'transfer_on_way_block': 0,
            'spot_goods_stock': 0,
            'spot_goods_block': 0
        }

        assert res['code'] == 200
        assert current_inventory == expect_ims_inventory_data

    def test_2_purchase_into_warehouse(self):
        res = ims.purchase_into_warehouse(
            sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)

        expect_ims_inventory_data = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": 0,
            "central_warehouse_stock": self.sale_sku_count,
            "central_warehouse_block": 0,
            'purchase_on_way_stock': 0,
            'purchase_on_way_block': 0,
            'transfer_on_way_stock': 0,
            'transfer_on_way_block': 0,
            'spot_goods_stock': self.sale_sku_count,
            'spot_goods_block': 0
        }
        for location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
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
