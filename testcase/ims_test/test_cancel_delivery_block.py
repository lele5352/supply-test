import time
import pytest

from testcase import *


class TestCancelDeliveryBlock(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id
        self.sale_sku_count = 2
        self.sj_kw_ids = fsj_kw_ids
        self.yk_kw_id = yk_kw_id

    def setup(self):
        self.delivery_code = 'CK' + str(int(time.time()))
        ims.delete_qualified_inventory([sale_sku])
        time.sleep(1)

    # @pytest.mark.skip(reason='test')
    def test_1_cancel_only_sale_sku_oms_order_oms_block(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku, bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(sale_sku, 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_cancel_only_sale_sku_delivery_order_block_before_pick(self):
        """只包含销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(sale_sku, 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims.cancel_block_before_pick(self.delivery_code)

        cancel_block_before_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_3_cancel_only_sale_sku_delivery_order_block_after_pick(self):
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(sale_sku, 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            sale_sku,
            bom,
            self.sale_sku_count,
            self.warehouse_id
        )
        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_block_after_pick_res = ims.cancel_block_after_pick(
            self.delivery_code,
            sale_sku,
            self.yk_kw_id,
            self.sale_sku_count,
            bom,
            self.warehouse_id
        )

        cancel_block_after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 构造期望库存数据
        actual_pick_num = 0
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            # 实拣数累加
            actual_pick_num += detail[1] * self.sale_sku_count
            # 释放库位库存,与最初的比，只需要直接把库位库存扣掉
            self.expect_inventory[detail[0]][sj_location_id]['stock'] -= detail[1] * self.sale_sku_count
            # 上架库位库存最终转移到移库库位
            self.expect_inventory[detail[0]].update(
                {
                    self.yk_kw_id: {
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

    def test_4_cancel_oms_block_include_component_and_sale_sku_oms_order(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku, bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)
        order_info = [(sale_sku, 1), ('BP' + sale_sku + 'A01', 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_5_cancel_delivery_order_block_include_component_and_sale_sku_oms_order(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(sale_sku, 1), ('BP' + sale_sku + 'A01', 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims.cancel_block_before_pick(self.delivery_code)

        cancel_block_before_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_7_cancel_oms_block_only_component_oms_order(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku, bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)
        order_info = [('BP' + sale_sku + 'A01', 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_8_cancel_delivery_order_block_only_component_oms_order(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims.add_qualified_stock_by_other_in(
            sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [('BP' + sale_sku + 'A01', 1)]
        oms_order_block_res = ims.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims.cancel_block_before_pick(self.delivery_code)

        cancel_block_before_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
