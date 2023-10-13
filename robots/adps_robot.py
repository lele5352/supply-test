import json
import time
from copy import deepcopy

from config.third_party_api_configs.wms_api_config import *
from robots.robot import ServiceRobot, AppRobot
from dbo.adps_dbo import ADPSDBOperator
from utils.log_handler import logger as log
from utils.time_handler import HumanDateTime


class ADPSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = ADPSDBOperator
        super().__init__()

class WMSBaseServiceRobot(AppRobot):

    def __init__(self):
        self.dbo = ADPSDBOperator
        super().__init__()


    def get_hm_detail_by_db(self, payment_channel,channel_account,pay_at) -> list:
        """
        从数据库获取HM账单状态为未对账的单据
        :param str payment_channel: 支付渠道
        :param str channel_account: 签约主体
        :param str pay_at: 支付时间 "2023/07/05"


        :return list
        """
        return self.dbo.query_hm_detail(payment_channel,channel_account,pay_at)



    def get_payment_channel_detail_by_db(self, payment_channel_code, legal_entity) -> list:
        """
        从数据库获取支付渠道账单状态为未对账的单据
        :param str payment_channel_code: 支付渠道
        :param str legal_entity: 签约主体

        :return list
        """
        return self.dbo.query_payment_channel_detail(payment_channel_code, legal_entity)


    def get_base_fee_item_by_db(self) -> list:
        """
        从数据库获取可以对账的费用项
        :return list
        """
        result_sql=self.dbo.query_base_fee_item()
        reconciliation_fee_list=[]
        for i in result_sql:
            if list(filter(lambda i1: int(i1["amountType"])==100 and i1["reconciledFlag"]==10, json.loads(i["amount_conf"]))) != []:
                reconciliation_fee_list.append(i)
        return reconciliation_fee_list



    def cmp_tradeOutId(self,hm_reconcilable_detail,payment_channel_reconcilable_detail):
        match_tradeOutId = []
        hm_reconcilable_detail_new=[]

        for i in hm_reconcilable_detail:
            print(hm_reconcilable_detail)
            if i["external_transaction_id"]:
               channel_reconcilable_by_tradeOutId=list(filter(lambda x:x["trade_out_id"]==i["external_transaction_id"] and x["item_code"] == i["fee_item_code"] and x["trade_out_id"],payment_channel_reconcilable_detail))
               if channel_reconcilable_by_tradeOutId:
                   print(i)
                   match_tradeOutId.append((i["external_transaction_id"], i["fee_item_code"]))
                   hm_reconcilable_detail_new.append((i))
                   payment_channel_reconcilable_detail.remove(channel_reconcilable_by_tradeOutId[0])

        return match_tradeOutId,hm_reconcilable_detail_new,payment_channel_reconcilable_detail

    def cmp_card_group_code(self, hm_reconcilable_detail, payment_channel_reconcilable_detail):
        match_card_group_code = []
        hm_reconcilable_detail_new = []

        for i in hm_reconcilable_detail:
            print(hm_reconcilable_detail)
            if i["card_group_code"]:
                channel_reconcilable_by_cardGroupCode = list(filter(
                    lambda x: x["card_group_code"] == i["card_group_code"] and x["item_code"] == i["fee_item_code"] and
                          x["card_group_code"], payment_channel_reconcilable_detail))
                if channel_reconcilable_by_cardGroupCode:
                    print(i)
                    match_card_group_code.append((i["card_group_code"], i["fee_item_code"]))
                    hm_reconcilable_detail_new.append((i))
                    payment_channel_reconcilable_detail.remove(channel_reconcilable_by_cardGroupCode[0])

        return match_card_group_code, hm_reconcilable_detail_new, payment_channel_reconcilable_detail

    def cmp_payment_code(self, hm_reconcilable_detail, payment_channel_reconcilable_detail):
        match_payment_code = []
        hm_reconcilable_detail_new = []

        for i in hm_reconcilable_detail:
            if i["payment_code"]:
                channel_reconcilable_by_paymentCode = list(filter(
                     lambda x: x["payment_code"] == i["payment_code"] and x["item_code"] == i["fee_item_code"] and
                          x["payment_code"], payment_channel_reconcilable_detail))
                if channel_reconcilable_by_paymentCode:
                   match_payment_code.append((i["payment_code"], i["fee_item_code"]))
                   hm_reconcilable_detail_new.append((i))
                   payment_channel_reconcilable_detail.remove(channel_reconcilable_by_paymentCode[0])

        return match_payment_code, hm_reconcilable_detail_new, payment_channel_reconcilable_detail

    def Into_account(self):

            base_fee_item = [i["fee_item_code"] for i in self.get_base_fee_item_by_db()]
            payment_channel_detail = self.get_payment_channel_detail_by_db("Airwallex", "HOMARY SERVICE (UK) LIMITED")
            hm_detail = self.get_hm_detail_by_db("Airwallex", "HOMARY SERVICE (UK) LIMITED", "2023-09-01")
            hm_reconcilable_detail = list(filter(lambda x: x["fee_item_code"] in base_fee_item, hm_detail))
            payment_channel_reconcilable_detail = list(
                filter(lambda x: x["item_code"] in base_fee_item, payment_channel_detail))

            aa=self.cmp_tradeOutId(hm_reconcilable_detail, payment_channel_reconcilable_detail)
            print(aa[1])
            hm_reconcilable_detail.remove(aa[1])

            print(hm_reconcilable_detail)



# if __name__ == "__main__":
#     wms = WMSAppRobot()
#     # print(wms.entry_order_page(["FH2211022680"]))
#     # wms.delivery_order_assign_stock(["PRE-CK2211100010"])
#     # print(wms.get_delivery_order_page(["PRE-CK2211100010"]))
#     # print(wms.get_user_info())
#     # print(wms.delivery_get_pick_data("1881"))
#     # print(wms.dbo.query_wait_assign_demands())
#
#     # order_sku_list = [
#     #     {
#     #         "skuCode": "63203684930B01", "skuName": "酒柜-金色A款08 1/2 X1", "num": 2
#     #     },{
#     #         "skuCode": "63203684930B02", "skuName": "酒柜(金色)07 2/2 X5", "num": 10
#     #     }]
#     # wms.delivery_mock_package_call_back("PRE-CK2302020006",1,order_sku_list)
#     wms.delivery_mock_label_callback("PRE-CK2302020007", ["PRE-BG2302020026"], False)




wms=WMSBaseServiceRobot()

print(wms.Into_account())

