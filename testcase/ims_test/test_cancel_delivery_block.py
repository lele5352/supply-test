import time
import pytest

from testcase import *


class TestCancelDeliveryBlock(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id
        self.sale_sku_count = 2
        self.sale_sku = '67330337129'
        self.component_sku = 'BP67330337129G01'
        self.sj_kw_ids = wms_logics.get_kw(1, 5, len(self.sale_sku), self.warehouse_id, self.to_warehouse_id)
        self.yk_kw_id = wms_logics.get_kw(1, 4, 1, self.warehouse_id, self.to_warehouse_id)

    def setup(self):
        IMSDBOperator.delete_qualified_inventory([self.sale_sku])
        self.delivery_code = 'CK' + str(int(time.time()))
        time.sleep(1)

    # @pytest.mark.skip(reason='test')
    def test_1_cancel_only_sale_sku_oms_order_oms_block(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku, bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims_request.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_cancel_only_sale_sku_delivery_order_block_before_assign_stock(self):
        """只包含销售sku的出库单下发后，当前未分配库位库存，取消出库单"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_3_cancel_only_sale_sku_delivery_order_block_before_assign_stock_ever_assigned(self):
        """只包含销售sku的出库单下发后，分配过库位库存又取消分配库位库存的拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        block_book_id = assign_stock_res['data'][0]['blockBookId']
        cancel_location_block = ims_request.only_cancel_location_block(block_book_id, self.delivery_code)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_location_block['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_4_cancel_only_sale_sku_delivery_order_block_after_assign_stock(self):
        """只包含销售sku的出库单下发后，分配过库位库存又取消分配库位库存的拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 1)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_5_cancel_only_sale_sku_delivery_order_block_after_assign_stock(self):
        """
            测试场景：销售出库单分配2次库位库存后取消出库单
                步骤1：出库单分配库位库存
                步骤2：出库单创建拣货单并完成拣货
                步骤3：出库单拦截并完成归位
                步骤4：出库单再次分配库位库存
                步骤5：出库单触发取消
        """
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)

        # 分配库存
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)

        # 分配的库存明细
        assigned_ware_sku_info = assign_stock_res['data'][0]['wareSkuList']
        # 确认拣货：库存从上架库位转移到dock
        confirm_all_pick_res = ims_logics.confirm_all_picked(self.delivery_code, assigned_ware_sku_info,
                                                             self.warehouse_id)

        # 拦截归位：走移库，库存从dock到上架库位
        move_dock_res = ims_logics.move_dock_to_sj_kw(self.warehouse_id, self.delivery_code, block_ware_sku_list,
                                                      self.sj_kw_ids)
        # 拦截归位后，wms的出库单是未分配状态，再次分配库位库存，形成2次分配库存流水
        assign_stock_res2 = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        # 取消出库单（拣货前）
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 1)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 期望库存写入各仓库sku dock的stock为的数据
        assigned_ware_skus = set()
        for assigned_info in assigned_ware_sku_info:
            assigned_ware_skus.add(assigned_info['wareSkuCode'])
        for ware_sku in assigned_ware_skus:
            self.expect_inventory[ware_sku].update({
                -self.warehouse_id: {'stock': 0, 'block': 0}
            })

        assert confirm_all_pick_res['code'] == 200
        assert move_dock_res['code'] == 200
        assert assign_stock_res2['code'] == 200
        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_6_cancel_only_sale_sku_delivery_order_block_after_pick(self):
        """只包含销售sku的出库单下发后，拣货后取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims_logics.get_combined_block_result_list(block_result_list)
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims_request.assign_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        ware_sku_list = list()
        for location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            temp_dict = {
                "qty": qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
        confirm_pick_res = ims_logics.confirm_all_picked(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        cancel_block_after_pick_res = ims_request.cancel_block_after_pick(
            self.delivery_code,
            combined_block_result_list,
            self.yk_kw_id,
            self.warehouse_id
        )

        cancel_block_after_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 构造期望库存数据
        for sj_location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            # 释放库位库存,与最初的比，只需要直接把库位库存扣掉
            self.expect_inventory[ware_sku][sj_location_id]['stock'] -= qty
            # 上架库位库存最终转移到移库库位
            self.expect_inventory[ware_sku].update(
                {
                    self.yk_kw_id: {
                        "stock": qty,
                        "block": 0
                    },
                    # 拣货时库位库存转移到dock库存，取消后dock库存又转移到移库库位，所以相当于插入dock为0的库存数据
                    -self.warehouse_id: {'stock': 0, 'block': 0}
                })

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert cancel_block_after_pick_res['code'] == 200
        assert cancel_block_after_pick_inventory == self.expect_inventory

    def test_7_cancel_oms_block_include_component_and_sale_sku_oms_order(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku, bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)
        order_info = [(self.sale_sku, 1), (self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims_request.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_8_cancel_only_sale_sku_delivery_order_block_before_pick_never_block_location(self):
        """只包含销售sku的出库单下发后，从未分配过库位库存的拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_9_cancel_delivery_order_block_include_component_and_sale_sku_oms_order_before_assign_stock(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1), (self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_10_cancel_delivery_order_block_include_component_and_sale_sku_oms_order_before_assign_stock_ever_assigned(
            self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1), (self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        block_book_id = assign_stock_res['data'][0]['blockBookId']
        cancel_location_block = ims_request.only_cancel_location_block(block_book_id, self.delivery_code)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert cancel_location_block['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_11_cancel_delivery_order_block_include_component_and_sale_sku_oms_order_after_assign_stock(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1), (self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 1)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_12_cancel_include_component_and_sale_sku_delivery_order_block_after_pick(self):
        """包含销售sku和部件sku的出库单下发后，拣货后取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.sale_sku, 1), (self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims_logics.get_combined_block_result_list(block_result_list)
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims_request.assign_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for sj_location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            temp_dict = {
                "qty": qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
        confirm_pick_res = ims_logics.confirm_all_picked(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        cancel_block_after_pick_res = ims_request.cancel_block_after_pick(
            self.delivery_code,
            combined_block_result_list,
            self.yk_kw_id,
            self.warehouse_id
        )

        cancel_block_after_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 构造期望库存数据
        for sj_location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            # 释放库位库存,与最初的比，只需要直接把库位库存扣掉
            self.expect_inventory[ware_sku][sj_location_id]['stock'] -= qty
            # 上架库位库存最终转移到移库库位
            self.expect_inventory[ware_sku].update(
                {
                    self.yk_kw_id: {
                        "stock": qty,
                        "block": 0
                    },
                    # 拣货时库位库存转移到dock库存，取消后dock库存又转移到移库库位，所以相当于插入dock为0的库存数据
                    -self.warehouse_id: {'stock': 0, 'block': 0}
                })
        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert cancel_block_after_pick_res['code'] == 200
        assert cancel_block_after_pick_inventory == self.expect_inventory

    def test_13_cancel_oms_block_only_component_oms_order(self):
        """
        取消oms订单预占：只包含销售sku
        """
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(self.sale_sku, bom, self.sale_sku_count, self.sj_kw_ids,
                                            self.warehouse_id,
                                            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(self.sale_sku, self.warehouse_id,
                                                            self.to_warehouse_id)
        order_info = [(self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id,
        )

        oms_order_order_block_book_id = oms_order_block_res['data']['blockBookId']
        oms_order_order_block_source_no = oms_order_block_res['data']['sourceNo']

        cancel_oms_order_block_res = ims_request.cancel_oms_order_block(
            oms_order_order_block_book_id, oms_order_order_block_source_no
        )
        cancel_oms_order_block_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert cancel_oms_order_block_res['code'] == 200
        assert cancel_oms_order_block_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_14_cancel_delivery_order_block_only_component_oms_order_before_assign_stock(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_15_cancel_delivery_order_block_only_component_oms_order_before_assign_stock_ever_assigned(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )  # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        block_book_id = assign_stock_res['data'][0]['blockBookId']
        cancel_location_block = ims_request.only_cancel_location_block(block_book_id, self.delivery_code)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 2)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_location_block['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_16_cancel_delivery_order_block_only_component_oms_order_after_assign_stock(self):
        """包含配件sku和销售sku的出库单下发后，拣货前取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        block_ware_sku_list = ims_logics.get_combined_block_result_list(block_result_list)
        assign_stock_res = ims_request.assign_stock(self.delivery_code, block_ware_sku_list, self.warehouse_id)
        cancel_block_before_pick_res = ims_request.cancel_block_before_pick(self.delivery_code, 1)

        cancel_block_before_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_stock_res['code'] == 200
        assert cancel_block_before_pick_res['code'] == 200
        assert cancel_block_before_pick_inventory == self.expect_inventory

    def test_17_cancel_only_component_delivery_order_block_after_pick(self):
        """只包含部件sku的出库单下发后，拣货后取消"""
        # 采购入库生成销售sku现货库存
        ims_logics.add_lp_stock_by_other_in(
            self.sale_sku,
            bom,
            self.sale_sku_count,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        self.expect_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        order_info = [(self.component_sku, 1)]
        oms_order_block_res = ims_request.oms_order_block(
            order_info,
            self.warehouse_id
        )

        delivery_order_block_res = ims_request.delivery_order_block(
            self.delivery_code,
            order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']

        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims_logics.get_combined_block_result_list(block_result_list)
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims_request.assign_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for sj_location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            temp_dict = {
                "qty": qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
        confirm_pick_res = ims_logics.confirm_all_picked(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )

        cancel_block_after_pick_res = ims_request.cancel_block_after_pick(
            self.delivery_code,
            combined_block_result_list,
            self.yk_kw_id,
            self.warehouse_id
        )

        cancel_block_after_pick_inventory = ims_logics.get_lp_inventory(
            self.sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 构造期望库存数据
        for sj_location_id, (ware_sku, qty) in zip(self.sj_kw_ids, combined_block_result_list):
            # 释放库位库存,与最初的比，只需要直接把库位库存扣掉
            self.expect_inventory[ware_sku][sj_location_id]['stock'] -= qty
            # 上架库位库存最终转移到移库库位
            self.expect_inventory[ware_sku].update(
                {
                    self.yk_kw_id: {
                        "stock": qty,
                        "block": 0
                    },
                    # 拣货时库位库存转移到dock库存，取消后dock库存又转移到移库库位，所以相当于插入dock为0的库存数据
                    -self.warehouse_id: {'stock': 0, 'block': 0}
                })
        assert oms_order_block_res['code'] == 200
        assert delivery_order_block_res['code'] == 200
        assert assign_location_stock_res['code'] == 200
        assert confirm_pick_res['code'] == 200
        assert cancel_block_after_pick_res['code'] == 200
        assert cancel_block_after_pick_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
