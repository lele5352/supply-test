import time
import pytest

from testcase import *


class TestTransferFromStockToDeliveryWarehouse(object):
    def setup_class(self):
        self.wms = wms
        self.ims = ims
        self.transfer_service = transfer_service

        # 初始化调出仓为备货仓，调入仓为发货仓
        self.delivery_warehouse_id = stock_warehouse_id
        self.delivery_target_warehouse_id = ''
        self.receive_warehouse_id = delivery_warehouse_id
        self.receive_target_warehouse_id = delivery_warehouse_id

        self.demand_qty = 2
        self.sj_location_id = self.wms.db_get_location_ids(5, 1, self.delivery_warehouse_id,
                                                           self.delivery_target_warehouse_id)

        self.sale_sku_code = sale_sku_code
        self.bom_version = bom_version
        self.bom_detail = self.ims.get_sale_sku_bom_detail(self.sale_sku_code, self.bom_version)
        self.tp_location_ids = self.wms.db_get_location_ids(3, len(self.bom_detail), self.delivery_warehouse_id,
                                                            self.delivery_target_warehouse_id)
        self.wms.switch_default_warehouse(self.delivery_warehouse_id)

    def setup(self):
        self.ims.delete_ims_data(self.sale_sku_code)
        self.ims.add_stock_by_other_in(self.sale_sku_code, self.bom_version, self.demand_qty, self.sj_location_id,
                                       self.delivery_warehouse_id, self.delivery_target_warehouse_id)
        self.expect_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version,
                                                               self.delivery_warehouse_id,
                                                               self.delivery_target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_create_transfer_demand(self):
        """测试创建调拨需求从备货仓调往发货仓"""
        # 生成调拨需求
        demand_res = self.transfer_service.create_transfer_demand(
            self.wms.db_warehouse_id_to_code(self.delivery_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_warehouse_id),
            self.sale_sku_code,
            self.demand_qty,
            self.wms.db_warehouse_id_to_code(self.delivery_target_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_target_warehouse_id)
        )
        assert demand_res['code'] == 200
        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.demand_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.demand_qty
        for detail in self.bom_detail.items():
            # 按各个仓库sku预占仓库商品总库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.demand_qty
        ims_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, self.delivery_warehouse_id,
                                                       self.delivery_target_warehouse_id)
        assert self.expect_inventory == ims_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_create_transfer_pick_order(self):
        """测试调拨需求创建后将该需求创建纸质拣货单"""
        # 生成调拨需求
        demand_res = self.transfer_service.create_transfer_demand(
            self.wms.db_warehouse_id_to_code(self.delivery_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_warehouse_id),
            self.sale_sku_code,
            self.demand_qty,
            self.wms.db_warehouse_id_to_code(self.delivery_target_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_target_warehouse_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = self.wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.demand_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.demand_qty
        for detail in self.bom_detail.items():
            # 按仓库sku预占仓库商品总库存、库位库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.demand_qty
            self.expect_inventory[detail[0]][self.sj_location_id]['block'] += detail[1] * self.demand_qty
        ims_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, self.delivery_warehouse_id,
                                                       self.delivery_target_warehouse_id)
        assert self.expect_inventory == ims_inventory

    # @pytest.mark.skip(reason='test')
    def test_3_pick_order_confirm_pick(self):
        """测试生成调拨需求、然后创建纸质拣货单再确认拣货"""
        # 生成调拨需求
        demand_res = self.transfer_service.create_transfer_demand(
            self.wms.db_warehouse_id_to_code(self.delivery_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_warehouse_id),
            self.sale_sku_code,
            self.demand_qty,
            self.wms.db_warehouse_id_to_code(self.delivery_target_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_target_warehouse_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = self.wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = self.wms.transfer_pick_order_assign_pick_user([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = self.wms.transfer_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = self.wms.transfer_pick_order_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.demand_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.demand_qty
        for detail in self.bom_detail.items():
            # 预占仓库商品总库存,stock从库位移动到dock，需要减去库位上的stock
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.demand_qty
            self.expect_inventory[detail[0]][self.sj_location_id]['stock'] -= detail[1] * self.demand_qty
            self.expect_inventory[detail[0]].update(
                {
                    -self.delivery_warehouse_id: {'block': 0, 'stock': detail[1] * self.demand_qty}
                }
            )
        ims_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, self.delivery_warehouse_id,
                                                       self.delivery_target_warehouse_id)
        assert self.expect_inventory == ims_inventory

    # @pytest.mark.skip(reason='test')
    def test_4_pick_order_submit_tray(self):
        """测试创建调拨需求，然后创建调拨拣货单再确认拣货，然后拣货单完成按需装托提交"""
        # 生成调拨需求
        demand_res = self.transfer_service.create_transfer_demand(
            self.wms.db_warehouse_id_to_code(self.delivery_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_warehouse_id),
            self.sale_sku_code,
            self.demand_qty,
            self.wms.db_warehouse_id_to_code(self.delivery_target_warehouse_id),
            self.wms.db_warehouse_id_to_code(self.receive_target_warehouse_id)
        )
        assert demand_res['code'] == 200
        demand_no = demand_res['data']['demandCode']

        # 创建调拨拣货单
        pick_order_res = self.wms.create_transfer_pick_order([demand_no], 1)
        assert pick_order_res['code'] == 200
        pick_order_code = pick_order_res['data']

        # 分配调拨拣货人
        assign_pick_user_res = self.wms.transfer_pick_order_assign_pick_user([pick_order_code], 'admin', 1)
        assert assign_pick_user_res['code'] == 200

        # 获取调拨拣货单详情数据
        pick_order_details = self.wms.transfer_pick_order_detail(pick_order_code)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = self.wms.transfer_pick_order_confirm_pick(pick_order_details)
        assert confirm_pick_res['code'] == 200

        # 调拨拣货单按需装托提交
        submit_tray_res = self.wms.transfer_submit_tray(pick_order_details, self.tp_location_ids)
        assert submit_tray_res['code'] == 200

        # 预占销售商品总库存、现货库存
        self.expect_inventory["central_inventory_sale_block"] += self.demand_qty
        self.expect_inventory["goods_inventory_spot_goods_block"] += self.demand_qty
        for detail, tp_location_id in zip(self.bom_detail.items(), self.tp_location_ids):
            # 按仓库sku预占仓库商品总库存；上架库位库存转移到dock，扣掉对应库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.demand_qty
            self.expect_inventory[detail[0]][self.sj_location_id]['stock'] -= detail[1] * self.demand_qty

            # 更新期望库存：插入托盘库位库存和dock库存，库存是先进dock，再从dock到托盘库位，所以dock插入stock为0
            self.expect_inventory[detail[0]].update(
                {
                    -self.delivery_warehouse_id: {'block': 0, 'stock': 0},
                    tp_location_id: {'block': 0, 'stock': detail[1] * self.demand_qty}
                }
            )
        ims_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, self.delivery_warehouse_id,
                                                       self.delivery_target_warehouse_id)
        assert self.expect_inventory == ims_inventory


if __name__ == '__main__':
    pytest.main()
