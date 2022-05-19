import pytest

from testcase import *


class TestBHCOtherIntoLP(object):
    def setup_class(self):
        self.ck_id = stock_warehouse_id
        self.to_ck_id = ''
        wms_request.switch_default_warehouse(self.ck_id)

    def test_1_up_shelf_one_single_goods_to_one_location(self):
        """
        测试场景：1种单品，数量1个，上架到1个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        ware_sku_qty_list = [('16338527895A01', 1)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_2_up_shelf_many_single_goods_to_one_location(self):
        """
        测试场景：1种单品，数量多个，上架到1个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_3_up_shelf_many_single_goods_to_several_locations(self):
        """
        测试场景：1种单品，数量多个，上架到多个上架库位
        销售sku：16338527895
        bom:A
        仓库sku：16338527895A01
        """
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = wms_logics.get_kw(1, 5, len(ware_sku_qty_list), self.ck_id, self.to_ck_id)

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_4_up_shelf_one_multiple_goods_to_one_location(self):
        """
        测试场景：多品中的1个仓库sku，数量1个，上架到1个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        ware_sku_qty_list = [('63203684930A01', 1)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_5_up_shelf_many_multiple_goods_to_one_location(self):
        """
        测试场景：多品中的1个仓库sku，数量多个，上架到1个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A01', 3)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_6_up_shelf_many_multiple_goods_to_several_locations(self):
        """
        测试场景：多品中的1个仓库sku，数量多个，上架到多个上架库位
        销售sku：63203684930
        bom:A
        仓库sku：63203684930A01
        """
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A01', 3)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = wms_logics.get_kw(1, 5, len(ware_sku_qty_list), self.ck_id, self.to_ck_id)

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_7_up_shelf_different_single_goods_to_one_location(self):
        """
        测试场景：多个不同单品，数量多个，上架到1个上架库位
        销售sku：16338527895，20537964151
        bom:A
        仓库sku：16338527895A01，20537964151A01
        """
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3), ('20537964151A01', 1), ('20537964151A01', 2)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_8_up_shelf_different_single_goods_to_several_locations(self):
        """
        测试场景：多个不同单品，数量多个，上架到多个上架库位
        销售sku：16338527895，20537964151
        bom:A
        仓库sku：16338527895A01，20537964151A01
        """
        ware_sku_qty_list = [('16338527895A01', 2), ('16338527895A01', 3), ('20537964151A01', 1), ('20537964151A01', 2)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = wms_logics.get_kw(1, 5, len(ware_sku_qty_list), self.ck_id, self.to_ck_id)

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_9_up_shelf_multiple_goods_less_than_one_set_to_one_location(self):
        """
        测试场景：多品不够一套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_10_up_shelf_multiple_goods_one_set_to_one_location(self):
        """
        测试场景：多品刚好够一套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_11_up_shelf_multiple_goods_less_than_two_set_to_one_location(self):
        """
        测试场景：多品够一套，不到2套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A02', 9)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_12_up_shelf_multiple_goods_two_set_to_one_location(self):
        """
        测试场景：多品够一套，不到2套，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        仓库sku：63203684930A01, 63203684930A02
        """
        ware_sku_qty_list = [('63203684930A01', 2), ('63203684930A02', 10)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_13_up_shelf_different_bom_multiple_goods_two_set_to_one_location(self):
        """
        测试场景：多品够2套，2个bom，上架到1个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        bom:B 63203684930B01:63203684930B02 => 1:5

        仓库sku：63203684930A01, 63203684930A02;63203684930B01,63203684930B02
        """
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5), ('63203684930B01', 1), ('63203684930B02', 5)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = [fsj_kw_ids[0] for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_14_up_shelf_different_bom_multiple_goods_two_set_to_several_locations(self):
        """
        测试场景：多品够2套，2个bom，上架到多个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        bom:B 63203684930B01:63203684930B02 => 1:5
        """
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5), ('63203684930B01', 1), ('63203684930B02', 5)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = wms_logics.get_kw(1, 5, len(ware_sku_qty_list), self.ck_id, self.to_ck_id)

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)

        res = ims_request.lp_other_in(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}

    def test_15_up_shelf_multiple_goods_one_set_to_several_locations_by_times(self):
        """
        测试场景：多品够1套，分多次上架到多个上架库位
        销售sku：63203684930
        bom:A 63203684930A01:63203684930A02 => 1:5
        """
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4), ('63203684930A02', 1)]
        sale_skus = ims_logics.get_sale_skus(ware_sku_qty_list)
        sj_kw_ids = wms_logics.get_kw(1, 5, len(ware_sku_qty_list), self.ck_id, self.to_ck_id)

        IMSDBOperator.delete_unqualified_inventory(sale_skus)
        expect = ims_logics.get_expect_inventory_with_kws(ware_sku_qty_list, sj_kw_ids, self.ck_id, self.to_ck_id)
        # 构造入库仓库sku明细数据
        for (ware_sku, qty), sj_location_id in zip(ware_sku_qty_list, sj_kw_ids):
            temp_ware_sku_qty_list = [(ware_sku, qty)]
            tem_sj_location_id_list = [sj_location_id]
            res = ims_request.lp_other_in(temp_ware_sku_qty_list, tem_sj_location_id_list, self.ck_id, self.to_ck_id)
            assert res['code'] == 200

        actual = ims_logics.query_lp_inventories(sale_skus, self.ck_id, self.to_ck_id)
        assert expect == actual
        unqualified_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.ck_id, self.to_ck_id)
        assert unqualified_inventory == {}


if __name__ == '__main__':
    pytest.main()
