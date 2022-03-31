import time
import pytest

from testcase import *


class TestOMSOrderBlock(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id

    # @pytest.mark.skip(reason='test')
    def test_1_oms_block_sale_sku_without_inventory(self):
        """测试没有库存的情况下，oms下销售sku订单"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('63203684930', 1)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 销售订单预占，更新central表的block
        self.expect_inventory['central_block'] += 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_oms_block_component_sku_without_inventory(self):
        """测试没有库存的情况下，oms下部件sku订单"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('BP63203684930A01', 1)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 部件预占仓库商品总库存，销售商品总库存remain要对应更新
        for sku, qty in delivery_order_goods_list:
            self.expect_inventory.update({
                sku.replace('BP', ''): {
                    "warehouse_total": {'block': qty, 'stock': 0}
                }
            })
        self.expect_inventory['central_remain'] -= 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

    def test_3_oms_block_component_sku_and_sale_sku_without_inventory(self):
        """测试没有库存的情况下，oms下包含销售sku和部件sku的订单，部件sku不成套"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('BP63203684930A01', 1), ('63203684930', 1)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 销售订单预占，更新central表的block
        # 部件预占仓库商品总库存，销售商品总库存remain要对应更新
        for sku, qty in delivery_order_goods_list:
            if sku.startswith('BP'):
                self.expect_inventory.update({
                    sku.replace('BP', ''): {
                        "warehouse_total": {'block': qty, 'stock': 0}
                    }
                })
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] += 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

    def test_4_oms_block_one_suite_component_sku_and_sale_sku_without_inventory(self):
        """测试没有库存的情况下，oms下包含销售sku和部件sku的订单，部件sku成1套"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('BP63203684930A01', 1), ('63203684930', 1), ('BP63203684930A02', 5)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 销售订单预占，更新central表的block
        # 部件预占仓库商品总库存，销售商品总库存remain要对应更新
        for sku, qty in delivery_order_goods_list:
            if sku.startswith('BP'):
                self.expect_inventory.update({
                    sku.replace('BP', ''): {
                        "warehouse_total": {'block': qty, 'stock': 0}
                    }
                })
        self.expect_inventory['central_remain'] -= 1
        self.expect_inventory['central_block'] += 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

    def test_5_oms_block_less_than_two_suite_component_sku_and_sale_sku_without_inventory(self):
        """测试没有库存的情况下，oms下包含销售sku和部件sku的订单，部件sku组合起来超过1套，不满2套"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('BP63203684930A01', 2), ('63203684930', 1), ('BP63203684930A02', 5)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 销售订单预占，更新central表的block
        # 部件预占仓库商品总库存，销售商品总库存remain要对应更新
        for sku, qty in delivery_order_goods_list:
            if sku.startswith('BP'):
                self.expect_inventory.update({
                    sku.replace('BP', ''): {
                        "warehouse_total": {'block': qty, 'stock': 0}
                    }
                })
        self.expect_inventory['central_remain'] -= 2
        self.expect_inventory['central_block'] += 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory

    def test_6_oms_block_two_suite_component_sku_and_sale_sku_without_inventory(self):
        """测试没有库存的情况下，oms下包含销售sku和部件sku的订单，部件sku组合起来超过1套，不满2套"""
        sale_sku = '63203684930'
        delivery_order_goods_list = [('BP63203684930A01', 2), ('63203684930', 1), ('BP63203684930A02', 10)]

        # 干掉该销售sku的库存数据；
        ims.delete_qualified_inventory([sale_sku])
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.to_warehouse_id)

        # oms销售订单预占
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
        # 销售订单预占，更新central表的block
        # 部件预占仓库商品总库存，销售商品总库存remain要对应更新
        for sku, qty in delivery_order_goods_list:
            if sku.startswith('BP'):
                self.expect_inventory.update({
                    sku.replace('BP', ''): {
                        "warehouse_total": {'block': qty, 'stock': 0}
                    }
                })
        self.expect_inventory['central_remain'] -= 2
        self.expect_inventory['central_block'] += 1

        assert res['code'] == 200
        assert self.expect_inventory == after_oms_block_inventory


if __name__ == '__main__':
    pytest.main()
