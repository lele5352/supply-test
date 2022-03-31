import time
import pytest

from testcase import *


class TestSalesOutboundOrderDelivery(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id

    def setup(self):
        self.delivery_code = 'CK' + str(int(time.time() * 1000))

    def test_1_reissue_order_delivered_break_up_suite(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单,导致不成套
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3)]
        delivery_order_goods_list = [('BP63203684930A01', 1)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        print(after_oms_block_inventory)
        # 补发单生成只预占仓库商品总库存，更新remain
        for ware_sku, qty in delivery_order_goods_list:
            self.expect_inventory[ware_sku.replace('BP', '')]["warehouse_total"]['block'] += qty
        self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['location_total']['block'] += qty
        self.expect_inventory['spot_goods_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory

        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']

        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            self.expect_inventory[ware_sku].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                }
            )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_2_reissue_order_delivered_no_suite_broken_up(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单，只出多余出来不成套的部分
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        delivery_order_goods_list = [('BP63203684930A01', 1)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 补发单生成只预占仓库商品总库存，此处场景不会拆成套，不扣remain
        for ware_sku, qty in delivery_order_goods_list:
            self.expect_inventory[ware_sku.replace('BP', '')]["warehouse_total"]['block'] += qty
        # self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，此处场景不会拆成套，不扣现货remain
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['location_total']['block'] += qty
        # self.expect_inventory['spot_goods_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory

        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']

        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            self.expect_inventory[ware_sku].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                }
            )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        # self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        # self.expect_inventory["spot_goods_stock"] -= 1
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_3_reissue_order_delivered_not_in_suite_part_and_break_up_suite(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单，同时出不成套部分且把成套的拆不成套
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        delivery_order_goods_list = [('BP63203684930A01', 1), ('BP63203684930A02', 1)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 补发单生成只预占仓库商品总库存，更新remain
        for ware_sku, qty in delivery_order_goods_list:
            self.expect_inventory[ware_sku.replace('BP', '')]["warehouse_total"]['block'] += qty
        self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['location_total']['block'] += qty
        self.expect_inventory['spot_goods_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory

        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )

        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']

        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            self.expect_inventory[ware_sku].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                }
            )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_4_mixed_sku_order_delivered_with_less_than_one_suite_components(self):
        """
        测试场景：一套多一个部件库存放在多个不同库位，出库单中包含一套多一个补件，同时出完
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        delivery_order_goods_list = [('63203684930', 1), ('BP63203684930A01', 1)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 1
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] -= 1
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_5_mixed_sku_order_delivered_with_one_suite_components(self):
        """
        测试场景：2套不同bom库存放在多个不同库位，出库单中包含1套和多个组成1套的部件，同时出完
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3), ('63203684930B01', 1),
                            ('63203684930B02', 5)]
        delivery_order_goods_list = [('63203684930', 1), ('BP63203684930B01', 1), ('BP63203684930B02', 5)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty
        self.expect_inventory["central_remain"] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 2
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] -= 1
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 2
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 2
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_6_mixed_sku_order_delivered_with_one_suite_components(self):
        """
        测试场景：3套不同bom库存放在多个不同库位，出库单中包含2套和多个组成1套的部件，同时出完
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3), ('63203684930B01', 2),
                            ('63203684930B02', 10)]
        delivery_order_goods_list = [('63203684930', 2), ('BP63203684930B01', 1), ('BP63203684930B02', 5)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty
        self.expect_inventory["central_remain"] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 3
        self.expect_inventory['central_remain'] -= 2
        self.expect_inventory['central_block'] -= 2
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 3
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 3
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_7_mixed_sku_order_delivered_with_two_different_bom_components(self):
        """
        测试场景：3套不同bom库存放在多个不同库位，出库单中包含1套和多个不同bom组成2套的部件，同时出完
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3), ('63203684930B01', 2),
                            ('63203684930B02', 10)]
        delivery_order_goods_list = [('63203684930', 1), ('BP63203684930B01', 1), ('BP63203684930B02', 5),
                                     ('BP63203684930A01', 1), ('BP63203684930A02', 5)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty
        self.expect_inventory["central_remain"] -= 2

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 3
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] -= 1
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 3
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 3
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_8_multiple_goods_sales_order_delivered_without_components(self):
        """
        测试场景：一套多一个部件库存放在多个不同库位，出库单中包含一套，同时出完
        """
        sale_sku = '63203684930'
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3)]
        delivery_order_goods_list = [('63203684930', 1)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 1
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] -= 1
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_9_single_goods_sales_order_delivered_without_components(self):
        """
        测试场景：多套单品库存放在多个不同库位，出库单中包含多套该单品，同时出完
        """
        sale_sku = '53170041592'  # 单品销售sku
        origin_inventory = [('53170041592A01', 1), ('53170041592A01', 2), ('53170041592A01', 3)]
        delivery_order_goods_list = [('53170041592', 6)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= delivery_order_goods_list[0][1]
        self.expect_inventory['central_remain'] -= delivery_order_goods_list[0][1]
        self.expect_inventory['central_block'] -= delivery_order_goods_list[0][1]
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= delivery_order_goods_list[0][1]
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= delivery_order_goods_list[0][1]
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory

    def test_10_single_goods_sales_order_delivered_with_components(self):
        """
        测试场景：多套单品库存放在多个不同库位，出库单中包含多套该单品，同时出完
        """
        sale_sku = '53170041592'  # 单品销售sku
        origin_inventory = [('53170041592A01', 1), ('53170041592A01', 2), ('53170041592A01', 3)]
        delivery_order_goods_list = [('53170041592', 2), ('BP53170041592A01', 4)]
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory,
            sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms补发订单生成，预占
        res = ims.oms_order_block(
            delivery_order_goods_list,
            self.warehouse_id,
        )
        # 获取库存数据
        after_oms_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sku, qty in delivery_order_goods_list:
            if sku.startswith("BP"):
                # 补发单生成只预占仓库商品总库存
                self.expect_inventory[sku.replace('BP', '')]["warehouse_total"]['block'] += qty
            else:
                # 销售sku更新block
                self.expect_inventory["central_block"] += qty
        self.expect_inventory['central_remain'] -= 4
        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

        delivery_order_block_res = ims.delivery_order_block(
            self.delivery_code,
            delivery_order_goods_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 销售出库单预占分配库存的结果列表
        block_result_list = delivery_order_block_res['data']['wareSkuList']
        # 把分配库存的预占结果按仓库sku维度聚合
        combined_block_result_list = ims.get_combined_block_result_list(block_result_list)

        # 获取库存数据
        after_delivery_order_block_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        for block_result in block_result_list:
            if block_result['goodsSkuCode'].startswith('BP'):
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
            else:
                self.expect_inventory[block_result['wareSkuCode']]['location_total']['block'] += block_result['qty']
                self.expect_inventory[block_result['wareSkuCode']]['warehouse_total']['block'] += block_result['qty']
        self.expect_inventory['spot_goods_remain'] -= 6
        self.expect_inventory['central_remain'] -= 2
        self.expect_inventory['central_block'] -= 2
        assert res['code'] == 200
        assert self.expect_inventory == after_delivery_order_block_inventory
        # 分配库位库存，预占库位库存
        assign_location_stock_res = ims.assign_location_stock(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id
        )
        # 获取库存数据
        after_assign_stock_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 构造拣货sku明细数据，拣货明细从分配库存响应数据中提取,此处为完整拣货，非短拣；
        assigned_sku_list = assign_location_stock_res['data'][0]['wareSkuList']
        # 预占库位库存
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            self.expect_inventory[ware_sku][location_id]['block'] += qty
        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        assert res['code'] == 200
        assert self.expect_inventory == after_assign_stock_inventory

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            assigned_sku_list,
            self.warehouse_id
        )
        # 构造拣货后期望库存数据
        for pick_ware_sku in assigned_sku_list:
            ware_sku = pick_ware_sku['wareSkuCode']
            pick_qty = pick_ware_sku['qty']
            location_id = int(pick_ware_sku['storageLocationId'])
            # 释放库位库存
            self.expect_inventory[ware_sku][location_id]['block'] -= pick_qty
            self.expect_inventory[ware_sku][location_id]['stock'] -= pick_qty
            if -self.warehouse_id in self.expect_inventory[ware_sku]:
                self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] += pick_qty
            else:
                self.expect_inventory[ware_sku].update(
                    {
                        -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                    }
                )
        # 获取库存数据
        after_pick_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert self.expect_inventory == after_pick_inventory

        # 执行发货
        delivery_res = ims.delivery_out(
            self.delivery_code,
            combined_block_result_list,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        after_delivered_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 6
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 6
        # 释放仓库商品总库存
        for ware_sku, qty in combined_block_result_list:
            self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['warehouse_total']['block'] -= qty
            self.expect_inventory[ware_sku]['location_total']['stock'] -= qty
            self.expect_inventory[ware_sku]['location_total']['block'] -= qty

            # 扣掉dock库存
            self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= qty

        assert delivery_res['code'] == 200
        assert self.expect_inventory == after_delivered_inventory


if __name__ == '__main__':
    pytest.main()
