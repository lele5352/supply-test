import time
import pytest

from testcase.ims_test import *


class TestDeliveryPick(object):
    """
    README:
        仅发货仓、直发仓支持销售出库流程，对应IMS库存数据模型为AA型，即warehouse_id与target_warehouse_id相同且不为空
    """

    def setup_class(self):
        self.ims = ims
        self.sale_sku_code = sale_sku_code
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.bom_version = bom_version

        self.sale_sku_count = 2
        self.bom_detail = self.ims.get_sale_sku_bom_detail(self.sale_sku_code, self.bom_version)
        self.sj_location_codes = self.ims.wms_api.get_location_codes(len(self.bom_detail), 5, self.warehouse_id)
        self.yk_location_codes = self.ims.wms_api.get_location_codes(len(self.bom_detail), 4, self.warehouse_id)
        self.sj_location_ids = [self.ims.wms_api.get_location_id(location_code, self.warehouse_id) for location_code in
                                self.sj_location_codes]

    def setup(self):
        # 这里踩过坑，单据号不能放在setupclass里面，否则每次单据号都一样，会触发幂等，导致结果不正确
        self.delivery_code = 'CK' + str(int(time.time()))
        # 清掉测试的销售sku库存数据
        self.ims.delete_ims_data(self.sale_sku_code, self.warehouse_id)
        # 采购入库生成销售sku现货库存
        self.ims.add_stock_by_purchase_into_warehouse(
            self.sale_sku_code, self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_completely_pick(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )
        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 分配库位库存，预占库位库存
        assign_location_stock_res = self.ims.assign_location_stock(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        expect_ware_sku_inventory_dict = dict()
        actual_pick_num = 0

        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
            # 实拣数累加
            actual_pick_num += detail[1] * self.sale_sku_count

            # 根据拣货数据构造拣货后期望的仓库库存数据
            expect_ware_sku_inventory_dict[detail[0]] = {
                location_id: {'block': detail[1] * self.sale_sku_count - pick_qty,
                              'stock': detail[1] * self.sale_sku_count - pick_qty},
                'total': {'block': detail[1] * self.sale_sku_count,
                          'stock': detail[1] * self.sale_sku_count}
            }
        # 更新期望仓库库存数据，加入dock库存为实拣数
        expect_ware_sku_inventory_dict.update({
            -self.warehouse_id: {'block': 0, 'stock': actual_pick_num}
        })
        confirm_pick_res = self.ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_pick_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
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
        assert after_pick_inventory == expect_after_pick_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_short_pick(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )
        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 分配库位库存，预占库位库存
        assign_location_stock_res = self.ims.assign_location_stock(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        expect_ware_sku_inventory_dict = dict()
        actual_pick_num = 0

        # 构造拣货sku明细数据，此处为短拣
        for location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count - 1
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
            # 实拣数累加
            actual_pick_num += pick_qty

            # 根据拣货数据构造拣货后期望的仓库库存数据
            expect_ware_sku_inventory_dict[detail[0]] = {
                location_id: {'block': detail[1] * self.sale_sku_count - pick_qty,
                              'stock': detail[1] * self.sale_sku_count - pick_qty},
                'total': {'block': detail[1] * self.sale_sku_count,
                          'stock': detail[1] * self.sale_sku_count}
            }
        # 更新期望仓库库存数据，加入dock库存为实拣数
        expect_ware_sku_inventory_dict.update({
            -self.warehouse_id: {'block': 0, 'stock': actual_pick_num}
        })
        confirm_pick_res = self.ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_short_pick_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
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
        assert after_short_pick_inventory == expect_after_short_pick_inventory


if __name__ == '__main__':
    pytest.main()
