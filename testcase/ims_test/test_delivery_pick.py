import time
import pytest

from testcase import *


class TestDeliveryPick(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id

        self.sale_sku_count = 2
        self.sj_kw_ids = fsj_kw_ids

    def setup(self):
        # 这里踩过坑，单据号不能放在setupclass里面，否则每次单据号都一样，会触发幂等，导致结果不正确
        self.delivery_code = 'CK' + str(int(time.time()))
        # 清掉测试的销售sku库存数据
        ims.delete_ims_data(sale_sku)
        time.sleep(1)
        # 采购入库生成销售sku现货库存
        ims.add_stock_by_purchase_in(
            sale_sku,
            bom,
            self.sj_kw_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_completely_pick(self):
        oms_order_block_res = ims.oms_order_block(
            sale_sku,
            self.sale_sku_count,
            self.warehouse_id,
        )
        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            sale_sku,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            sale_sku,
            bom,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        expect_ware_sku_inventory_dict = dict()

        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)

            # 根据拣货数据构造拣货后期望的仓库库存数据
            expect_ware_sku_inventory_dict[detail[0]] = {
                location_id: {'block': detail[1] * self.sale_sku_count - pick_qty,
                              'stock': detail[1] * self.sale_sku_count - pick_qty},
                'total': {'block': detail[1] * self.sale_sku_count,
                          'stock': detail[1] * self.sale_sku_count},
                -self.warehouse_id: {'block': 0, 'stock': pick_qty}
            }

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_pick_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id
        )

        expect_central_inventory_dict = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": self.sale_sku_count,
            "central_inventory_sale_stock": self.sale_sku_count,
            "central_inventory_sale_block": self.sale_sku_count
        }

        expect_goods_inventory_dict = {
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': self.sale_sku_count,
            'goods_inventory_spot_goods_block': self.sale_sku_count,
        }

        expect_after_pick_inventory = dict()
        expect_after_pick_inventory.update(expect_central_inventory_dict)
        expect_after_pick_inventory.update(expect_goods_inventory_dict)
        expect_after_pick_inventory.update(expect_ware_sku_inventory_dict)

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert expect_after_pick_inventory == after_pick_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_short_pick(self):
        oms_order_block_res = ims.oms_order_block(
            sale_sku,
            self.sale_sku_count,
            self.warehouse_id,
        )
        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            sale_sku,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            sale_sku,
            bom,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        expect_ware_sku_inventory_dict = dict()
        actual_pick_num = 0

        # 构造拣货sku明细数据，此处为短拣
        for location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count - 1
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
            # 实拣数累加

            # 根据拣货数据构造拣货后期望的仓库库存数据
            expect_ware_sku_inventory_dict[detail[0]] = {
                location_id: {'block': detail[1] * self.sale_sku_count - pick_qty,
                              'stock': detail[1] * self.sale_sku_count - pick_qty},
                'total': {'block': detail[1] * self.sale_sku_count,
                          'stock': detail[1] * self.sale_sku_count},
                -self.warehouse_id: {'block': 0, 'stock': pick_qty}
            }

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_short_pick_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id
        )
        expect_central_inventory_dict = {
            "central_inventory_stock": self.sale_sku_count,
            "central_inventory_block": self.sale_sku_count,
            "central_inventory_sale_stock": self.sale_sku_count,
            "central_inventory_sale_block": self.sale_sku_count
        }

        expect_goods_inventory_dict = {
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': self.sale_sku_count,
            'goods_inventory_spot_goods_block': self.sale_sku_count,
        }

        expect_after_short_pick_inventory = dict()
        expect_after_short_pick_inventory.update(expect_central_inventory_dict)
        expect_after_short_pick_inventory.update(expect_goods_inventory_dict)
        expect_after_short_pick_inventory.update(expect_ware_sku_inventory_dict)

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert expect_after_short_pick_inventory == after_short_pick_inventory


if __name__ == '__main__':
    pytest.main()
