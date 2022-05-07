from models.wms_model import *
from playhouse.shortcuts import model_to_dict


class WMSDBOperator:
    @classmethod
    def query_warehouse_info_by_id(cls, warehouse_id):
        """
        :param int warehouse_id: 仓库id
        :return: 查询结果数据，字典格式
        """

        item = BaseWarehouse.get_or_none(BaseWarehouse.id == warehouse_id)
        if not item:
            return
        return model_to_dict(item)

    @classmethod
    def query_warehouse_info_by_code(cls, warehouse_code):
        """
        :param str warehouse_code: 仓库编码
        :return: 查询结果数据，字典格式
        """
        item = BaseWarehouse.get_or_none(BaseWarehouse.warehouse_code == warehouse_code)
        if not item:
            return
        return model_to_dict(item)

    @classmethod
    def query_warehouse_location_info_by_id(cls, location_id):
        """
        :param int location_id: 库位id
        :return: 查询结果数据，字典格式
        """

        item = BaseWarehouseLocation.get_or_none(BaseWarehouseLocation.id == location_id)
        if not item:
            return
        return model_to_dict(item)

    @classmethod
    def query_warehouse_location_info_by_code(cls, location_code):
        """
        :param str location_code: 库位编码
        :return: 查询结果数据，字典格式
        """
        item = BaseWarehouseLocation.get_or_none(BaseWarehouseLocation.warehouse_location_code == location_code)
        if not item:
            return
        return model_to_dict(item)

    @classmethod
    def query_warehouse_locations(cls, kw_type, num, warehouse_id, to_warehouse_id):
        """
        :param int kw_type: 库位类型
        :param int num: 库位个数
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :return: 查询结果数据，字典格式
        """
        if not to_warehouse_id or to_warehouse_id == warehouse_id or kw_type == 6:
            items = BaseWarehouseLocation.select().where(BaseWarehouseLocation.warehouse_id == warehouse_id,
                                                         BaseWarehouseLocation.dest_warehouse_id >> None,
                                                         BaseWarehouseLocation.type == kw_type).limit(num)
        else:
            items = BaseWarehouseLocation.select().where(BaseWarehouseLocation.warehouse_id == warehouse_id,
                                                         BaseWarehouseLocation.dest_warehouse_id == to_warehouse_id,
                                                         BaseWarehouseLocation.type == kw_type).limit(num)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_warehouse_area_info_by_type(cls, warehouse_id, area_type):
        """
        :param int warehouse_id: 仓库id
        :param int area_type: 库区类型
        :return: 查询结果数据，字典格式
        """
        item = BaseWarehouseArea.get_or_none(BaseWarehouseArea.warehouse_id == warehouse_id,
                                             BaseWarehouseArea.type == area_type)
        if not item:
            return
        return model_to_dict(item)

    @classmethod
    def query_delivery_order_package_info(cls, delivery_order_code):
        """
        :param string delivery_order_code: 销售出库单号
        :return: 查询结果数据，字典格式
        """
        items = TdoDeliveryPackage.select().where(TdoDeliveryPackage.delivery_order_code == delivery_order_code,
                                                  TdoDeliveryPackage.del_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items
