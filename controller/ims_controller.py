import time

from utils.request_handler import RequestHandler
from utils.mysql_handler import MysqlHandler

from config.api_config.ims_api_config import ims_api_config
from config.sys_config import env_config


class ImsController(RequestHandler):
    def __init__(self):
        self.prefix = env_config.get('ims_service_prefix')
        self.service_headers = {"serviceName": "ec-warehouse-delivery-service"}
        super().__init__(self.prefix, self.service_headers)
        self.db = MysqlHandler(**env_config.get('mysql_info_ims'))

    def delete_qualified_inventory(self, sale_sku_code):
        """
        删除销售sku对应的全部库存数据，包括中央库存、销售商品总库存、现货库存、仓库商品总库存、库位库存

        :param sale_sku_code: 销售sku编码
        """
        del_central_inventory_sql = "delete from central_inventory where goods_sku_code='%s';"
        del_goods_inventory_sql = "delete from goods_inventory where goods_sku_code='%s';"
        del_wares_inventory_sql = "delete from wares_inventory where goods_sku_code='%s';"
        sql_list = [del_wares_inventory_sql, del_goods_inventory_sql, del_central_inventory_sql]
        for sql in sql_list:
            self.db.execute(sql % sale_sku_code)

    def delete_unqualified_inventory(self, sale_sku_code, bom_version, warehouse_id):
        """
        删除销售sku对应的全部次品库存数据

        :param sale_sku_code: 销售sku编码
        :param bom_version: bom版本
        :param warehouse_id: 仓库id
        """
        for ware_sku_code in self.db_get_bom_detail(sale_sku_code, bom_version).keys():
            del_sql = "delete from nogood_wares_inventory where ware_sku_code='%s' and warehouse_id = %s;" % (
                ware_sku_code, warehouse_id)
            self.db.execute(del_sql)

    # 获取销售商品bom比例
    def db_get_bom_detail(self, sale_sku_code, bom_version):
        """
        返回销售sku的bom版本明细，格式如： {"ware_sku_code1":x,"ware_sku_code2":y,...}

        :param sale_sku_code: 销售sku
        :param bom_version: bom版本
        """
        # 最终要返回的数据
        sale_sku_bom_detail = dict()

        # 获取bom明细数据，组装成{"仓库sku1":数量1,"仓库sku2":数量2}格式
        get_bom_detail_sql = """
                   SELECT
                       ware_sku_code,bom_qty 
                   FROM
                       bom_detail 
                   WHERE
                       goods_sku_code = '%s' 
                       and bom_version = '%s';
                   """ % (sale_sku_code, bom_version)
        bom_detail_data = self.db.get_all(get_bom_detail_sql)

        for ware_sku_detail in bom_detail_data:
            sale_sku_bom_detail.update(
                {
                    ware_sku_detail['ware_sku_code']: ware_sku_detail['bom_qty']
                })
        return sale_sku_bom_detail

    # 销售商品中央总库存获取
    def get_central_inventory(self, sale_sku_code):
        """
        :param sale_sku_code: 销售sku编码

        return dict：{'central_inventory_stock':x,'central_inventory_block':y}
        """
        sql = "select stock,block from central_inventory where goods_sku_code ='%s' and warehouse_id is NULL;" % sale_sku_code
        central_inventory_data = self.db.get_one(sql)
        if not central_inventory_data:
            return {
                "central_inventory_stock": 0,
                "central_inventory_block": 0
            }
        return {
            "central_inventory_stock": central_inventory_data['stock'],
            "central_inventory_block": central_inventory_data['block']
        }

    # 销售商品仓库总库存获取
    def get_warehouse_central_inventory(self, sale_sku_code, warehouse_id, target_warehouse_id) -> dict or None:
        """
        获取销售商品总库存

        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int target_warehouse_id: 目的仓库id

        if query stock data fail return None;
        else return dict like {'central_inventory_sale_stock':x,'central_inventory_sale_block':y}
        """
        temp_sql = 'warehouse_id=%s' % target_warehouse_id if target_warehouse_id else 'warehouse_id=%s' % warehouse_id
        sql = "select stock,block from central_inventory where goods_sku_code ='%s' and %s" % (
            sale_sku_code, temp_sql)
        sale_sku_warehouse_central_inventory = self.db.get_one(sql)
        if not sale_sku_warehouse_central_inventory:
            return {
                "central_inventory_sale_stock": 0,
                "central_inventory_sale_block": 0
            }
        return {
            "central_inventory_sale_stock": sale_sku_warehouse_central_inventory['stock'],
            "central_inventory_sale_block": sale_sku_warehouse_central_inventory['block']
        }

    # 销售商品分类库存获取
    def get_goods_inventory(self, sale_sku_code, warehouse_id, target_warehouse_id):
        temp_sql = " = %s" % target_warehouse_id if target_warehouse_id else "is NULL"
        sql = """
                SELECT 
                    type,stock,block 
                FROM
                    goods_inventory 
                WHERE
                    goods_sku_code = '%s' 
                    AND current_warehouse_id = %s 
                    AND target_warehouse_id %s
                """ % (sale_sku_code, warehouse_id, temp_sql)
        goods_inventory_data = self.db.get_all(sql)
        goods_inventory_dict = {
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': 0,
            'goods_inventory_spot_goods_block': 0
        }
        if not goods_inventory_data:
            return goods_inventory_dict

        for inventory_data in goods_inventory_data:
            # 销售商品采购在途库存
            if inventory_data['type'] == 1:
                goods_inventory_dict.update({
                    'goods_inventory_purchase_on_way_stock': inventory_data['stock'],
                    'goods_inventory_purchase_on_way_block': inventory_data['block']
                })
            elif inventory_data['type'] == 2:
                goods_inventory_dict.update({
                    'goods_inventory_transfer_on_way_stock': inventory_data['stock'],
                    'goods_inventory_transfer_on_way_block': inventory_data['block']
                })
            elif inventory_data['type'] == 3:
                goods_inventory_dict.update({
                    'goods_inventory_spot_goods_stock': inventory_data['stock'],
                    'goods_inventory_spot_goods_block': inventory_data['block']
                })
        return goods_inventory_dict

    # 获取仓库商品总库存
    def get_wares_inventory(self, sale_sku_code, bom_version, warehouse_id, target_warehouse_id):
        ware_sku_code_list = self.db_get_bom_detail(sale_sku_code, bom_version).keys()
        if not ware_sku_code_list:
            return
        all_ware_sku_inventory = dict()

        for ware_sku_code in ware_sku_code_list:
            temp_sql = " = %s" % target_warehouse_id if target_warehouse_id else "is NULL"
            sql = """
                   SELECT
                       storage_location_id,stock,block 
                   FROM
                       wares_inventory 
                   WHERE
                       goods_sku_code = '%s' 
                       AND warehouse_id = %s
                       AND target_warehouse_id %s
                       AND ware_sku_code = '%s'
                   ORDER BY
                       ware_sku_code;
                   """ % (sale_sku_code, warehouse_id, temp_sql, ware_sku_code)

            ware_sku_inventory_data = self.db.get_all(sql)
            if not ware_sku_inventory_data:
                continue
            temp_ware_sku_inventory = dict()
            for data in ware_sku_inventory_data:
                if data['storage_location_id'] is None:
                    temp_ware_sku_inventory.update(
                        {
                            "total": {'stock': data['stock'], 'block': data['block']}
                        }
                    )
                else:
                    temp_ware_sku_inventory.update(
                        {data['storage_location_id']: {'stock': data['stock'], 'block': data['block']}}
                    )
            all_ware_sku_inventory.update({
                ware_sku_code: temp_ware_sku_inventory
            })
        return all_ware_sku_inventory

    # 获取良品库存
    def get_inventory(self, sale_sku_code, bom_version, warehouse_id, target_warehouse_id):
        current_inventory = dict()
        central_inventor = self.get_central_inventory(sale_sku_code)
        central_warehouse_inventory = self.get_warehouse_central_inventory(sale_sku_code, warehouse_id,
                                                                           target_warehouse_id)
        goods_inventory = self.get_goods_inventory(sale_sku_code, warehouse_id, target_warehouse_id)
        wares_inventory = self.get_wares_inventory(sale_sku_code, bom_version, warehouse_id, target_warehouse_id)

        # 库存字典数据合并
        if central_inventor:
            current_inventory.update(central_inventor)
        if central_warehouse_inventory:
            current_inventory.update(central_warehouse_inventory)
        if goods_inventory:
            current_inventory.update(goods_inventory)
        if wares_inventory:
            current_inventory.update(wares_inventory)
        return current_inventory

    # 获取仓库商品总库存
    def get_unqualified_inventory(self, sale_sku_code, bom_version, warehouse_id):
        unqualified_goods_inventory = dict()
        for ware_sku_code in self.db_get_bom_detail(sale_sku_code, bom_version).keys():
            sql = """
                    SELECT
                        storage_location_id,stock,block 
                    FROM
                        nogood_wares_inventory 
                    WHERE
                        warehouse_id = %s
                        AND ware_sku_code = '%s';
                    """ % (warehouse_id, ware_sku_code)
            ware_sku_inventory_data = self.db.get_all(sql)
            if not ware_sku_inventory_data:
                continue
            temp_ware_sku_inventory = dict()
            for data in ware_sku_inventory_data:
                if data['storage_location_id'] is None:
                    temp_ware_sku_inventory.update(
                        {"total": {'stock': data['stock'], 'block': data['block']}}
                    )
                elif data['storage_location_id'] > 0:
                    temp_ware_sku_inventory.update(
                        {data['storage_location_id']: {'stock': data['stock'], 'block': data['block']}}
                    )
            unqualified_goods_inventory.update({ware_sku_code: temp_ware_sku_inventory})
        return unqualified_goods_inventory

    # OMS下单预占中央库存、销售商品总库存
    def oms_order_block(self, sale_sku_code, count, warehouse_id):
        ims_api_config['oms_order_block']['data'].update({
            "goodsSkuList": [
                {
                    "goodsSkuCode": sale_sku_code,
                    "qty": count
                }],
            "sourceNo": "OMS" + str(int(time.time())),
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['oms_order_block'])
        return res

    # 采购下单
    def purchase_create_order(self, sale_sku_code, count, warehouse_id, target_warehouse_id):
        temp_data = {
            "goodsSkuList": [{
                "goodsSkuCode": sale_sku_code,
                "qty": count,
                "targetWarehouseId": target_warehouse_id
            }],
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "warehouseId": warehouse_id
        }

        ims_api_config['purchase_create_order']['data'][0].update(temp_data)
        res = self.send_request(**ims_api_config['purchase_create_order'])
        return res

    # 采购入库上架
    def purchase_into_warehouse(self, sale_sku_code, bom_version, sale_sku_count, sj_location_ids, warehouse_id,
                                target_warehouse_id):
        # 构建上架明细数据
        ware_sku_list = list()
        up_shelves_list = list()
        bom_detail = self.db_get_bom_detail(sale_sku_code, bom_version)
        for detail, location_id in zip(bom_detail.items(), sj_location_ids):
            ware_sku_list.append(
                {
                    "bomQty": detail[1],
                    "qty": sale_sku_count * detail[1],
                    "storageLocationId": location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": detail[0]
                }
            )
        up_shelves_list.append({
            "bomVersion": bom_version,
            "goodsSkuCode": sale_sku_code,
            "wareSkuList": ware_sku_list
        })
        temp_data = {
            "goodsSkuList": up_shelves_list,
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "targetWarehouseId": target_warehouse_id,
            "warehouseId": warehouse_id
        }
        ims_api_config['purchase_into_warehouse']['data'].update(temp_data)
        res = self.send_request(**ims_api_config['purchase_into_warehouse'])
        return res

    # 其他入库
    def other_into_warehouse(self, ware_sku_list, warehouse_id, target_warehouse_id):
        ims_api_config['other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "RK" + str(int(time.time() * 1000)),
                "targetWarehouseId": target_warehouse_id,
                "warehouseId": warehouse_id,
                "wareSkuList": ware_sku_list
            })
        res = self.send_request(**ims_api_config['other_into_warehouse'])
        return res

    # 销售出库单生成时预占
    def delivery_order_block(self, delivery_order_no, sale_sku_code, count, warehouse_id, target_warehouse_id):
        ims_api_config['delivery_order_block']['data'].update({
            "goodsSkuList": [
                {
                    "goodsSkuCode": sale_sku_code,
                    "qty": count
                }],
            "sourceNo": delivery_order_no,
            "targetWarehouseId": target_warehouse_id,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['delivery_order_block'])
        return res

    # 分配库位库存
    def assign_location_stock(self, delivery_order_no, sale_sku_code, bom_version, count, warehouse_id):
        bom_detail = self.db_get_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for ware_sku, qty in bom_detail.items():
            temp_ware_sku_dict = {
                "qty": qty * count,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['assign_location_stock']['data'][0].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['assign_location_stock'])
        return res

    # 确认拣货
    def confirm_pick(self, delivery_order_no, ware_sku_list, warehouse_id):
        ims_api_config['confirm_pick']['data'].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['confirm_pick'])
        return res

    # 发货
    def delivery_out(self, delivery_order_no, sale_sku_code, bom_version, count, warehouse_id, target_warehouse_id):
        bom_detail = self.db_get_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for ware_sku, qty in bom_detail.items():
            temp_ware_sku_dict = {
                "qty": qty * count,
                "wareSkuCode": ware_sku,
                "storageLocationId": -warehouse_id
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['delivery_out']['data'][0].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id,
            "targetWarehouseId": target_warehouse_id
        })
        res = self.send_request(**ims_api_config['delivery_out'])
        return res

    def cancel_oms_order_block(self, ims_block_book_id, oms_order_code):
        ims_api_config['cancel_oms_order_block']['data'].update({
            "blockBookId": ims_block_book_id,
            "sourceNo": oms_order_code
        })
        res = self.send_request(**ims_api_config['cancel_oms_order_block'])
        return res

    def cancel_block_before_pick(self, delivery_order_no):
        ims_api_config['cancel_block_before_pick']['data'].update({"sourceNo": delivery_order_no})
        res = self.send_request(**ims_api_config['cancel_block_before_pick'])
        return res

    def cancel_block_after_pick(self, delivery_order_no, sale_sku_code, location_id, count, bom_version,
                                warehouse_id):
        bom_detail = self.db_get_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for detail in bom_detail.items():
            temp_ware_sku_dict = {
                "fromStorageLocationId": -warehouse_id,
                "qty": detail[1] * count,
                "toStorageLocationId": location_id,
                "toStorageLocationType": "4",
                "toTargetWarehouseId": warehouse_id,
                "wareSkuCode": detail[0],
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['cancel_block_after_pick']['data'].update(
            {
                "wareSkuList": ware_sku_list,
                "sourceNo": delivery_order_no
            })
        res = self.send_request(**ims_api_config['cancel_block_after_pick'])
        return res

    def add_stock_by_purchase_in(self, sale_sku_code, bom_version, sj_location_ids, count, warehouse_id,
                                 target_warehouse_id):
        purchase_create_order_res = self.purchase_create_order(
            sale_sku_code,
            count,
            warehouse_id,
            target_warehouse_id)
        if not purchase_create_order_res or purchase_create_order_res['code'] != 200:
            return
        purchase_into_warehouse_res = self.purchase_into_warehouse(
            sale_sku_code,
            bom_version,
            count,
            sj_location_ids,
            warehouse_id,
            target_warehouse_id)
        return purchase_into_warehouse_res

    def qualified_goods_other_out_block(self, ware_sku_list, warehouse_id, target_warehouse_id):
        ims_api_config['qualified_goods_other_out_block']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "targetWarehouseId": target_warehouse_id,
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        qualified_goods_other_out_block_res = self.send_request(**ims_api_config['qualified_goods_other_out_block'])
        return qualified_goods_other_out_block_res

    def cancel_qualified_goods_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_qualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_qualified_goods_other_out_block'])
        return cancel_block_res

    def cancel_unqualified_goods_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_unqualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_unqualified_goods_other_out_block'])
        return cancel_block_res

    def unqualified_goods_other_out_block(self, ware_sku_list, warehouse_id):
        ims_api_config['unqualified_goods_other_out_block']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        unqualified_goods_other_out_block_res = self.send_request(**ims_api_config['unqualified_goods_other_out_block'])
        return unqualified_goods_other_out_block_res

    def qualified_goods_other_out_delivered(self, ware_sku_list, warehouse_id, target_warehouse_id):
        ims_api_config['qualified_goods_other_out_delivery_goods']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "targetWarehouseId": target_warehouse_id,
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        qualified_goods_other_out_block_res = self.send_request(
            **ims_api_config['qualified_goods_other_out_delivery_goods'])
        return qualified_goods_other_out_block_res

    def unqualified_goods_other_out_delivered(self, ware_sku_list, warehouse_id):
        ims_api_config['unqualified_goods_other_out_delivery_goods']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        unqualified_goods_other_out_block_res = self.send_request(
            **ims_api_config['unqualified_goods_other_out_delivery_goods'])
        return unqualified_goods_other_out_block_res

    def turn_to_unqualified_goods(self, ware_sku, from_location_id, to_location_id, qty, warehouse_id,
                                  target_warehouse_id):
        ims_api_config['turn_to_unqualified_goods']['data'].update(
            {
                "sourceNo": "LZC" + str(int(time.time() * 1000)),
                "qty": qty,
                "fromStorageLocationId": from_location_id,
                "toStorageLocationId": to_location_id,
                "warehouseId": warehouse_id,
                "targetWarehouseId": target_warehouse_id,
                "wareSkuCode": ware_sku
            }
        )
        turn_to_unqualified_goods = self.send_request(**ims_api_config['turn_to_unqualified_goods'])
        return turn_to_unqualified_goods

    def add_unqualified_stock_by_other_in(self, ware_sku, from_location_id, to_location_id, qty, warehouse_id,
                                          target_warehouse_id):
        ware_sku_list = [{
            "qty": qty,
            "storageLocationId": from_location_id,
            "storageLocationType": 5,
            "wareSkuCode": ware_sku
        }]
        ims_api_config['other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "RK" + str(int(time.time() * 1000)),
                "targetWarehouseId": target_warehouse_id,
                "warehouseId": warehouse_id,
                "wareSkuList": ware_sku_list
            })
        other_in_res = self.send_request(**ims_api_config['other_into_warehouse'])
        if not other_in_res or other_in_res['code'] != 200:
            return

        turn_to_unqualified_goods_res = self.turn_to_unqualified_goods(
            ware_sku,
            from_location_id,
            to_location_id,
            qty,
            warehouse_id,
            target_warehouse_id)
        if not turn_to_unqualified_goods_res:
            return
        return True

    def add_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, location_id, warehouse_id,
                              target_warehouse_id):
        detail = self.db_get_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for ware_sku, qty in detail.items():
            ware_sku_list.append(
                {
                    "qty": qty * add_stock_count,
                    "storageLocationId": location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": ware_sku
                }
            )
        res = self.other_into_warehouse(ware_sku_list, warehouse_id, target_warehouse_id)
        return res


if __name__ == '__main__':
    ims = ImsController()
    ims.delete_qualified_inventory('46638670690')
    # ims.delete_ims_data('20607392841')
