import pytest

from testcase import *


class TestTransferToSelf:
    def setup_class(self):
        pass

    def setup(self):
        IMSDBOperator.delete_qualified_inventory([sale_sku])

    def test_1_delivery_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个发货仓"""
        trans_out_id = delivery_warehouse_id  # 调出仓id
        trans_out_to_id = delivery_warehouse_id  # 调出仓的目的仓id
        trans_in_id = delivery_warehouse_id  # 调入仓id
        trans_in_to_id = delivery_warehouse_id  # 调入仓的目的仓id
        trans_qty = 2  # 调拨的销售sku件数

        trans_out_sj_kw_ids = wms_logics.base_get_kw(1, 5, len(bom_detail), trans_out_id, trans_out_to_id)
        wms_request.common_switch_warehouse(trans_out_id)
        ims_logics.add_lp_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_ids, trans_out_id, trans_out_to_id)
        trans_out_expect_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)

        # 生成调拨需求
        demand_res = wms_request.transfer_out_create_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku,
            trans_qty)
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)
        assert trans_out_expect_inventory == trans_out_inventory

    def test_2_stock_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个备货仓"""
        trans_out_id = stock_warehouse_id  # 调出仓id
        trans_out_to_id = ''  # 调出仓的目的仓id
        trans_in_id = stock_warehouse_id  # 调入仓id
        trans_in_to_id = ''  # 调入仓的目的仓id

        trans_qty = 2  # 调拨的销售sku件数
        trans_out_sj_kw_ids = wms_logics.base_get_kw(1, 5, len(bom_detail), trans_out_id, trans_out_to_id)
        wms_request.common_switch_warehouse(trans_out_id)
        ims_logics.add_lp_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_ids, trans_out_id, trans_out_to_id)
        trans_out_expect_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)

        # 生成调拨需求
        demand_res = wms_request.transfer_out_create_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku,
            trans_qty)
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)
        assert trans_out_expect_inventory == trans_out_inventory

    def test_3_exchange_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个中转仓，但目的仓不一样"""
        trans_out_id = exchange_warehouse_id  # 调出仓id
        trans_out_to_id = straight_delivery_warehouse_id  # 调出仓的目的仓id
        trans_in_id = exchange_warehouse_id  # 调入仓id
        trans_in_to_id = delivery_warehouse_id  # 调入仓的目的仓id

        trans_qty = 2  # 调拨的销售sku件数
        trans_out_sj_kw_ids = wms_logics.base_get_kw(1, 5, len(bom_detail), trans_out_id, trans_out_to_id)
        wms_request.common_switch_warehouse(trans_out_id)
        ims_logics.add_lp_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_ids, trans_out_id, trans_out_to_id)
        trans_out_expect_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)

        # 生成调拨需求
        demand_res = wms_request.transfer_out_create_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku,
            trans_qty)
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims_logics.get_lp_inventory(sale_sku, trans_out_id, trans_out_to_id, bom)
        assert trans_out_expect_inventory == trans_out_inventory


if __name__ == '__main__':
    pytest.main()
