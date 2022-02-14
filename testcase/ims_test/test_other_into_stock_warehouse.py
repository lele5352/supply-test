import pytest

from testcase import *


class TestOtherIntoStockWarehouse(object):
    def setup_class(self):
        self.warehouse_id = stock_warehouse_id
        self.target_warehouse_id = ''
        self.sj_kw_ids = bsj_kw_ids

    def setup(self):
        ims.delete_qualified_inventory(sale_sku)
        self.expect_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_other_into_warehouse_less_than_one_set(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：一套缺一件
        """
        ware_sku_list = list()
        # 构造入库仓库sku明细数据,刚好成1套的
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1]
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
        for i in range(len(ware_sku_list)):
            if ware_sku_list[i]['qty'] == 1:
                ware_sku_list.pop(i)
                break
            elif ware_sku_list[i]['qty'] > 1:
                ware_sku_list[i]['qty'] -= 1
                break
            else:
                continue
        res = ims.other_into_warehouse(ware_sku_list, self.warehouse_id, self.target_warehouse_id)
        self.expect_inventory.update(
            {
                # 插入中央库存、销售商品总库存数据，stock、block都为0
                "central_inventory_stock": 0,
                "central_inventory_block": 0,
                "central_warehouse_stock": 0,
                "central_warehouse_block": 0,

                # 插入销售商品现货库存，stock、block都为0
                'purchase_on_way_block': 0,
                'purchase_on_way_stock': 0,
                'transfer_on_way_block': 0,
                'transfer_on_way_stock': 0,
                "spot_goods_stock": 0,
                "spot_goods_block": 0
            }
        )
        for ware_sku in ware_sku_list:
            self.expect_inventory.update(
                {
                    ware_sku['wareSkuCode']: {
                        ware_sku['storageLocationId']: {'stock': ware_sku['qty'], 'block': 0},
                        'total': {'stock': ware_sku['qty'], 'block': 0}
                    }
                }
            )
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)
        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_2_other_into_warehouse_one_set(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：刚好一套
        """
        ware_sku_list = list()
        # 构造入库仓库sku明细数据,刚好成1套的
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1]
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
        res = ims.other_into_warehouse(ware_sku_list, self.warehouse_id, self.target_warehouse_id)
        self.expect_inventory.update(
            {
                # 插入中央库存、销售商品总库存数据，stock、block都为0
                "central_inventory_stock": 1,
                "central_inventory_block": 0,
                "central_warehouse_stock": 1,
                "central_warehouse_block": 0,

                # 插入销售商品现货库存，stock、block都为0
                'purchase_on_way_block': 0,
                'purchase_on_way_stock': 0,
                'transfer_on_way_block': 0,
                'transfer_on_way_stock': 0,
                "spot_goods_stock": 1,
                "spot_goods_block": 0
            }
        )
        for ware_sku in ware_sku_list:
            self.expect_inventory.update(
                {
                    ware_sku['wareSkuCode']: {
                        ware_sku['storageLocationId']: {'stock': ware_sku['qty'], 'block': 0},
                        'total': {'stock': ware_sku['qty'], 'block': 0}
                    }
                }
            )
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)
        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_3_other_into_warehouse_more_than_one_set(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：超过1套，不满2套
        """
        set_num = 2
        ware_sku_list = list()
        # 构造入库仓库sku明细数据,刚好成1套的
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1] * set_num
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
        for i in range(len(ware_sku_list)):
            if ware_sku_list[i]['qty'] == 1:
                ware_sku_list.pop(i)
                break
            elif ware_sku_list[i]['qty'] > 1:
                ware_sku_list[i]['qty'] -= 1
                break
            else:
                continue
        res = ims.other_into_warehouse(ware_sku_list, self.warehouse_id, self.target_warehouse_id)
        self.expect_inventory.update(
            {
                # 插入中央库存、销售商品总库存数据，stock、block都为0
                "central_inventory_stock": set_num - 1,
                "central_inventory_block": 0,
                "central_warehouse_stock": set_num - 1,
                "central_warehouse_block": 0,

                # 插入销售商品现货库存，stock、block都为0
                'purchase_on_way_block': 0,
                'purchase_on_way_stock': 0,
                'transfer_on_way_block': 0,
                'transfer_on_way_stock': 0,
                "spot_goods_stock": set_num - 1,
                "spot_goods_block": 0
            }
        )
        for ware_sku in ware_sku_list:
            self.expect_inventory.update(
                {
                    ware_sku['wareSkuCode']: {
                        ware_sku['storageLocationId']: {'stock': ware_sku['qty'], 'block': 0},
                        'total': {'stock': ware_sku['qty'], 'block': 0}
                    }
                }
            )
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)
        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_4_other_into_warehouse_two_set(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：超过1套，不满2套
        """
        set_num = 2
        ware_sku_list = list()
        # 构造入库仓库sku明细数据,刚好成1套的
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1] * set_num
            temp_dict = {
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }
            ware_sku_list.append(temp_dict)
        res = ims.other_into_warehouse(ware_sku_list, self.warehouse_id, self.target_warehouse_id)
        self.expect_inventory.update(
            {
                # 插入中央库存、销售商品总库存数据，stock、block都为0
                "central_inventory_stock": set_num,
                "central_inventory_block": 0,
                "central_warehouse_stock": set_num,
                "central_warehouse_block": 0,

                # 插入销售商品现货库存，stock、block都为0
                'purchase_on_way_block': 0,
                'purchase_on_way_stock': 0,
                'transfer_on_way_block': 0,
                'transfer_on_way_stock': 0,
                "spot_goods_stock": set_num,
                "spot_goods_block": 0
            }
        )
        for ware_sku in ware_sku_list:
            self.expect_inventory.update(
                {
                    ware_sku['wareSkuCode']: {
                        ware_sku['storageLocationId']: {'stock': ware_sku['qty'], 'block': 0},
                        'total': {'stock': ware_sku['qty'], 'block': 0}
                    }
                }
            )
        current_inventory = ims.get_inventory(
            sale_sku,
            bom,
            self.warehouse_id,
            self.target_warehouse_id)
        assert res['code'] == 200
        assert current_inventory == self.expect_inventory

    # @pytest.mark.skip(reason='test')
    def test_5_other_into_warehouse_one_set_complete_by_two_times(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：分多次凑成一套
        """
        self.expect_inventory.update({
            "central_inventory_stock": 0,
            "central_inventory_block": 0,
            "central_warehouse_stock": 0,
            "central_warehouse_block": 0,
            'purchase_on_way_block': 0,
            'purchase_on_way_stock': 0,
            'transfer_on_way_block': 0,
            'transfer_on_way_stock': 0,
            "spot_goods_stock": 0,
            "spot_goods_block": 0
        })
        # 构造入库仓库sku明细数据,刚好成1套的
        iter_time = 0
        for sj_location_id, detail in zip(self.sj_kw_ids, bom_detail.items()):
            pick_qty = detail[1]
            ware_sku_list = [{
                "qty": pick_qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": detail[0]
            }]

            res = ims.other_into_warehouse(ware_sku_list, self.warehouse_id, self.target_warehouse_id)
            self.expect_inventory.update(
                {
                    detail[0]: {
                        sj_location_id: {'stock': detail[1], 'block': 0},
                        'total': {'stock': detail[1], 'block': 0}
                    }
                }
            )
            current_inventory = ims.get_inventory(
                sale_sku,
                bom,
                self.warehouse_id,
                self.target_warehouse_id)
            if iter_time >= len(bom_detail) - 1:
                self.expect_inventory.update(
                    {
                        "central_inventory_stock": 1,
                        "central_warehouse_stock": 1,
                        "spot_goods_stock": 1,
                    }
                )
            iter_time += 1
            assert res['code'] == 200
            assert current_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
