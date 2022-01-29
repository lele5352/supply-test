import time
import pytest

from testcase import *


class TestTransfer(object):
    def setup_class(self):
        self.wms = wms
        self.ims = ims
        self.transfer_service = transfer_service

        self.sale_sku_code = sale_sku_code
        self.bom_version = bom_version
        self.bom_detail = self.ims.get_sale_sku_bom_detail(self.sale_sku_code, self.bom_version)

    def setup(self):
        self.ims.delete_ims_data(self.sale_sku_code)

    # @pytest.mark.skip(reason='test')
    def test_1_transfer_from_stock_to_delivery_warehouse(self):
        """测试从备货仓调往发货仓"""
        # 从备货仓调拨库存到发货仓
        demand_qty = 2
        sj_location_id = self.wms.db_get_location_ids(5, 1, stock_warehouse_id, '')
        # 初始化对应库存
        self.ims.add_stock_by_other_in(self.sale_sku_code, self.bom_version, demand_qty, sj_location_id,
                                       stock_warehouse_id, '')
        expect_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, stock_warehouse_id, '')

        demand_res = self.transfer_service.create_transfer_demand(
            self.wms.db_warehouse_id_to_code(stock_warehouse_id),
            self.wms.db_warehouse_id_to_code(delivery_warehouse_id),
            sale_sku_code,
            demand_qty,
            '',
            self.wms.db_warehouse_id_to_code(delivery_warehouse_id)
        )
        # 预占销售商品总库存、现货库存
        expect_inventory["central_inventory_sale_block"] += demand_qty
        expect_inventory["goods_inventory_spot_goods_block"] += demand_qty
        expect_inventory["central_inventory_sale_block"] += demand_qty
        for detail in self.bom_detail.items():
            # 预占仓库商品总库存
            expect_inventory[detail[0]]['total']['block'] += detail[1] * demand_qty
        ims_inventory = self.ims.get_current_inventory(self.sale_sku_code, self.bom_version, stock_warehouse_id, '')

        assert demand_res['code'] == 200
        assert expect_inventory == ims_inventory


if __name__ == '__main__':
    pytest.main()
