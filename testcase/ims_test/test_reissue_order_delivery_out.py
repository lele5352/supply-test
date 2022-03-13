import time
import pytest

from testcase import *


class TestReissueOrderDeliveryOut(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id

    def setup(self):
        self.delivery_code = 'CK' + str(int(time.time() * 1000))

    def test_reissue_order_delivery_break_up_suite(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单,导致不成套
        """

        origin_inventory_info = [('63203684930A01', 1), ('63203684930A02', 2), ('63203684930A02', 3)]
        reissue_order_info = [('BP63203684930A01', 1)]
        ware_sku = '63203684930A01'
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory_info), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory_info,
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
            reissue_order_info,
            self.warehouse_id,
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 补发单生成只预占仓库商品总库存，更新remain
        self.expect_inventory[ware_sku]["warehouse_total"]['block'] += reissue_order_info[0][1]
        self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        res = ims.delivery_order_block(
            self.delivery_code,
            reissue_order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        self.expect_inventory[ware_sku]['location_total']['block'] += reissue_order_info[0][1]
        self.expect_inventory['spot_goods_remain'] -= 1

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单分配库位库存
        res = ims.assign_pj_location_stock(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] += reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        temp_dict = {
            "qty": reissue_order_info[0][1],
            "storageLocationId": sj_kw_ids[0],
            "storageLocationType": 5,
            "wareSkuCode": ware_sku
        }
        ware_sku_list.append(temp_dict)

        # 释放库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku].update(
            {
                -self.warehouse_id: {'block': 0, 'stock': reissue_order_info[0][1]}
            }
        )

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 执行发货
        res = ims.pj_delivery_out(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1

        # 释放仓库商品总库存
        self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['warehouse_total']['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['block'] -= reissue_order_info[0][1]

        # 扣掉dock库存
        self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_reissue_order_delivery_not_in_suite_part(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单，只出多余出来不成套的部分
        """
        origin_inventory_info = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        reissue_order_info = [('BP63203684930A01', 1)]
        ware_sku = '63203684930A01'
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory_info), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory_info,
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
            reissue_order_info,
            self.warehouse_id,
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 补发单生成只预占仓库商品总库存，更新remain
        self.expect_inventory[ware_sku]["warehouse_total"]['block'] += reissue_order_info[0][1]
        # self.expect_inventory['central_remain'] -= self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        res = ims.delivery_order_block(
            self.delivery_code,
            reissue_order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        self.expect_inventory[ware_sku]['location_total']['block'] += reissue_order_info[0][1]
        # self.expect_inventory['spot_goods_remain'] -= self.sale_sku_count

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单分配库位库存
        res = ims.assign_pj_location_stock(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] += reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        temp_dict = {
            "qty": reissue_order_info[0][1],
            "storageLocationId": sj_kw_ids[0],
            "storageLocationType": 5,
            "wareSkuCode": ware_sku
        }
        ware_sku_list.append(temp_dict)

        # 释放库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku].update(
            {
                -self.warehouse_id: {'block': 0, 'stock': reissue_order_info[0][1]}
            }
        )

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 执行发货
        res = ims.pj_delivery_out(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 释放销售商品总库存
        # self.expect_inventory["central_stock"] -= self.sale_sku_count
        # 释放销售商品现货库存
        # self.expect_inventory["spot_goods_stock"] -= self.sale_sku_count

        # 释放仓库商品总库存
        self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['warehouse_total']['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['block'] -= reissue_order_info[0][1]

        # 扣掉dock库存
        self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    def test_reissue_order_delivery_not_in_suite_part_and_break_up_suite(self):
        """
        测试场景：一套库存放在多个不同库位，出库补发单，同时出不成套部分且把成套的拆不成套
        """
        origin_inventory_info = [('63203684930A01', 2), ('63203684930A02', 2), ('63203684930A02', 3)]
        reissue_order_info = [('BP63203684930A01', 2)]
        ware_sku = '63203684930A01'
        sj_kw_ids = wms.db_get_kw(1, 5, len(origin_inventory_info), self.warehouse_id, self.to_warehouse_id)

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成销售sku现货库存
        ims.qualified_goods_other_in(
            origin_inventory_info,
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
            reissue_order_info,
            self.warehouse_id,
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 补发单生成只预占仓库商品总库存，更新remain
        self.expect_inventory[ware_sku]["warehouse_total"]['block'] += reissue_order_info[0][1]
        self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单的销售出库单生成，预占现货和库位现货
        res = ims.delivery_order_block(
            self.delivery_code,
            reissue_order_info,
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 库位总库存预占增加，现货remain减少
        self.expect_inventory[ware_sku]['location_total']['block'] += reissue_order_info[0][1]
        self.expect_inventory['spot_goods_remain'] -= 1

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 补发单分配库位库存
        res = ims.assign_pj_location_stock(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 预占库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] += reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

        ware_sku_list = list()
        # 构造拣货sku明细数据，此处为完整拣货，非短拣
        temp_dict = {
            "qty": reissue_order_info[0][1],
            "storageLocationId": sj_kw_ids[0],
            "storageLocationType": 5,
            "wareSkuCode": ware_sku
        }
        ware_sku_list.append(temp_dict)

        # 释放库位库存
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku][sj_kw_ids[0]]['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku].update(
            {
                -self.warehouse_id: {'block': 0, 'stock': reissue_order_info[0][1]}
            }
        )

        confirm_pick_res = ims.confirm_pick(
            self.delivery_code,
            ware_sku_list,
            self.warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )
        assert confirm_pick_res['code'] == 200
        assert current_inventory == self.expect_inventory

        # 执行发货
        res = ims.pj_delivery_out(
            self.delivery_code,
            ware_sku,
            reissue_order_info[0][1],
            self.warehouse_id,
            self.to_warehouse_id
        )
        # 获取库存数据
        current_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id
        )

        # 释放销售商品总库存
        self.expect_inventory["central_stock"] -= 1
        # 释放销售商品现货库存
        self.expect_inventory["spot_goods_stock"] -= 1

        # 释放仓库商品总库存
        self.expect_inventory[ware_sku]['warehouse_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['warehouse_total']['block'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['stock'] -= reissue_order_info[0][1]
        self.expect_inventory[ware_sku]['location_total']['block'] -= reissue_order_info[0][1]

        # 扣掉dock库存
        self.expect_inventory[ware_sku][-self.warehouse_id]['stock'] -= reissue_order_info[0][1]

        assert res['code'] == 200
        assert current_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
