import pytest

from testcase import *


class TestFHCTransToOtherFHC:
    def setup_class(self):
        # 设定调出仓为发货仓，调入仓为不一样的发货仓
        self.trans_out_id = delivery_warehouse_id  # 调出仓id
        self.trans_out_to_id = delivery_warehouse_id  # 调出仓的目的仓id
        self.trans_in_id = delivery_warehouse_id2  # 调入仓id
        self.trans_in_to_id = delivery_warehouse_id2  # 调入仓的目的仓id

    def setup(self):
        wms_request.switch_default_warehouse(self.trans_out_id)

    def test_1_trans_multiple_goods_components_break_up_suite(self):
        """测试成套的库存，调拨出库配件后，导致库存不成套场景"""
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3)]
        transfer_demand_goods_list = [('BP63203684930A01', 1)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 1
        expect_trans_out_inventory["spot_goods_remain"] -= 1
        expect_trans_out_inventory["central_remain"] -= 1
        expect_trans_out_inventory["spot_goods_stock"] -= 1
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 0
        expect_trans_in_inventory['central_remain'] = 0
        expect_trans_in_inventory["spot_goods_stock"] = 0
        expect_trans_in_inventory["spot_goods_remain"] = 0

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_2_trans_multiple_goods_components_no_suite_broken_up(self):
        """测试有多余不成套配件，调拨出库配件后，不会拆成套的场景"""
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        transfer_demand_goods_list = [('BP63203684930A01', 1)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 0
        expect_trans_out_inventory["spot_goods_remain"] -= 0
        expect_trans_out_inventory["central_remain"] -= 0
        expect_trans_out_inventory["spot_goods_stock"] -= 0
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 0
        expect_trans_in_inventory['central_remain'] = 0
        expect_trans_in_inventory["spot_goods_stock"] = 0
        expect_trans_in_inventory["spot_goods_remain"] = 0

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_3_trans_multiple_goods_components_from_remain_and_break_up_suite(self):
        """测试调拨出库配件后，出了不成套的库存和拆散了成套的库存，导致库存不成套场景"""
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        transfer_demand_goods_list = [('BP63203684930A01', 2)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 1
        expect_trans_out_inventory["spot_goods_remain"] -= 1
        expect_trans_out_inventory["central_remain"] -= 1
        expect_trans_out_inventory["spot_goods_stock"] -= 1
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 0
        expect_trans_in_inventory['central_remain'] = 0
        expect_trans_in_inventory["spot_goods_stock"] = 0
        expect_trans_in_inventory["spot_goods_remain"] = 0

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_4_trans_multiple_goods_one_set_components(self):
        """测试多套不同bom库存，调拨成套配件场景"""
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3),
                            ('63203684930B01', 2), ('63203684930B02', 10)]
        transfer_demand_goods_list = [('BP63203684930A01', 1), ('BP63203684930A02', 5)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 1
        expect_trans_out_inventory["spot_goods_remain"] -= 1
        expect_trans_out_inventory["central_remain"] -= 1
        expect_trans_out_inventory["spot_goods_stock"] -= 1
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 1
        expect_trans_in_inventory['central_remain'] = 1
        expect_trans_in_inventory["spot_goods_stock"] = 1
        expect_trans_in_inventory["spot_goods_remain"] = 1

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_5_trans_multiple_goods_one_set_components_and_one_suite_with_different_bom_stock(self):
        """测试多bom库存，调拨成套的配件和销售sku场景，其中部件对应的bom版本库存等于部件成套库存"""
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3),
                            ('63203684930B01', 1),
                            ('63203684930B02', 5)]
        transfer_demand_goods_list = [('BP63203684930A01', 1), ('BP63203684930A02', 5), ('63203684930', 1)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 2
        expect_trans_out_inventory["spot_goods_remain"] -= 2
        expect_trans_out_inventory["central_remain"] -= 2
        expect_trans_out_inventory["spot_goods_stock"] -= 2
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 2
        expect_trans_in_inventory['central_remain'] = 2
        expect_trans_in_inventory["spot_goods_stock"] = 2
        expect_trans_in_inventory["spot_goods_remain"] = 2

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_6_trans_multiple_goods_one_set_components_and_two_suite_with_different_bom_stock(self):
        """测试多bom库存，调拨成套的配件和销售sku场景，其中部件对应的bom版本库存大于部件成套库存"""
        origin_inventory = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3),
                            ('63203684930B01', 2),
                            ('63203684930B02', 10)]
        transfer_demand_goods_list = [('BP63203684930A01', 1), ('BP63203684930A02', 5), ('63203684930', 2)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 3
        expect_trans_out_inventory["spot_goods_remain"] -= 3
        expect_trans_out_inventory["central_remain"] -= 3
        expect_trans_out_inventory["spot_goods_stock"] -= 3
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 3
        expect_trans_in_inventory['central_remain'] = 3
        expect_trans_in_inventory["spot_goods_stock"] = 3
        expect_trans_in_inventory["spot_goods_remain"] = 3

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_7_trans_multiple_goods_one_suite_and_all_remain_components(self):
        """测试成套的库存，调拨出库配件后，导致库存不成套场景"""
        origin_inventory = [('63203684930A01', 1), ('63203684930B01', 1), ('63203684930B02', 5)]
        transfer_demand_goods_list = [('BP63203684930A01', 1), ('63203684930', 1)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 1
        expect_trans_out_inventory["spot_goods_remain"] -= 1
        expect_trans_out_inventory["central_remain"] -= 1
        expect_trans_out_inventory["spot_goods_stock"] -= 1
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 1
        expect_trans_in_inventory['central_remain'] = 1
        expect_trans_in_inventory["spot_goods_stock"] = 1
        expect_trans_in_inventory["spot_goods_remain"] = 1

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_8_trans_multiple_goods_three_suites_with_one_bom_stock(self):
        """测试调拨多品单个bom库存"""
        origin_inventory = [('63203684930A01', 3), ('63203684930A02', 6), ('63203684930A02', 9)]
        transfer_demand_goods_list = [('63203684930', 3)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 3
        expect_trans_out_inventory["spot_goods_remain"] -= 3
        expect_trans_out_inventory["central_remain"] -= 3
        expect_trans_out_inventory["spot_goods_stock"] -= 3
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 3
        expect_trans_in_inventory['central_remain'] = 3
        expect_trans_in_inventory["spot_goods_stock"] = 3
        expect_trans_in_inventory["spot_goods_remain"] = 3

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_9_trans_multiple_goods_three_suites_with_two_bom_stock(self):
        """测试调拨多品多个bom库存"""
        origin_inventory = [('63203684930A01', 2), ('63203684930A02', 4), ('63203684930A02', 6),
                            ('63203684930B01', 1),
                            ('63203684930B02', 5)]
        transfer_demand_goods_list = [('63203684930', 3)]
        sale_sku = '63203684930'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 3
        expect_trans_out_inventory["spot_goods_remain"] -= 3
        expect_trans_out_inventory["central_remain"] -= 3
        expect_trans_out_inventory["spot_goods_stock"] -= 3
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 3
        expect_trans_in_inventory['central_remain'] = 3
        expect_trans_in_inventory["spot_goods_stock"] = 3
        expect_trans_in_inventory["spot_goods_remain"] = 3

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_10_trans_single_goods_with_components(self):
        """测试调拨多品多个bom库存"""
        origin_inventory = [('53170041592A01', 3), ]
        transfer_demand_goods_list = [('53170041592', 2), ('BP53170041592A01', 1)]
        sale_sku = '53170041592'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)]

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 3
        expect_trans_out_inventory["spot_goods_remain"] -= 3
        expect_trans_out_inventory["central_remain"] -= 3
        expect_trans_out_inventory["spot_goods_stock"] -= 3
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 3
        expect_trans_in_inventory['central_remain'] = 3
        expect_trans_in_inventory["spot_goods_stock"] = 3
        expect_trans_in_inventory["spot_goods_remain"] = 3

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory

    def test_11_trans_single_goods_without_components(self):
        """测试调拨多品多个bom库存"""
        origin_inventory = [('53170041592A01', 3), ]
        transfer_demand_goods_list = [('53170041592', 3)]
        sale_sku = '53170041592'
        IMSDBOperator.delete_qualified_inventory([sale_sku])
        trans_out_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(origin_inventory), self.trans_out_id, self.trans_out_to_id)]

        # 其他入库生成库存
        ims_request.lp_other_in(
            origin_inventory,
            trans_out_sj_kw_ids,
            self.trans_out_id,
            self.trans_out_to_id
        )
        expect_trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        expect_trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)

        # 生成调拨需求
        demand_list = list()
        for sku, qty in transfer_demand_goods_list:
            demand_res = wms_request.transfer_out_create_demand(
                self.trans_out_id,
                self.trans_out_to_id,
                self.trans_in_id,
                self.trans_in_to_id,
                sku,
                qty)
            assert demand_res['code'] == 200
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)

        # 创建调拨拣货单
        pick_order_res = wms_request.transfer_out_create_pick_order(demand_list, 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms_request.transfer_out_pick_order_detail(pick_order_code)['details']

        pick_sku_list = list()
        for detail in pick_order_details:
            #     for location_id, qty in pick_sku_dict[ware_sku].items():
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        assert confirm_pick_res['code'] == 200
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [wms_logics.db_get_kw(1, 3, len(pick_sku_list), self.trans_out_id, self.trans_out_to_id)]

        # 调拨拣货单按需装托提交
        submit_tray_res = wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        tray_id_list.sort(reverse=False)
        tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        finish_packing_res = wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms_request.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms_request.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms_request.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms_request.switch_default_warehouse(self.trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [wms_logics.db_get_kw(1, 5, len(pick_sku_list), self.trans_in_id, self.trans_in_to_id)]
        trans_in_sj_kw_codes = [wms_request.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        received_res = wms_request.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            shelf_res = wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)
            assert shelf_res['code'] == 200
        # --------------------------------调出仓库存更新--------------------------------#
        # 预占销售商品总库存、现货库存remain扣减
        expect_trans_out_inventory["central_stock"] -= 3
        expect_trans_out_inventory["spot_goods_remain"] -= 3
        expect_trans_out_inventory["central_remain"] -= 3
        expect_trans_out_inventory["spot_goods_stock"] -= 3
        # 按各个仓库sku预占仓库商品总库存
        for (ware_sku, qty, sj_kw_id), tp_kw_id in zip(pick_sku_list, tray_id_list):
            expect_trans_out_inventory[ware_sku]['warehouse_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku]['location_total']['stock'] -= qty
            expect_trans_out_inventory[ware_sku][sj_kw_id]['stock'] -= qty
            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            expect_trans_out_inventory[ware_sku].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # --------------------------------调入仓库存更新--------------------------------#
        # 调入仓销售商品总库存增加，库位总库存增加、库位库存增加，block为0
        expect_trans_in_inventory["central_stock"] = 3
        expect_trans_in_inventory['central_remain'] = 3
        expect_trans_in_inventory["spot_goods_stock"] = 3
        expect_trans_in_inventory["spot_goods_remain"] = 3

        for detail, in_sj_kw_id in zip(sorted_tray_sku_list, trans_in_sj_kw_ids):
            if detail['waresSkuCode'] not in expect_trans_in_inventory:
                expect_trans_in_inventory.update(
                    {
                        detail['waresSkuCode']: {
                            in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0},
                            'warehouse_total': {'stock': detail['skuQty'], 'block': 0},
                            'location_total': {'stock': detail['skuQty'], 'block': 0},
                            'transfer_on_way': {'stock': 0, 'block': 0}
                        }
                    }
                )
            else:
                expect_trans_in_inventory[detail['waresSkuCode']]['warehouse_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']]['location_total']['stock'] += detail['skuQty']
                expect_trans_in_inventory[detail['waresSkuCode']].update({
                    in_sj_kw_id: {'stock': detail['skuQty'], 'block': 0}
                })
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims_logics.query_lp_inventory(sale_sku, self.trans_in_id, self.trans_in_to_id)
        assert expect_trans_out_inventory == trans_out_inventory
        assert expect_trans_in_inventory == trans_in_inventory


if __name__ == '__main__':
    pytest.main()
