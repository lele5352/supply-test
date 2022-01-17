import time
import pytest

from testcase.ims_test import *


class TestBlockCancel(object):
    def setup_class(self):
        self.ims = ims
        self.sale_sku_code = sale_sku_code
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.sale_sku_count = 2
        self.bom_version = bom_version
        self.bom_detail = bom_detail
        self.sj_location_ids = fsj_location_ids
        self.yk_location_id = yk_location_id

    def setup(self):
        self.delivery_code = 'CK' + str(int(time.time()))
        self.ims.delete_ims_data(self.sale_sku_code)
        time.sleep(1)
        # 采购入库生成销售sku现货库存
        self.ims.add_stock_by_purchase_into_warehouse(
            self.sale_sku_code, self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)
        self.expect_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_cancel_oms_order_block(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = self.ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_cancel_delivery_order_block_before_assign_location_stock(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )

        delivery_order_block_res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 记录oms预占库存流水id和sourceNo
        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = self.ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_block_before_pick_res = self.ims.cancel_block_before_pick(self.delivery_code)

        cancel_block_before_pick_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_3_cancel_delivery_order_block_after_assign_location_stock(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )

        delivery_order_block_res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        assign_location_stock_res = self.ims.assign_location_stock(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id
        )
        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = self.ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_block_before_pick_res = self.ims.cancel_block_before_pick(self.delivery_code)

        cancel_block_before_pick_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_4_cancel_delivery_order_block_after_pick(self):
        oms_order_block_res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )

        delivery_order_block_res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        assign_location_stock_res = self.ims.assign_location_stock(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for sj_location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)

        confirm_pick_res = self.ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = self.ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_block_after_pick_res = self.ims.cancel_block_after_pick(
            self.delivery_code,
            self.sale_sku_code,
            self.yk_location_id,
            self.sale_sku_count,
            self.bom_version,
            self.warehouse_id
        )

        cancel_block_after_pick_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )

        # 构造期望库存数据
        actual_pick_num = 0
        for sj_location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            # 实拣数累加
            actual_pick_num += detail[1] * self.sale_sku_count
            # 释放库位库存,与最初的比，只需要直接把库位库存扣掉
            self.expect_inventory[detail[0]][sj_location_id]['stock'] -= detail[1] * self.sale_sku_count
            # 上架库位库存最终转移到移库库位
            self.expect_inventory[detail[0]].update(
                {
                    self.yk_location_id: {
                        "stock": detail[1] * self.sale_sku_count,
                        "block": 0
                    },
                    # 拣货时库位库存转移到dock库存，取消后dock库存又转移到移库库位，所以相当于插入dock为0的库存数据
                    -self.warehouse_id: {'stock': 0, 'block': 0}
                })

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_block_after_pick_res['code'] == 200
        assert cancel_block_after_pick_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
