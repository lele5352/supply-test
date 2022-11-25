from models.scm_model import *
from playhouse.shortcuts import model_to_dict


class SCMDBOperator:
    @classmethod
    def query_shortage_demand(cls):
        """
        获取待执行采购流程的缺货需求（状态为待处理）
        @return: 查询结果数据，字典格式
        """
        items = ShortageDemand.select().where(ShortageDemand.shortage_demand_status == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_purchase_demand(cls):
        """
        获取待执行采购流程的采购需求（状态为待确认）
        @return: 查询结果数据，字典格式
        """
        items = PurchaseDemand.select().where(PurchaseDemand.purchase_demand_status == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_purchase_order(cls):
        """
        获取待执行采购流程的采购单（状态为待确认）
        @return: 查询结果数据，字典格式
        """
        items = PurchaseOrder.select().where(PurchaseOrder.purchase_order_status == 0)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
        return items