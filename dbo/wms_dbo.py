from models.wms_model import *
from playhouse.shortcuts import model_to_dict
from utils.log_handler import logger


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
    def query_warehouse_locations(cls, kw_type, num, warehouse_id, to_warehouse_id, use_status=0):
        """
        :param int kw_type: 库位类型
        :param int num: 库位个数
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :param int use_status: 库位状态
        :return: 查询结果数据，字典格式
        """
        if not to_warehouse_id or to_warehouse_id == warehouse_id or kw_type == 6:
            items = BaseWarehouseLocation.select().where(BaseWarehouseLocation.warehouse_id == warehouse_id,
                                                         BaseWarehouseLocation.dest_warehouse_id >> None,
                                                         BaseWarehouseLocation.type == kw_type,
                                                         BaseWarehouseLocation.use_state == use_status,
                                                         BaseWarehouseLocation.state == 0
                                                         ).limit(num)
        else:
            items = BaseWarehouseLocation.select().where(BaseWarehouseLocation.warehouse_id == warehouse_id,
                                                         BaseWarehouseLocation.dest_warehouse_id == to_warehouse_id,
                                                         BaseWarehouseLocation.type == kw_type,
                                                         BaseWarehouseLocation.use_state == use_status,
                                                         BaseWarehouseLocation.state == 0
                                                         ).limit(num)
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

    @classmethod
    def query_wait_assign_demands(cls):
        """
        获取未分配的调拨需求数据
        :return: 查询结果数据，字典格式
        """
        items = TrfTransferDemand.select().where(TrfTransferDemand.state == 0, TrfTransferDemand.del_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_demand_detail(cls, demand_code):
        """
        获取指定的调拨需求数据
        :param demand_code: 调拨需求编码
        :return: 查询结果数据，字典格式
        """
        items = TrfTransferDemandDetail.select().where(TrfTransferDemandDetail.demand_code == demand_code)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_wait_receive_entry_order(cls):
        """
        获取待收货的入库单数据
        :return: 查询结果数据，字典格式
        """
        items = EnEntryOrder.select().where(EnEntryOrder.state == 1, EnEntryOrder.type == 0, EnEntryOrder.del_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_receive_entry_order_detail(cls, distribute_order_code):
        """
        获取入库单数据
        :return: 查询结果数据，字典格式
        """
        items = EnEntryOrder.select().where(EnEntryOrder.distribute_order_code == distribute_order_code,
                                            EnEntryOrder.del_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_wait_delivery_order(cls):
        """
        获取待发货的出库数据数据,状态为0（未分配）且未被拦截、未被取消，从分配库存走到发货完成
        :return: 查询结果数据，字典格式
        """
        items = TdoDeliveryOrder.select().where(TdoDeliveryOrder.state == 0, TdoDeliveryOrder.del_flag == 0,
                                                TdoDeliveryOrder.cancel_flag == 0, TdoDeliveryOrder.intercept_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_warehouse_config(cls):
        """
        获取仓库作业流程配置
        :return: 查询结果数据，字典格式
        """
        items = BaseWarehouseConfig.select(BaseWarehouseConfig.warehouse_id).distinct().where(
            BaseWarehouseConfig.del_flag == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def get_delivery_order_code_list(cls, limit=100):
        """
        获取出库单号列表
        """
        items = TdoDeliveryOrder.select(TdoDeliveryOrder.delivery_order_code).where(
            TdoDeliveryOrder.del_flag == 0).limit(limit)

        if not items:
            return None

        return [model_to_dict(i, only=[TdoDeliveryOrder.delivery_order_code])
                for i in items]

    @classmethod
    def get_workday_calendar(cls, warehouse_id, start_time, end_time):
        """
        获取仓库工作日
        :param warehouse_id: 仓库id
        :param start_time: 开始时间
        :param end_time: 结束时间
        """
        try:
            relation = BaseWorkdayConfigRelation.get(
                BaseWorkdayConfigRelation.warehouse_id == warehouse_id,
                BaseWorkdayConfigRelation.del_flag == 0
            )
        except BaseWorkdayConfigRelation.DoesNotExist:
            logger.error(f"查询不到该仓库的工作日配置，warehouse_id: {warehouse_id}")
            raise
        else:
            workday = BaseWorkdayCalendar.select().where(
                (BaseWorkdayCalendar.workday_config_id == relation.workday_config_id) &
                (BaseWorkdayCalendar.dt >= start_time) & (BaseWorkdayCalendar.dt <= end_time)
            )

            return [i.dt for i in workday]

    @classmethod
    def get_warehouse_timezone(cls, warehouse_id):
        """
        获取仓库时区
        """
        try:
            info = BaseWarehouse.get_by_id(warehouse_id)
        except BaseWarehouse.DoesNotExist:
            logger.error(f"根据仓库id查询base_warehouse表为空，warehouse_id: {warehouse_id}")
            raise
        else:
            return info.time_zone
