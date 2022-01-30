import pytest

from testcase import *


class TestTransferFromStockToDeliveryWarehouse(object):
    def setup_class(self):
        # 初始化调出仓为备货仓，调入仓为发货仓
        self.trans_out_id = stock_warehouse_id  # 调出仓id
        self.trans_out_target_id = ''  # 调出仓的目的仓id
        self.trans_in_id = delivery_warehouse_id  # 调入仓id
        self.trans_in_target_id = delivery_warehouse_id  # 调入仓的目的仓id
        self.trans_qty = 2  # 调拨的销售sku件数

        self.sj_kw_id = bsj_kw_ids[0]
        self.tp_kw_ids = btp_kw_ids
        wms.switch_default_warehouse(self.trans_out_id)

    def setup(self):
        ims.delete_ims_data(sale_sku)
        ims.add_stock_by_other_in(sale_sku, bom, self.trans_qty, self.sj_kw_id, self.trans_out_id,
                                  self.trans_out_target_id)
        self.expect_inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_target_id)

    # @pytest.mark.skip(reason='test')
    def test_1_create_transfer_demand(self):
        """测试创建调拨需求从备货仓调往发货仓"""
        # 生成调拨需求
        demand_res = transfer.create_transfer_demand(
            wms.db_ck_id_to_code(self.trans_out_id),
            wms.db_ck_id_to_code(self.trans_in_id),
            sale_sku,
            self.trans_qty,
            wms.db_ck_id_to_code(self.trans_out_target_id),
            wms.db_ck_id_to_code(self.trans_in_target_id)
        )
        assert demand_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.trans_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 按各个仓库sku预占仓库商品总库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
        inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_target_id)
        assert self.expect_inventory == inventory

    # @pytest.mark.skip(reason='test')
    def test_2_create_transfer_pick_order(self):
        """测试调拨需求创建后将该需求创建纸质拣货单"""
        # 生成调拨需求
        demand_res = transfer.create_transfer_demand(
            wms.db_ck_id_to_code(self.trans_out_id),
            wms.db_ck_id_to_code(self.trans_in_id),
            sale_sku,
            self.trans_qty,
            wms.db_ck_id_to_code(self.trans_out_target_id),
            wms.db_ck_id_to_code(self.trans_in_target_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.trans_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 按仓库sku预占仓库商品总库存、库位库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.expect_inventory[detail[0]][self.sj_kw_id]['block'] += detail[1] * self.trans_qty
        inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_target_id)
        assert self.expect_inventory == inventory

    # @pytest.mark.skip(reason='test')
    def test_3_pick_order_confirm_pick(self):
        """测试生成调拨需求、然后创建纸质拣货单再确认拣货"""
        # 生成调拨需求
        demand_res = transfer.create_transfer_demand(
            wms.db_ck_id_to_code(self.trans_out_id),
            wms.db_ck_id_to_code(self.trans_in_id),
            sale_sku,
            self.trans_qty,
            wms.db_ck_id_to_code(self.trans_out_target_id),
            wms.db_ck_id_to_code(self.trans_in_target_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_pick_order_assign_pick_user([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_pick_order_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.trans_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.trans_qty
        for detail in bom_detail.items():
            # 预占仓库商品总库存,stock从库位移动到dock，需要减去库位上的stock
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.expect_inventory[detail[0]][self.sj_kw_id]['stock'] -= detail[1] * self.trans_qty
            self.expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_target_id)
        assert self.expect_inventory == inventory

    # @pytest.mark.skip(reason='test')
    def test_4_pick_order_submit_tray(self):
        """测试创建调拨需求，然后创建调拨拣货单再确认拣货，然后拣货单完成按需装托提交"""
        # 生成调拨需求
        demand_res = transfer.create_transfer_demand(
            wms.db_ck_id_to_code(self.trans_out_id),
            wms.db_ck_id_to_code(self.trans_in_id),
            sale_sku,
            self.trans_qty,
            wms.db_ck_id_to_code(self.trans_out_target_id),
            wms.db_ck_id_to_code(self.trans_in_target_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = wms.transfer_pick_order_assign_pick_user([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = wms.transfer_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = wms.transfer_pick_order_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = wms.transfer_submit_tray(pick_order_details, self.tp_kw_ids)
        assert submit_tray_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.trans_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.trans_qty
        for detail, tp_location_id in zip(bom_detail.items(), self.tp_kw_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.trans_qty
            self.expect_inventory[detail[0]][self.sj_kw_id]['stock'] -= detail[1] * self.trans_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.expect_inventory[detail[0]].update(
                {
                    -self.trans_out_id: {'block': 0, 'stock': 0},
                    tp_location_id: {'block': 0, 'stock': detail[1] * self.trans_qty}
                }
            )
        inventory = ims.get_inventory(sale_sku, bom, self.trans_out_id, self.trans_out_target_id)
        assert self.expect_inventory == inventory


if __name__ == '__main__':
    pytest.main()
