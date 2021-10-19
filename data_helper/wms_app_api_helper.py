import copy
import time

from utils.barcode_handler import barcode_generate
from utils.request_handler import RequestHandler
from config.wms_app_api_config import wms_app_api_config
from utils.mysql_handler import MysqlHandler
from utils.log_handler import LoggerHandler
from utils.ums_handler import get_app_headers


class WmsAppApiHelper(RequestHandler):
    def __init__(self):
        self.prefix_key = 'app_26'
        # self.infix = '/api/ec-wms-api'
        self.app_headers = get_app_headers()
        super().__init__(self.prefix_key, self.app_headers)
        self.db = MysqlHandler('test_163', 'supply_wms')
        self.log_handler = LoggerHandler('WmsAppApiHelper')

    def get_warehouse_area(self, warehouse_id, area_type):
        wms_app_api_config['get_warehouse_area']['data'].update(
            {
                'warehouseAreaType': area_type,
                'warehouseId': warehouse_id
            }
        )
        res = self.send_request(**wms_app_api_config['get_warehouse_area'])
        area_id = res['data']['records'][0]['warehouseAreaId']
        return int(area_id)

    def get_location_id(self, location_code, warehouse_id):
        query_warehouse_location_id_sql = """
                SELECT
                    id 
                FROM
                    base_warehouse_location 
                WHERE
                    warehouse_location_code ='%s'
                AND warehouse_id = %s;
                """ % (location_code, warehouse_id)
        location_id = self.db.get_one(query_warehouse_location_id_sql)
        if not location_id:
            return
        return location_id['id']

    # 获取库位，先从数据库获取，获取不到则新建
    def get_location_codes(self, num, location_type, warehouse_id, target_warehouse_id=None):
        location_codes = list()
        if not target_warehouse_id:
            query_warehouse_location_code_sql = """
                    SELECT
                        warehouse_location_code 
                    FROM
                        base_warehouse_location 
                    WHERE
                        type = %s 
                        AND use_state = 0 
                        AND state = 0 
                        AND warehouse_id = %s 
                        AND dest_warehouse_id is NULL
                        AND del_flag = 0 
                        LIMIT %s
                    """ % (location_type, warehouse_id, num)
        else:
            query_warehouse_location_code_sql = """
            SELECT
                warehouse_location_code 
            FROM
                base_warehouse_location 
            WHERE
                type = %s 
                AND use_state = 0 
                AND state = 0 
                AND warehouse_id = %s 
                AND dest_warehouse_id = %s
                AND del_flag = 0 
                LIMIT %s
        """ % (location_type, warehouse_id, target_warehouse_id, num)
        locations = self.db.get_all(
            query_warehouse_location_code_sql
        )
        if not locations:
            location_codes = self.location_create(num, location_type, warehouse_id, target_warehouse_id)
            return location_codes
        # 可能存在有库位，但是数量少于需要的，这种情况需要获取已有的，创建缺的
        elif 1 <= len(locations) < num:
            for location in locations:
                location_codes.append(location['warehouse_location_code'])
            new_location_codes = self.location_create((num - len(locations)), location_type, warehouse_id,
                                                      target_warehouse_id)
            location_codes.extend(new_location_codes)
            return location_codes
        else:
            for location in locations:
                location_codes.append(location['warehouse_location_code'])
            return location_codes

    # 创建库位
    def location_create(self, num, location_type, warehouse_id, target_warehouse_id=None, extra=None):
        """
        :param location_type: 库位类型：1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位
        :param num: 新建的库位数
        :param extra: 为空时用接口配置中的参数；非空时则更新接口配置中的参数
        :param warehouse_id: 所属仓库id
        :param target_warehouse_id: 目的仓id
        :return: list 库位列表

        库位类型对应的库区类型
        1-收货库位 类型：容器库区-5
        2-质检库位 类型：容器库区-5
        3-调拨库位 类型：容器库区-5
        4-移库库位 类型：容器库区-5
        5-上架库位 类型：上架库区-1
        6-不良品库位 类型：不良品库区-2
        7-入库异常库位 类型：入库异常库区-3
        8-出库异常库位 类型：出库异常库区-4
        """
        location_area_maps = {
            1: {
                'area_type': 5,
                "code_prefix": "SH",
                "name_prefix": "SHKW"
            },
            2: {
                'area_type': 5,
                "code_prefix": "ZJ",
                "name_prefix": "ZJKW"
            },
            3: {
                'area_type': 5,
                "code_prefix": "DB",
                "name_prefix": "DBKW"
            },
            4: {
                'area_type': 5,
                "code_prefix": "YK",
                "name_prefix": "YJKW"
            },
            5: {
                'area_type': 1,
                "code_prefix": "SJ",
                "name_prefix": "SJKW"
            },
            6: {
                'area_type': 2,
                "code_prefix": "CP",
                "name_prefix": "CPKW"
            },
            7: {
                'area_type': 3,
                "code_prefix": "RKYC",
                "name_prefix": "RKYCKW"
            },
            8: {
                'area_type': 4,
                "code_prefix": "CKYC",
                "name_prefix": "CKYCKW"
            }
        }

        if extra:
            wms_app_api_config['location_create']['data'].update(extra)

        location_codes = list()
        for i in range(num):
            now = str(int(time.time() * 1000))
            location_info = {
                'warehouseLocationCode': location_area_maps[location_type]['code_prefix'] + now,
                'warehouseLocationName': location_area_maps[location_type]['name_prefix'] + now,
                'warehouseLocationType': location_type,
                'belongWarehouseAreaId': self.get_warehouse_area(warehouse_id,location_area_maps[location_type]['area_type']),
                'warehouseAreaType': location_area_maps[location_type]['area_type'],
                'belongWarehouseId': warehouse_id,
                'destWarehouseId': target_warehouse_id
            }
            print(location_info)
            wms_app_api_config['location_create']['data'].update(location_info)
            location_create_res = self.send_request(**wms_app_api_config['location_create'])
            if location_create_res['code'] != 200:
                self.log_handler.log('创建库位失败', 'ERROR')
                return
            location_codes.append(wms_app_api_config['location_create']['data']['warehouseLocationCode'])
        return location_codes

    # 确认收货，生成收货单
    def receipt_order_create(self, entry_order_code, num=1):
        """
        :param entry_order_code: string，入库单号
        :param num:int,收货单数量
        :return: 收货单编码-list、收货库位编码-list
        """
        sh_location_codes = self.get_location_codes(num, 1)
        if not (entry_order_code and sh_location_codes):
            return
        wms_app_api_config['receipt_order_create']['data'].update({'entryOrderCode': entry_order_code})

        for location_code in sh_location_codes:
            for info in wms_app_api_config['receipt_order_create']['data']['receiveLocationInfos']:
                info.update({'locationCode': location_code})
            receipt_order_create_res = self.send_request(**wms_app_api_config['receipt_order_create'])
            if receipt_order_create_res['code'] != 200:
                return
        db_data = self.db.get_all(
            "select receipt_order_code from en_receipt_order where entry_order_code ='%s'" % entry_order_code)
        sh_order_codes = [i['receipt_order_code'] for i in db_data]

        for code in sh_order_codes:
            barcode_generate(code, 'receipt_order')
        return sh_order_codes, sh_location_codes

    # 收货交接
    def receipt_handover(self, receipt_locations):
        wms_app_api_config['receipt_handover']['data'].update({'locationCodes': receipt_locations})
        receipt_handover_res = self.send_request(**wms_app_api_config['receipt_handover'])
        if receipt_handover_res['code'] == 200 and receipt_handover_res['data']['state'] == 0:
            return True

    # 质检完成，生成质检单
    def quality_order_create(self, entry_order_code, sh_order_codes, sh_location_codes, num=1):
        """
        :param sh_location_codes: list 收货库位编码
        :param sh_order_codes: list 收货单编码
        :param entry_order_code: string 入库单编码
        :param num:optional,质检单数量,不填默认为1
        :return: 质检单编码-list，质检库位编码-list
        """
        # 生成质检库位
        zj_location_codes = self.get_location_codes(num, 2)

        temp = zip(sh_location_codes, zj_location_codes, sh_order_codes)
        target_sku_list = list()

        for sh_location_code, zj_location_code, sh_order_code in temp:
            for info in wms_app_api_config['quality_order_create']['data']['skuList']:
                info.update({
                    'receiveLocationCode': sh_location_code,
                    'entryOrderCode': entry_order_code,
                    'receiveOrderCode': sh_order_code,
                    'qcLocationCode': zj_location_code,
                })
                target_sku_list.append(copy.deepcopy(info))
        wms_app_api_config['quality_order_create']['data'].update({'skuList': target_sku_list})

        quality_order_create_res = self.send_request(**wms_app_api_config['quality_order_create'])
        if quality_order_create_res['code'] != 200:
            self.log_handler.log('质检单创建失败', 'ERROR')
            return
        query_quality_order_code_sql = """
        SELECT
            quality_order_code 
        FROM
            en_quality_order 
        WHERE
            entry_order_code = '%s' 
        ORDER BY
            create_time DESC;
        """
        db_data = self.db.get_all(query_quality_order_code_sql % entry_order_code)
        zj_order_codes = [i['quality_order_code'] for i in db_data]

        for code in zj_order_codes:
            barcode_generate(code, 'quality_order')
        return zj_order_codes, zj_location_codes

    # 质检交接
    def quality_handover(self, zj_location_codes):
        wms_app_api_config['quality_handover']['data']['locationCodes'] = zj_location_codes
        quality_handover_res = self.send_request(**wms_app_api_config['quality_handover'])
        if quality_handover_res['code'] == 200 and quality_handover_res['data']['type'] == 0:
            return True

    # 上架单创建
    def shelves_order_create(self, entry_order_code, zj_location_codes, sj_location_codes):
        """
        :param sj_location_codes: list，上架库位
        :param zj_location_codes: list，质检库位
        :param entry_order_code: string，入库单号
        :return: 上架返回数据-list
        """

        temp = zip(zj_location_codes, sj_location_codes)
        for zj_location, sj_location in temp:
            wms_app_api_config['shelves_order_create']['data'].update({
                'oldLocationCode': zj_location,
                'upshelfLocationCode': sj_location
            })
            shelves_order_create_res = self.send_request(**wms_app_api_config['shelves_order_create'])
            if shelves_order_create_res['code'] != 200:
                return

        db_shelves_order_data = self.db.get_all(
            "select shelves_order_code from en_shelves_order where entry_order_code ='%s'" % entry_order_code)
        shelves_order_codes = [i['shelves_order_code'] for i in db_shelves_order_data]

        db_shelves_location_data = self.db.get_all(
            """
            select warehouse_location_code from en_shelves_order_detail where shelves_order_code in("%s");
            """ % '","'.join(shelves_order_codes)
        )
        shelves_location_codes = [i['warehouse_location_code'] for i in db_shelves_location_data]
        location_sku_info_dict = dict()
        for shelves_location_code in shelves_location_codes:
            location_sku_info = self.db.get_all(
                """select sku_code,sku_qty from en_shelves_order_detail where warehouse_location_code ="%s" 
                and shelves_order_code in("%s");
            """ % (shelves_location_code, '","'.join(shelves_order_codes))
            )
            location_sku_info_dict.update({shelves_location_code: location_sku_info})
        return location_sku_info_dict

    def package_assign_call_back(self, deliver_order_code, sale_sku_count):
        suffix = int(time.time() * 1000)

        temp_data = {
            "deliveryNo": deliver_order_code
        }

        wms_app_api_config['package_assign_call_back']['data'].update(temp_data)

        # 根据销售SKU数量更新包裹中仓库SKU的数量数量
        for package in wms_app_api_config['package_assign_call_back']['data']["packageInfo"]["packageList"]:
            package.update({
                "packageNo": "BG" + str(suffix)
            })
            for sku in package['packageSkuList']:
                sku['num'] *= sale_sku_count
        package_call_back_res = self.send_request(
            **wms_app_api_config['package_assign_call_back'])
        if package_call_back_res['code'] != 200:
            self.log_handler.log('包裹方案回调失败', 'ERROR')
            return
        return True

    def front_label_express_call_back(self, deliver_order_code):
        """
        :param deliver_order_code: string,销售出库单号
        :return:bool
        """
        # 修正来源单号、销售单号、销售单id
        suffix = int(time.time() * 1000)
        package_data = self.db.get_one(
            "select package_code from tdo_delivery_package where delivery_order_code ='%s'" % deliver_order_code)
        package_no = package_data["package_code"]
        temp_order_list_data = {
            "deliveryNo": deliver_order_code,
            "packageNo": package_no,
            "logistyNo": "logNo" + str(suffix),
            "barCode": "barcode" + str(suffix),
            "whOrderNo": "wh" + str(suffix),
            "saleNo": "saleNo" + str(suffix),
            "turnOrderNo": "turn" + str(suffix),
            "drawOrderNo": "draw" + str(suffix)
        }
        temp_data = {
            "deliveryNo": deliver_order_code
        }
        wms_app_api_config['front_label_express_order_call_back']['data'].update(temp_data)
        wms_app_api_config['front_label_express_order_call_back']['data']['orderList'][0].update(
            temp_order_list_data)
        express_order_create_res = self.send_request(
            **wms_app_api_config['front_label_express_order_call_back'])

        if express_order_create_res['code'] != 200:
            self.log_handler.log('面单回调失败', 'ERROR')
            return
        return True

    def stock_assign(self, deliver_order_codes):
        """
        :param deliver_order_codes: string,销售出库单号
        :return:bool
        """

        wms_app_api_config['stock_assign']['data'].update({"deliveryOrderCodes": deliver_order_codes})
        stock_assign_res = self.send_request(
            **wms_app_api_config['stock_assign'])

        if stock_assign_res['code'] != 200:
            self.log_handler.log('库存分配失败', 'ERROR')
            return
        return True


if __name__ == '__main__':
    pa = WmsAppApiHelper()
    # num = 1
    # sj_locations_codes = pa.get_location_codes(num, 6, 31)
    # print(sj_locations_codes)

    # code = pa.location_create(1, 6, 31)
    # code = pa.get_location_codes(3, 1, 29)
    # print(code)

    zsj_location_codes = pa.get_location_codes(2, 5, 30, 31)
    print(zsj_location_codes)
    # zsj_location_ids = [pa.get_location_id(location_code, 30) for location_code in
    #                     zsj_location_codes]
    # print(zsj_location_ids)
    # area = pa.get_warehouse_area(30, 1)
    # print(area)
