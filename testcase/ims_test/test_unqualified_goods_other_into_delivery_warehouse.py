import pytest

from testcase import *


class TestUnqualifiedGoodsOtherIntoDeliveryWarehouse(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id
        wms.switch_default_warehouse(self.warehouse_id)

    def test_1_up_shelf_one_single_goods_to_one_location(self):
        """
        测试场景：1种单品，数量1个，上架到1个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        sale_skus = ['16338527895']
        ware_sku_qty_list = [('16338527895A01', 1)]
        cp_location_ids = [wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)]

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)

            assert qualified_inventory == {}

    def test_2_up_shelf_many_single_goods_to_one_location(self):
        """
        测试场景：1种单品，数量多个，上架到1个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        sale_skus = ['16338527895']
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_3_up_shelf_many_single_goods_to_several_locations(self):
        """
        测试场景：1种单品，数量多个，上架到多个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        sale_skus = ['16338527895']
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_4_up_shelf_one_multiple_goods_to_one_location(self):
        """
        测试场景：多品中的1个仓库sku，数量1个，上架到1个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 1)]
        cp_location_ids = [wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)]

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_5_up_shelf_many_multiple_goods_to_one_location(self):
        """
        测试场景：多品中的1个仓库sku，数量多个，上架到1个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A01', 3)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_6_up_shelf_many_multiple_goods_to_several_locations(self):
        """
        测试场景：多品中的1个仓库sku，数量多个，上架到多个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A01', 3)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_7_up_shelf_different_single_goods_to_one_location(self):
        """
        测试场景：多个不同单品，数量多个，上架到1个上架库位
        销售sku：16338527895，20537964151
        bom:A
        仓库sku：16338527895A01，20537964151A01
        """
        sale_skus = ['16338527895', '20537964151']
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3), ('20537964151A01', 1), ('20537964151A01', 2)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_8_up_shelf_different_single_goods_to_several_locations(self):
        """
        测试场景：多个不同单品，数量多个，上架到多个上架库位
        销售sku：16338527895，20537964151
        bom:A
        仓库sku：16338527895A01，20537964151A01
        """
        sale_skus = ['16338527895', '20537964151']
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3), ('20537964151A01', 1), ('20537964151A01', 2)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_9_up_shelf_multiple_goods_less_than_one_set_to_one_location(self):
        """
        测试场景：多品不够一套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_10_up_shelf_multiple_goods_one_set_to_one_location(self):
        """
        测试场景：多品刚好够一套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_11_up_shelf_multiple_goods_less_than_two_set_to_one_location(self):
        """
        测试场景：多品够一套，不到2套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A02', 9)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_12_up_shelf_multiple_goods_two_set_to_one_location(self):
        """
        测试场景：多品够一套，不到2套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A02', 10)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_13_up_shelf_different_bom_multiple_goods_two_set_to_one_location(self):
        """
        测试场景：多品够2套，2个bom，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        bom:B 63203684930B01:63203684930B02 => 1:5

        仓库sku：63203684930A01, 63203684930A02;63203684930B01,63203684930B02
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5), ('63203684930B01', 1), ('63203684930B02', 5)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(ware_sku_qty_list,
                                                                                               cp_location_ids).get(
                sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}

    def test_14_up_shelf_different_bom_multiple_goods_two_set_to_several_locations(self):
        """
        测试场景：多品够2套，2个bom，上架到多个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        bom:B 63203684930B01:63203684930B02 => 1:5
        """
        sale_skus = ['63203684930']
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5), ('63203684930B01', 1), ('63203684930B02', 5)]
        cp_location_ids = wms.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_qualified_inventory(sale_skus)
        IMSDBOperator.delete_unqualified_inventory(sale_skus)

        res = ims.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, self.warehouse_id,
                                             self.to_warehouse_id)
        assert res['code'] == 200

        for sale_sku in sale_skus:
            unqualified_inventory = IMSDBOperator.query_unqualified_inventory(sale_sku, self.warehouse_id)
            expect_unqualified_inventory = ims.get_unqualified_goods_other_in_expect_inventory(
                ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_unqualified_inventory == unqualified_inventory

            qualified_inventory = IMSDBOperator.query_qualified_inventory(sale_sku, self.warehouse_id, self.to_warehouse_id)
            assert qualified_inventory == {}


if __name__ == '__main__':
    pytest.main()
