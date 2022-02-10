import pytest

from testcase import *


class TestTransferToSelf:
    def setup_class(self):
        pass

    def setup(self):
        ims.delete_qualified_inventory(sale_sku)

    def test_1_delivery_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个发货仓"""
        trans_out_id = delivery_warehouse_id  # 调出仓id
        trans_out_target_id = delivery_warehouse_id  # 调出仓的目的仓id
        trans_in_id = delivery_warehouse_id  # 调入仓id
        trans_in_target_id = delivery_warehouse_id  # 调入仓的目的仓id

        trans_qty = 2  # 调拨的销售sku件数
        trans_out_sj_kw_id = wms.db_get_kw(1, 5, 1, trans_out_id, trans_out_target_id)
        wms.switch_default_warehouse(trans_out_id)
        ims.add_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_id, trans_out_id, trans_out_target_id)
        trans_out_expect_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)

        # 生成调拨需求
        demand_res = transfer.transfer_out_create_demand(
            wms.db_ck_id_to_code(trans_out_id),
            wms.db_ck_id_to_code(trans_in_id),
            sale_sku,
            trans_qty,
            wms.db_ck_id_to_code(trans_out_target_id),
            wms.db_ck_id_to_code(trans_in_target_id)
        )
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)
        assert trans_out_expect_inventory == trans_out_inventory

    def test_2_stock_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个备货仓"""
        trans_out_id = stock_warehouse_id  # 调出仓id
        trans_out_target_id = ''  # 调出仓的目的仓id
        trans_in_id = stock_warehouse_id  # 调入仓id
        trans_in_target_id = ''  # 调入仓的目的仓id

        trans_qty = 2  # 调拨的销售sku件数
        trans_out_sj_kw_id = wms.db_get_kw(1, 5, 1, trans_out_id, trans_out_target_id)
        wms.switch_default_warehouse(trans_out_id)
        ims.add_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_id, trans_out_id, trans_out_target_id)
        trans_out_expect_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)

        # 生成调拨需求
        demand_res = transfer.transfer_out_create_demand(
            wms.db_ck_id_to_code(trans_out_id),
            wms.db_ck_id_to_code(trans_in_id),
            sale_sku,
            trans_qty,
            wms.db_ck_id_to_code(trans_out_target_id),
            wms.db_ck_id_to_code(trans_in_target_id)
        )
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)
        assert trans_out_expect_inventory == trans_out_inventory

    def test_3_exchange_warehouse_trans_to_itself(self):
        """测试调出仓和调入仓为同个中转仓，但目的仓不一样"""
        trans_out_id = exchange_warehouse_id  # 调出仓id
        trans_out_target_id = straight_delivery_warehouse_id  # 调出仓的目的仓id
        trans_in_id = exchange_warehouse_id  # 调入仓id
        trans_in_target_id = delivery_warehouse_id  # 调入仓的目的仓id

        trans_qty = 2  # 调拨的销售sku件数
        trans_out_sj_kw_id = wms.db_get_kw(1, 5, 1, trans_out_id, trans_out_target_id)
        wms.switch_default_warehouse(trans_out_id)
        ims.add_stock_by_other_in(sale_sku, bom, trans_qty, trans_out_sj_kw_id, trans_out_id, trans_out_target_id)
        trans_out_expect_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)

        # 生成调拨需求
        demand_res = transfer.transfer_out_create_demand(
            wms.db_ck_id_to_code(trans_out_id),
            wms.db_ck_id_to_code(trans_in_id),
            sale_sku,
            trans_qty,
            wms.db_ck_id_to_code(trans_out_target_id),
            wms.db_ck_id_to_code(trans_in_target_id)
        )
        assert demand_res['code'] == 57587
        assert demand_res['message'] == "发货仓和收货仓不能相同"
        assert demand_res['data'] is None

        # 调拨需求下发失败，库存不变
        trans_out_inventory = ims.get_inventory(sale_sku, bom, trans_out_id, trans_out_target_id)
        assert trans_out_expect_inventory == trans_out_inventory


if __name__ == '__main__':
    pytest.main()
