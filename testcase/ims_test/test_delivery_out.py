import time
import pytest

from testcase import *


class TestDeliveryOut(object):
    def setup_class(self):
        self.ims = ims
        self.sale_sku_code = sale_sku_code
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.bom_version = bom_version
        self.bom_detail = bom_detail
        self.delivery_code = 'CK' + str(int(time.time() * 1000))
        self.sale_sku_count = 2
        self.sj_location_ids = fsj_location_ids

        # 干掉该销售sku的库存数据；
        self.ims.delete_ims_data(self.sale_sku_code)
        # 采购入库生成销售sku现货库存
        self.ims.add_stock_by_purchase_into_warehouse(
            self.sale_sku_code, self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)
        self.expect_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id)

    def test_1_oms_order_block(self):
        res = self.ims.oms_order_block(
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 预占中央库存、销售商品总库存
        self.expect_inventory["central_inventory_block"] += self.sale_sku_count
        self.expect_inventory["central_inventory_sale_block"] += self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_2_delivery_order_block(self):
        res = self.ims.delivery_order_block(
            self.delivery_code,
            self.sale_sku_code,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )

        for detail in self.bom_detail.items():
            # 预占仓库商品总库存
            self.expect_inventory[detail[0]]['total']['block'] += detail[1] * self.sale_sku_count
        # 预占现货库存
        self.expect_inventory['goods_inventory_spot_goods_block'] += self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_3_assign_location_stock(self):
        res = self.ims.assign_location_stock(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )
        for location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            # 预占库位库存
            self.expect_inventory[detail[0]][location_id]['block'] += detail[1] * self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_4_confirm_pick(self):
        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        for location_id, detail in zip(self.sj_location_ids, self.bom_detail.items()):
            pick_qty = detail[1] * self.sale_sku_count
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)

            # 释放库位库存
            self.expect_inventory[detail[0]][location_id]['block'] -= detail[1] * self.sale_sku_count
            self.expect_inventory[detail[0]][location_id]['stock'] -= detail[1] * self.sale_sku_count
            self.expect_inventory[detail[0]].update(
                {
                    -self.warehouse_id: {'block': 0, 'stock': pick_qty}
                }
            )

        confirm_pick_res = self.ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_5_delivery_out(self):
        # 执行发货
        res = self.ims.delivery_out(
            self.delivery_code,
            self.sale_sku_code,
            self.bom_version,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 获取库存数据
        current_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )
        # 释放中央总库存
        self.expect_inventory["central_inventory_stock"] -= self.sale_sku_count
        self.expect_inventory["central_inventory_block"] -= self.sale_sku_count
        # 释放销售商品总库存
        self.expect_inventory["central_inventory_sale_stock"] -= self.sale_sku_count
        self.expect_inventory["central_inventory_sale_block"] -= self.sale_sku_count
        # 释放销售商品现货库存
        self.expect_inventory["goods_inventory_spot_goods_stock"] -= self.sale_sku_count
        self.expect_inventory["goods_inventory_spot_goods_block"] -= self.sale_sku_count

        for detail in self.bom_detail.items():
            # 释放仓库商品总库存
            self.expect_inventory[detail[0]]['total']['stock'] -= detail[1] * self.sale_sku_count
            self.expect_inventory[detail[0]]['total']['block'] -= detail[1] * self.sale_sku_count

            # 扣掉dock库存
            self.expect_inventory[detail[0]][-self.warehouse_id]['stock'] -= detail[1] * self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
