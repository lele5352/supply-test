import time
import pytest

from testcase import *


class TestDeliveryPick(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id

        self.order_info = [(sale_sku, bom, 2)]
        self.sj_kw_ids = wms_logics.base_get_kw(1, 2, len(sale_sku), self.warehouse_id, self.to_warehouse_id)

    def setup(self):
        # 这里踩过坑，单据号不能放在setupclass里面，否则每次单据号都一样，会触发幂等，导致结果不正确
        self.delivery_code = 'OMS' + str(int(time.time()))

    # @pytest.mark.skip(reason='test')
    def test_1_completely_pick(self):
        if not ims_logics.is_stock_satisfy(sale_sku):
            ims_logics.add_lp_stock_by_other_in()

        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            self.order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims_logics.get_combined_block_result_list(block_result_list)
        # 分配库位库存，预占库位库存
        assign_stock_res = ims_request.assign_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        self.expect_lp_inventory['spot_goods_remain'] -= self.order_info[0][1]
        self.expect_lp_inventory['central_remain'] -= self.order_info[0][1]
        for location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            temp_dict = {
                "qty": qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
            # 释放库位库存
            self.expect_lp_inventory[ware_sku]['warehouse_total']['block'] += qty
            self.expect_lp_inventory[ware_sku]['location_total']['block'] += qty
            self.expect_lp_inventory[ware_sku][location_id]['stock'] -= qty
            self.expect_lp_inventory[ware_sku].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': qty}
                }
            )

        confirm_pick_res = ims_logics.confirm_all_picked(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_pick_inventory = ims_logics.get_lp_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert self.expect_lp_inventory == after_pick_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_short_pick(self):
        oms_order_block_res = ims_request.oms_order_block(
            self.order_info,
            self.warehouse_id,
        )
        # 下发销售出库单预占仓库商品总库存、销售sku现货库存
        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            self.order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims_logics.get_combined_block_result_list(block_result_list)
        # 分配库位库存，预占库位库存
        assign_stock_res = ims_request.assign_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        ware_sku_list = list()

        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        self.expect_lp_inventory['spot_goods_remain'] -= self.order_info[0][1]
        self.expect_lp_inventory['central_remain'] -= self.order_info[0][1]
        for location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            pick_loss_num = 1
            temp_dict = {
                "qty": qty - pick_loss_num,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
            # 释放库位库存
            self.expect_lp_inventory[ware_sku]['warehouse_total']['block'] += qty
            self.expect_lp_inventory[ware_sku]['location_total']['block'] += qty
            self.expect_lp_inventory[ware_sku][location_id]['stock'] = pick_loss_num
            self.expect_lp_inventory[ware_sku][location_id]['block'] = pick_loss_num

            self.expect_lp_inventory[ware_sku].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': qty - pick_loss_num}
                }
            )

        confirm_pick_res = ims_logics.confirm_all_picked(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        after_pick_inventory = ims_logics.get_lp_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert self.expect_lp_inventory == after_pick_inventory


if __name__ == '__main__':
    pytest.main()
