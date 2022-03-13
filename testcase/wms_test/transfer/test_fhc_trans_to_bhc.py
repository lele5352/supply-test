import pytest

from testcase import *


class TestFHCTransToBHC:
    def setup_class(self):
        # 设定调出仓为发货仓，调入仓为备货仓
        self.trans_out_id = delivery_warehouse_id  # 调出仓id
        self.trans_out_to_id = delivery_warehouse_id  # 调出仓的目的仓id
        self.trans_in_id = stock_warehouse_id  # 调入仓id
        self.trans_in_to_id = ''  # 调入仓的目的仓id
        self.trans_qty = 2  # 调拨的销售sku件数

        self.trans_out_sj_kw_id = wms.db_get_kw(1, 5, 1, self.trans_out_id, self.trans_out_to_id)
        self.trans_out_tp_kw_ids = wms.db_get_kw(1, 3, len(bom_detail), self.trans_out_id, self.trans_out_to_id)

        self.trans_in_sj_kw_id = wms.db_get_kw(1, 5, 1, self.trans_in_id, self.trans_in_to_id)
        self.trans_in_sj_kw_code = wms.db_get_kw(2, 5, 1, self.trans_in_id, self.trans_in_to_id)

    def setup(self):
        wms.switch_default_warehouse(self.trans_out_id)
        ims.delete_qualified_inventory([sale_sku])
        ims.add_qualified_stock_by_other_in(sale_sku, bom, self.trans_qty, self.trans_out_sj_kw_id, self.trans_out_id,
                                            self.trans_out_to_id)
        self.trans_out_expect_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        self.trans_in_expect_inventory = ims.get_inventory(sale_sku, bom, self.trans_in_id, self.trans_in_to_id)

    def test_1_create_transfer_demand(self):
        """测试调拨流程执行到生成调拨需求"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 按各个仓库sku预占仓库商品总库存
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_2_create_transfer_pick_order(self):
        """测试调拨调拨流程执行到创建纸质拣货单"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 按仓库sku预占仓库商品总库存、库位库存
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['block'] += detail[1] * self.trans_qty
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_3_pick_order_confirm_pick(self):
        """测试调拨流程执行到确认拣货"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 预占仓库商品总库存,stock从库位移动到dock，需要减去库位上的stock
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_4_pick_order_submit_tray(self):
        """测试调拨流程执行到装托完成"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_5_pick_order_finish_packing(self):
        """测试调拨执行到生成调拨出库单"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = wms.transfer_out_finish_packing(pick_order_code, tray_list)
        assert finish_packing_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_6_transfer_out_order_review(self):
        """测试调拨执行到完成调拨复核"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = wms.transfer_out_finish_packing(pick_order_code, tray_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]

        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.trans_out_expect_inventory["central_block"] += self.trans_qty
        self.trans_out_expect_inventory["spot_goods_block"] += self.trans_qty
        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.trans_out_expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory

    def test_7_transfer_delivery(self):
        """测试调拨流程执行到调拨出库发货交接完成"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = wms.transfer_out_finish_packing(pick_order_code, tray_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]

        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 调出仓销售商品总库存、现货库存扣减；；
        self.trans_out_expect_inventory["central_stock"] -= self.trans_qty
        self.trans_out_expect_inventory["spot_goods_stock"] -= self.trans_qty
        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.trans_out_expect_inventory[detail[0]]['total']['stock'] -= detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # 调入仓销售商品总库存增加，调拨在途增加
        self.trans_in_expect_inventory["central_stock"] += self.trans_qty
        self.trans_in_expect_inventory["transfer_on_way_stock"] += self.trans_qty

        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims.get_inventory(sale_sku, bom, self.trans_in_id, self.trans_in_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory
        assert self.trans_in_expect_inventory == trans_in_inventory

    def test_8_transfer_in_received(self):
        """测试调拨流程执行到调拨入库收货"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = wms.transfer_out_finish_packing(pick_order_code, tray_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]

        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms.switch_default_warehouse(self.trans_in_id)
        # 调拨入库收货
        received_res = wms.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调出仓销售商品总库存、现货库存扣减；；
        self.trans_out_expect_inventory["central_stock"] -= self.trans_qty
        self.trans_out_expect_inventory["spot_goods_stock"] -= self.trans_qty
        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.trans_out_expect_inventory[detail[0]]['total']['stock'] -= detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
        # 调入仓销售商品总库存增加，调拨在途增加
        self.trans_in_expect_inventory["central_stock"] += self.trans_qty
        self.trans_in_expect_inventory["transfer_on_way_stock"] += self.trans_qty

        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims.get_inventory(sale_sku, bom, self.trans_in_id, self.trans_in_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory
        assert self.trans_in_expect_inventory == trans_in_inventory

    def test_9_transfer_in_up_shelf(self):
        """测试调拨流程执行到调拨入库收货"""
        # 生成调拨需求
        demand_res = wms.transfer_out_create_demand(
            self.trans_out_id,
            self.trans_out_to_id,
            self.trans_in_id,
            self.trans_in_to_id,
            sale_sku,
            self.trans_qty)
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.transfer_out_create_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_out_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_out_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_out_submit_tray(pick_order_details, self.trans_out_tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 查看整单获取已装托的托盘
        tray_detail_res = wms.transfer_out_pick_order_tray_detail(pick_order_code)
        assert tray_detail_res['code'] == 200

        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = wms.transfer_out_finish_packing(pick_order_code, tray_list)
        assert finish_packing_res['code'] == 200
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']

        transfer_out_order_detail_res = wms.transfer_out_order_detail(transfer_out_order_no)
        assert transfer_out_order_detail_res['code'] == 200
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]

        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_res = wms.transfer_out_order_review(box_no, tray_code)
            assert review_res['code'] == 200

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = wms.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            assert bind_res['code'] == 200
            handover_no = bind_res['data']['handoverNo']

        delivery_res = wms.transfer_out_delivery(handover_no)
        assert delivery_res['code'] == 200

        # 切换仓库到调入仓
        wms.switch_default_warehouse(self.trans_in_id)
        # 调拨入库收货
        received_res = wms.transfer_in_received(handover_no)
        assert received_res['code'] == 200

        # 调拨入库按箱单逐个整箱上架
        for detail in details:
            shelf_res = wms.transfer_in_up_shelf(detail[0], self.trans_in_sj_kw_code)
            assert shelf_res['code'] == 200

        # 调出仓销售商品总库存、现货库存扣减；；
        self.trans_out_expect_inventory["central_stock"] -= self.trans_qty
        self.trans_out_expect_inventory["spot_goods_stock"] -= self.trans_qty
        # 调入仓销售商品总库存增加，现货库存增加，仓库商品总库存增加，仓库库位库存增加
        self.trans_in_expect_inventory["central_stock"] += self.trans_qty
        self.trans_in_expect_inventory["spot_goods_stock"] += self.trans_qty

        for detail, tp_kw_id in zip(bom_detail.items(), self.trans_out_tp_kw_ids):
            # 调出仓扣除仓库商品总库存、库位库存
            self.trans_out_expect_inventory[detail[0]]['total']['stock'] -= detail[1] * self.trans_qty
            self.trans_out_expect_inventory[detail[0]][self.trans_out_sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新调出仓期望库存：插入托盘库位库存和dock库存，插入stock为0
            self.trans_out_expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_kw_id: {'block': 0, 'stock': 0}
                }
            )
            # 更新调入仓期望库存：插入仓库商品总库存和库位库存
            self.trans_in_expect_inventory.update(
                {
                    detail[0]: {
                        'total': {'block': 0, 'stock': detail[1] * self.trans_qty},
                        self.trans_in_sj_kw_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                    }
                }
            )
        # 获取当前最新库存数据，比对预期数据
        trans_out_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_to_id)
        trans_in_inventory = ims.get_inventory(sale_sku, bom, self.trans_in_id, self.trans_in_to_id)
        assert self.trans_out_expect_inventory == trans_out_inventory
        assert self.trans_in_expect_inventory == trans_in_inventory


if __name__ == '__main__':
    pytest.main()
