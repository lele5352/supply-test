import copy
import time

from utils.request_handler import RequestHandler
from utils.mysql_handler import MysqlHandler
from utils.log_handler import LoggerHandler
from utils.ums_handler import get_ims_headers
from config.ims_api_config import ims_api_config
from data_helper.wms_app_api_helper import WmsAppApiHelper


class ImsDataHelper(RequestHandler):
    def __init__(self):
        self.prefix_key = 'ims_service_26'
        self.service_headers = get_ims_headers()
        self.wms_api = WmsAppApiHelper()
        super().__init__(self.prefix_key, self.service_headers)
        self.db = MysqlHandler('test_72', 'homary_ims')
        self.log_handler = LoggerHandler('ImsServiceHelper')

    def delete_ims_data(self, sale_sku_code, warehouse_id):
        del_central_inventory_sql = "DELETE from central_inventory where goods_sku_code='%s'" % (sale_sku_code)
        del_goods_inventory_sql = "DELETE from goods_inventory where goods_sku_code='%s';" % (
            sale_sku_code)
        del_wares_inventory_sql = "DELETE from wares_inventory where goods_sku_code='%s' or storage_location_id='%s';" % (
            sale_sku_code, -warehouse_id)
        sql_list = [del_wares_inventory_sql, del_goods_inventory_sql, del_central_inventory_sql]
        for sql in sql_list:
            self.db.execute(sql)

    # 获取销售商品bom比例
    def get_sale_sku_bom_detail(self, sale_sku_code, bom_version):
        """
        :param sale_sku_code: 销售sku
        :param bom_version: bom版本
        :return:格式{"仓库sku1":数量1,"仓库sku2":数量2}
        """
        # 最终要返回的数据
        sale_sku_bom_detail = dict()

        # 获取bom明细数据，组装成{"仓库sku1":数量1,"仓库sku2":数量2}格式
        get_bom_detail_sql = """
                   SELECT
                       ware_sku_code,
                       bom_qty 
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

    def get_bom_version_ware_sku(self, sale_sku_code, bom_version):
        """
        :param sale_sku_code: string，销售sku
        :param bom_version: string，bom版本
        :return: list，所传的销售sku、bom版本对应的仓库sku列表（不含比例）
        """
        bom_detail = self.get_sale_sku_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = bom_detail.keys()
        return ware_sku_list

    # 销售商品中央总库存获取
    def get_central_inventory(self, sale_sku_code):
        """
        :return: dict：{'central_inventory_stock':x,'central_inventory_block':y}
        """
        sql = "select stock,block from central_inventory where goods_sku_code ='%s' and warehouse_id is NULL;" % sale_sku_code
        central_inventory_data = self.db.get_one(sql)
        if not central_inventory_data:
            return
        return {
            "central_inventory_stock": central_inventory_data['stock'],
            "central_inventory_block": central_inventory_data['block']
        }

    # 销售商品仓库总库存获取
    def get_warehouse_central_inventory(self, sale_sku_code, warehouse_id):
        """
        :return: dict：{'central_inventory_sale_stock':x,'central_inventory_sale_block':y}
        """
        sql = "select stock,block from central_inventory where goods_sku_code ='%s' and warehouse_id=%s;" % (
            sale_sku_code, warehouse_id)
        sale_sku_warehouse_central_inventory = self.db.get_one(sql)
        if not sale_sku_warehouse_central_inventory:
            return
        return {
            "central_inventory_sale_stock": sale_sku_warehouse_central_inventory['stock'],
            "central_inventory_sale_block": sale_sku_warehouse_central_inventory['block']
        }

    # 销售商品分类库存获取
    def get_goods_inventory(self, sale_sku_code, current_warehouse_id, target_warehouse_id):
        if not target_warehouse_id:
            sql = """
                        SELECT
                            type,
                            stock,
                            block 
                        FROM
                            goods_inventory 
                        WHERE
                            goods_sku_code = '%s' 
                            AND current_warehouse_id = %s 
                            AND target_warehouse_id is NULL;
                        """ % (
                sale_sku_code,
                current_warehouse_id
            )
        else:
            sql = """
                SELECT
                    type,
                    stock,
                    block 
                FROM
                    goods_inventory 
                WHERE
                    goods_sku_code = '%s' 
                    AND current_warehouse_id = %s 
                    AND target_warehouse_id = %s
                """ % (
                sale_sku_code,
                current_warehouse_id,
                target_warehouse_id
            )
        goods_inventory_data = self.db.get_all(sql)
        if not goods_inventory_data:
            return
        goods_inventory_dict = {
            'goods_inventory_purchase_on_way_stock': 0,
            'goods_inventory_purchase_on_way_block': 0,
            'goods_inventory_transfer_on_way_stock': 0,
            'goods_inventory_transfer_on_way_block': 0,
            'goods_inventory_spot_goods_stock': 0,
            'goods_inventory_spot_goods_block': 0
        }
        for type_inventory_data in goods_inventory_data:
            # 销售商品采购在途库存
            if type_inventory_data['type'] == 1:
                goods_inventory_dict.update({
                    'goods_inventory_purchase_on_way_stock': type_inventory_data['stock'],
                    'goods_inventory_purchase_on_way_block': type_inventory_data['block']
                })
            elif type_inventory_data['type'] == 2:
                goods_inventory_dict.update({
                    'goods_inventory_transfer_on_way_stock': type_inventory_data['stock'],
                    'goods_inventory_transfer_on_way_block': type_inventory_data['block']
                })
            elif type_inventory_data['type'] == 3:
                goods_inventory_dict.update({
                    'goods_inventory_spot_goods_stock': type_inventory_data['stock'],
                    'goods_inventory_spot_goods_block': type_inventory_data['block']
                })
        return goods_inventory_dict

    # 获取仓库商品总库存
    def get_wares_inventory(self, sale_sku_code, current_warehouse_id, target_warehouse_id):
        if not target_warehouse_id:
            get_ware_sku_code_sql = "SELECT DISTINCT ware_sku_code from wares_inventory where goods_sku_code = '%s' and target_warehouse_id is null;" % sale_sku_code
        else:
            get_ware_sku_code_sql = "SELECT DISTINCT ware_sku_code from wares_inventory where goods_sku_code = '%s' and target_warehouse_id ='%s';" % (
                sale_sku_code, target_warehouse_id)
        ware_sku_code_list = [data['ware_sku_code'] for data in self.db.get_all(get_ware_sku_code_sql)]
        if not ware_sku_code_list:
            return
        all_ware_sku_inventory = dict()

        for ware_sku_code in ware_sku_code_list:
            sql = """
                SELECT
                    storage_location_id,
                    stock,
                    block 
                FROM
                    wares_inventory 
                WHERE
                    goods_sku_code = '%s' 
                    AND warehouse_id = %s
                    AND ware_sku_code = '%s'
                    OR storage_location_id = -%s
                ORDER BY
                    ware_sku_code;
                """ % (
                sale_sku_code, current_warehouse_id, ware_sku_code, current_warehouse_id)
            ware_sku_inventory_data = self.db.get_all(sql)
            if not ware_sku_inventory_data:
                return
            temp_ware_sku_inventory = dict()
            for data in ware_sku_inventory_data:
                if data['storage_location_id'] is None:
                    temp_ware_sku_inventory.update(
                        {
                            "total": {'stock': data['stock'], 'block': data['block']}
                        }
                    )
                elif data['storage_location_id'] > 0:
                    temp_ware_sku_inventory.update(
                        {
                            data['storage_location_id']: {'stock': data['stock'], 'block': data['block']}}
                    )
            all_ware_sku_inventory.update({
                ware_sku_code: temp_ware_sku_inventory
            })
            get_dock_sql = "select storage_location_id,stock,block from wares_inventory where storage_location_id =-%s;" % current_warehouse_id
            dock_data = self.db.get_one(get_dock_sql)
            if dock_data:
                dock = {
                    -current_warehouse_id: {
                        "stock": dock_data['stock'],
                        "block": dock_data['block']
                    }
                }
                all_ware_sku_inventory.update(dock)
        return all_ware_sku_inventory

    def get_current_inventory(self, sale_sku_code, current_warehouse_id, target_warehouse_id):
        # 发货仓库存模型
        current_inventory = dict()
        central_inventor = self.get_central_inventory(sale_sku_code)
        if not target_warehouse_id:
            sale_sku_central_inventory = self.get_warehouse_central_inventory(sale_sku_code, current_warehouse_id)
        else:
            sale_sku_central_inventory = self.get_warehouse_central_inventory(sale_sku_code, target_warehouse_id)

        goods_inventory = self.get_goods_inventory(sale_sku_code, current_warehouse_id, target_warehouse_id)
        wares_inventory = self.get_wares_inventory(sale_sku_code, current_warehouse_id, target_warehouse_id)

        # 库存字典数据合并
        if central_inventor:
            current_inventory.update(central_inventor)
        if sale_sku_central_inventory:
            current_inventory.update(sale_sku_central_inventory)
        if goods_inventory:
            current_inventory.update(goods_inventory)
        if wares_inventory:
            current_inventory.update(wares_inventory)
        return current_inventory

    # OMS下单预占中央库存、销售商品总库存
    def oms_order_block(self, sale_sku_code, count, current_warehouse_id):
        ims_api_config['oms_order_block']['data'].update({
            "goodsSkuList": [
                {
                    "goodsSkuCode": sale_sku_code,
                    "qty": count
                }],
            "sourceNo": "OMS" + str(int(time.time())),
            "warehouseId": current_warehouse_id
        })
        res = self.send_request(**ims_api_config['oms_order_block'])
        return res

    # 采购下单
    def purchase_create_order(self, sale_sku_code, count, current_warehouse_id, target_warehouse_id):
        temp_data = {
            "goodsSkuList": [
                {
                    "goodsSkuCode": sale_sku_code,
                    "qty": count,
                    "targetWarehouseId": target_warehouse_id
                }
            ],
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "warehouseId": current_warehouse_id
        }

        ims_api_config['purchase_create_order']['data'][0].update(temp_data)
        res = self.send_request(**ims_api_config['purchase_create_order'])
        return res

    # 采购入库上架
    def purchase_into_warehouse(self, sale_sku_code, bom_version, sj_location_ids, count, current_warehouse_id,
                                target_warehouse_id):
        sale_sku_bom_detail = self.get_sale_sku_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = sale_sku_bom_detail.items()
        temp_ware_sku_list = list()
        for ware_sku, location_id in zip(ware_sku_list, sj_location_ids):
            temp_ware_sku_list.append(
                {
                    "bomQty": ware_sku[1],
                    "qty": ware_sku[1] * count,
                    "storageLocationId": location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": ware_sku[0]
                }
            )
        temp_data = {
            "goodsSkuList": [
                {
                    "bomVersion": bom_version,
                    "goodsSkuCode": sale_sku_code,
                    "wareSkuList": temp_ware_sku_list
                }
            ],
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "targetWarehouseId": target_warehouse_id,
            "warehouseId": current_warehouse_id
        }

        ims_api_config['purchase_into_warehouse']['data'].update(temp_data)
        res = self.send_request(**ims_api_config['purchase_into_warehouse'])
        return res

    # 其他入库
    def other_into_warehouse(self, ware_sku_list, current_warehouse_id, target_warehouse_id):
        ims_api_config['other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "RK" + str(int(time.time())),
                "targetWarehouseId": target_warehouse_id,
                "warehouseId": current_warehouse_id,
                "wareSkuList": ware_sku_list
            })
        res = self.send_request(**ims_api_config['other_into_warehouse'])
        return res

    # 销售出库单生成时预占
    def delivery_order_block(self, delivery_order_code, sale_sku_code, count, current_warehouse_id,
                             target_warehouse_id):
        ims_api_config['delivery_order_block']['data'].update({
            "goodsSkuList": [
                {
                    "goodsSkuCode": sale_sku_code,
                    "qty": count
                }],
            "sourceNo": delivery_order_code,
            "targetWarehouseId": target_warehouse_id,
            "warehouseId": current_warehouse_id
        })
        res = self.send_request(**ims_api_config['delivery_order_block'])
        return res

    # 分配库位库存
    def assign_location_stock(self, delivery_order_code, sale_sku_code, bom_version, count, current_warehouse_id):
        bom_detail = self.get_sale_sku_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for ware_sku, qty in bom_detail.items():
            temp_ware_sku_dict = {
                "qty": qty * count,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['assign_location_stock']['data'][0].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_code,
            "warehouseId": current_warehouse_id
        })
        res = self.send_request(**ims_api_config['assign_location_stock'])
        return res

    # 确认拣货
    def confirm_pick(self, delivery_order_code, ware_sku_list, current_warehouse_id):
        ims_api_config['confirm_pick']['data'].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_code,
            "warehouseId": current_warehouse_id
        })
        res = self.send_request(**ims_api_config['confirm_pick'])
        return res

    # 发货
    def delivery_out(self, delivery_order_code, sale_sku_code, bom_version, count, current_warehouse_id,
                     target_warehouse_id):
        bom_detail = self.get_sale_sku_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for ware_sku, qty in bom_detail.items():
            temp_ware_sku_dict = {
                "qty": qty * count,
                "wareSkuCode": ware_sku,
                "storageLocationId": -current_warehouse_id
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['delivery_out']['data'][0].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_code,
            "warehouseId": current_warehouse_id,
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

    def cancel_block_before_pick(self, delivery_order_code):
        ims_api_config['cancel_block_before_pick']['data'].update({"sourceNo": delivery_order_code})
        res = self.send_request(**ims_api_config['cancel_block_before_pick'])
        return res

    def cancel_block_after_pick(self, delivery_order_code, sale_sku_code, location_id, count, bom_version,
                                current_warehouse_id):
        bom_detail = self.get_sale_sku_bom_detail(sale_sku_code, bom_version)
        ware_sku_list = list()
        for detail in bom_detail.items():
            temp_ware_sku_dict = {
                "fromStorageLocationId": -current_warehouse_id,
                "qty": detail[1] * count,
                "toStorageLocationId": location_id,
                "toStorageLocationType": "4",
                "toTargetWarehouseId": current_warehouse_id,
                "wareSkuCode": detail[0],
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['cancel_block_after_pick']['data'].update(
            {
                "wareSkuList": ware_sku_list,
                "sourceNo": delivery_order_code
            })
        res = self.send_request(**ims_api_config['cancel_block_after_pick'])
        return res

    def add_stock_by_purchase_into_warehouse(self, sale_sku_code, bom_version, sj_location_ids, count,
                                             current_warehouse_id,
                                             target_warehouse_id):
        purchase_create_order_res = self.purchase_create_order(
            sale_sku_code,
            count,
            current_warehouse_id,
            target_warehouse_id)
        if not purchase_create_order_res or purchase_create_order_res['code'] != 200:
            return
        purchase_into_warehouse_res = self.purchase_into_warehouse(
            sale_sku_code,
            bom_version,
            sj_location_ids,
            count,
            current_warehouse_id,
            target_warehouse_id)
        return purchase_into_warehouse_res