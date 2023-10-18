import json
import os
import time
from copy import deepcopy

from config.third_party_api_configs.wms_api_config import *
from config.third_party_api_configs.adps_api_config import *
from robots.robot import ServiceRobot, AppRobot
from dbo.adps_dbo import ADPSDBOperator
from utils.log_handler import logger as log
from utils.time_handler import HumanDateTime
from utils.excel_handler import ExcelTool


class ADPSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = ADPSDBOperator
        super().__init__()

    def create_hm_from_file(self, file_path, key_config: BrainTreeMap,
                            payment_channel, channel_account):
        """
        读取excel文件，解析为hm账单
        """
        data_list = []
        pay_at = HumanDateTime().human_time()
        abs_file_path = os.path.abspath(file_path)
        raw_data = ExcelTool(abs_file_path).multi_read2dict()
        if not raw_data:
            raise ValueError("解析hm账单数据为空")

        for row in raw_data:

            data = {"payment_channel": payment_channel, "channel_account": channel_account, "pay_at": pay_at,
                    "country_code": "US", "site": "us", "card_type": "visa", "business_code": "1",
                    "business_name": "商城订单", "bill_source": 10, "create_username": "自动化批量写入",
                    "create_time": pay_at, "del_flag": 0,
                    "account_status": AccountStatus.INIT.value,
                    key_config.card_group_code.value: row[key_config.card_group_code.description],
                    key_config.external_transaction_id.value: row[key_config.external_transaction_id.description],
                    key_config.currency.value: row[key_config.currency.description],
                    key_config.pay_amount.value: row[key_config.pay_amount.description]
            }

            # 金额大于等于0 解析为 回款，小于0 则解析为 退款
            if row.get(key_config.pay_amount.description, 0) >= 0:
                data[key_config.payment_code.value] = row[key_config.payment_code.description]
                data["fee_item_name"] = Fee.CHARGE.description
                data["fee_item_code"] = Fee.CHARGE.value

            else:
                data[key_config.refund_no.value] = row[key_config.refund_no.description]
                data["fee_item_name"] = Fee.REFUND.description
                data["fee_item_code"] = Fee.REFUND.value

            data_list.append(data)

        return data_list

        # log.info(f"数据解析完成，总记录条数{len(data_list)}，开始执行批量写入")
        #
        # self.dbo.batch_insert_hm(data_list, 500)


class WMSBaseServiceRobot(AppRobot):

    def __init__(self):
        self.dbo = ADPSDBOperator
        super().__init__()

    def get_hm_detail_by_db(self, payment_channel, channel_account, pay_at) -> list:
        """
        从数据库获取HM账单状态为未对账的单据
        :param str payment_channel: 支付渠道
        :param str channel_account: 签约主体
        :param str pay_at: 支付时间 "2023/07/05"


        :return list
        """
        return self.dbo.query_hm_detail(payment_channel, channel_account, pay_at)

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
        result_sql = self.dbo.query_base_fee_item()
        reconciliation_fee_list = []
        for i in result_sql:
            if list(filter(lambda i1: int(i1["amountType"]) == 100 and i1["reconciledFlag"] == 10,
                           json.loads(i["amount_conf"]))) != []:
                reconciliation_fee_list.append(i)
        return reconciliation_fee_list

    def cmp_tradeOutId(self, hm_reconcilable_detail, payment_channel_reconcilable_detail):
        match_tradeOutId = []
        hm_reconcilable_detail_new = []

        for i in hm_reconcilable_detail:
            print(hm_reconcilable_detail)
            if i["external_transaction_id"]:
                channel_reconcilable_by_tradeOutId = list(filter(
                    lambda x: x["trade_out_id"] == i["external_transaction_id"] and x["item_code"] == i[
                        "fee_item_code"] and x["trade_out_id"], payment_channel_reconcilable_detail))
                if channel_reconcilable_by_tradeOutId:
                    print(i)
                    match_tradeOutId.append((i["external_transaction_id"], i["fee_item_code"]))
                    hm_reconcilable_detail_new.append((i))
                    payment_channel_reconcilable_detail.remove(channel_reconcilable_by_tradeOutId[0])

        return match_tradeOutId, hm_reconcilable_detail_new, payment_channel_reconcilable_detail

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

        aa = self.cmp_tradeOutId(hm_reconcilable_detail, payment_channel_reconcilable_detail)
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
#
#
# wms = WMSBaseServiceRobot()
#
# print(wms.Into_account())
