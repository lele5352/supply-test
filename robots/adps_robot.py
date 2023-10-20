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
            if list(filter(lambda x: int(x["amountType"])==100 and x["reconciledFlag"]==10, json.loads(i["amount_conf"]))) != []:
                reconciliation_fee_list.append(i)
        return reconciliation_fee_list

    def cmp_amount_currency(self, hm_detail, channel_detail):
        same_with_both_result=0
        same_with_amount_result=0
        same_with_currency_result=0
        # print(hm_detail,channel_detail)
        """
        判断金额，币种是否一致
        """

        if hm_detail["currency"] and hm_detail["pay_amount"] == channel_detail["trade_amount"] and hm_detail["currency"]==channel_detail["trade_currency"] :
             same_with_both_result  =1
        elif hm_detail["currency"] and hm_detail["pay_amount"] != channel_detail["trade_amount"] and hm_detail["currency"]==channel_detail["trade_currency"] :
            same_with_amount_result =1
        else:
            same_with_currency_result =1

        return same_with_both_result,same_with_amount_result,same_with_currency_result


    def cmp_tradeOutId(self,hm_reconcilable_detail,payment_channel_reconcilable_detail):
        """
        通过交易单号进行匹配
        返回二者匹配到的外部交易id，和费用项
        及hm账单匹配到的原始数据
        """
        match_tradeOutId = []
        cmp_hm_result=[]
        sum_same_with_both=0
        sum_same_with_amount=0
        sum_same_with_currency=0


        for i in hm_reconcilable_detail:

            if i["external_transaction_id"]:
               """ 循环判断 支付渠道的外部交易id 是否等于 hm账单的外部交易id  """

               channel_reconcilable_by_tradeOutId=list(filter(lambda x:x["trade_out_id"]==i["external_transaction_id"] and x["item_code"] == i["fee_item_code"] and x["trade_out_id"],payment_channel_reconcilable_detail))

               if channel_reconcilable_by_tradeOutId:

                   match_tradeOutId.append((i["external_transaction_id"], i["fee_item_code"]))
                   cmp_hm_result.append(i)

                   """
                   判断该单据是"无差异/金额不一致/币种不一致"
                   """
                   same_with_both_result, same_with_amount_result, same_with_currency_result =self.cmp_amount_currency(i,channel_reconcilable_by_tradeOutId[0])
                   sum_same_with_both+=same_with_both_result
                   sum_same_with_amount += same_with_amount_result
                   sum_same_with_currency += same_with_currency_result

                   """从渠道中进行移除已经匹配的数据"""
                   payment_channel_reconcilable_detail.remove(channel_reconcilable_by_tradeOutId[0])


        return match_tradeOutId, cmp_hm_result,{"sum_same_with_both": sum_same_with_both,
         "sum_same_with_amount": sum_same_with_amount,
         "sum_same_with_currency": sum_same_with_currency}

    def cmp_card_group_code(self, hm_reconcilable_detail, payment_channel_reconcilable_detail):
        """
                通过交易单号进行匹配
                返回二者匹配到的外部交易id，和费用项
                及hm账单匹配到的原始数据
        """
        match_card_group_code = []
        hm_match_card_detail = []
        sum_same_with_both = 0
        sum_same_with_amount = 0
        sum_same_with_currency = 0

        for i in hm_reconcilable_detail:
            """ 循环判断 支付渠道的卡组流水号 是否等于 hm账单的卡组流水号  """
            if i["card_group_code"]:
                channel_reconcilable_by_cardGroupCode = list(filter(
                    lambda x: x["card_group_code"] == i["card_group_code"] and x["item_code"] == i["fee_item_code"] and
                          x["card_group_code"], payment_channel_reconcilable_detail))
                if channel_reconcilable_by_cardGroupCode:

                    match_card_group_code.append((i["card_group_code"], i["fee_item_code"]))
                    hm_match_card_detail.append(i)

                    """
                        判断该单据是"无差异/金额不一致/币种不一致"
                                     """
                    same_with_both_result, same_with_amount_result, same_with_currency_result = self.cmp_amount_currency(
                        i, channel_reconcilable_by_cardGroupCode[0])
                    sum_same_with_both += same_with_both_result
                    sum_same_with_amount += same_with_amount_result
                    sum_same_with_currency += same_with_currency_result
                    payment_channel_reconcilable_detail.remove(channel_reconcilable_by_cardGroupCode[0])

        return match_card_group_code, hm_match_card_detail,{"sum_same_with_both": sum_same_with_both,
         "sum_same_with_amount": sum_same_with_amount,
         "sum_same_with_currency": sum_same_with_currency}

    def cmp_payment_code(self, hm_reconcilable_detail, payment_channel_reconcilable_detail):
        match_payment_code = []
        hm_match_payment_detial = []
        sum_same_with_both = 0
        sum_same_with_amount = 0
        sum_same_with_currency = 0

        for i in hm_reconcilable_detail:
            if i["payment_code"]:
                channel_reconcilable_by_paymentCode = list(filter(
                     lambda x: x["payment_code"] == i["payment_code"] and x["item_code"] == i["fee_item_code"] and
                          x["payment_code"], payment_channel_reconcilable_detail))
                if channel_reconcilable_by_paymentCode:
                   match_payment_code.append((i["payment_code"], i["fee_item_code"]))
                   hm_match_payment_detial.append(i)

                   """
                                    判断该单据是"无差异/金额不一致/币种不一致"
                                    """
                   same_with_both_result, same_with_amount_result, same_with_currency_result = self.cmp_amount_currency(
                       i, channel_reconcilable_by_paymentCode[0])
                   sum_same_with_both += same_with_both_result
                   sum_same_with_amount += same_with_amount_result
                   sum_same_with_currency += same_with_currency_result
                   payment_channel_reconcilable_detail.remove(channel_reconcilable_by_paymentCode[0])

        return match_payment_code, hm_match_payment_detial,{"sum_same_with_both": sum_same_with_both,
         "sum_same_with_amount": sum_same_with_amount,
         "sum_same_with_currency": sum_same_with_currency}

    def Into_account(self):
            """
            获取hm账单 和支付渠道账单，分别可以对账的原始数据
            """
            base_fee_item = [i["fee_item_code"] for i in self.get_base_fee_item_by_db()]
            payment_channel_detail = self.get_payment_channel_detail_by_db("Airwallex", "HOMARY SERVICE (UK) LIMITED")
            hm_detail = self.get_hm_detail_by_db("Airwallex", "HOMARY SERVICE (UK) LIMITED", "2023-09-01")

            # payment_channel_detail = self.get_payment_channel_detail_by_db("Braintree", "POPICORNS E-COMMERCE CO., LIMITED")
            # hm_detail = self.get_hm_detail_by_db("Braintree", "POPICORNS E-COMMERCE CO., LIMITED", "2023-11-06")

            hm_reconcilable_detail = list(filter(lambda x: x["fee_item_code"] in base_fee_item, hm_detail))
            payment_channel_reconcilable_detail1 = list(
                filter(lambda x: x["item_code"] in base_fee_item, payment_channel_detail))

            log.info(f"原始HM账单的数据，共: {len(hm_reconcilable_detail)} 条")
            log.info(f"原始支付渠道账单的数据，共: {len(payment_channel_reconcilable_detail1)} 条")

            """ 根据外部交易id进行匹配 """
            match_tradeOutId,cmp_hm_result,cmp_amount_currency_tradeOutId=self.cmp_tradeOutId(hm_reconcilable_detail, payment_channel_reconcilable_detail1)

            log.info(f"Hm和渠道，可根据外部交易id进行匹配的数据，共: {len(match_tradeOutId)} 条")
            log.info('匹配的外部交易数据中，其中二者无差异的共 {0}条,金额不一致的 {1}条，币种不一致{2}条'.format(cmp_amount_currency_tradeOutId["sum_same_with_both"],
                                                                              cmp_amount_currency_tradeOutId["sum_same_with_amount"],
                                                                              cmp_amount_currency_tradeOutId["sum_same_with_currency"]))


            if cmp_hm_result:
                for _ in cmp_hm_result:
                    """ 原始hm单据 移除已经进行外部交易id的数据"""
                    hm_reconcilable_detail.remove(_)


            """ 二者根据卡组流水号进行匹配 """
            match_card, cmp_card_hm_result ,cmp_amount_currency_cardcode= self.cmp_card_group_code(hm_reconcilable_detail,
                                                                  payment_channel_reconcilable_detail1)
            log.info('匹配的卡组交易数据中，其中二者无差异的共 {0}条,金额不一致的 {1}条，币种不一致{2}条'.format(
                cmp_amount_currency_cardcode["sum_same_with_both"],
                cmp_amount_currency_cardcode["sum_same_with_amount"],
                cmp_amount_currency_cardcode["sum_same_with_currency"]))

            log.info(f"Hm和渠道，可根据卡组流水号进行匹配的数据，共: {len(match_card)} 条")
            if cmp_card_hm_result:
                for _ in cmp_card_hm_result:
                    """ 原始hm单据 移除已经进行外部交易id的数据"""
                    hm_reconcilable_detail.remove(_)

            """ 二者根据交易单号进行匹配 """
            match_paymentCode, cmp_paymentcode_hm_result,cmp_amount_currency_paymentcode = self.cmp_payment_code(hm_reconcilable_detail,
                                                                       payment_channel_reconcilable_detail1)

            log.info('匹配的卡组交易数据中，其中二者无差异的共 {0}条,金额不一致的 {1}条，币种不一致{2}条'.format(
                cmp_amount_currency_paymentcode["sum_same_with_both"],
                cmp_amount_currency_paymentcode["sum_same_with_amount"],
                cmp_amount_currency_paymentcode["sum_same_with_currency"]))

            log.info(f"Hm和渠道，可根据交易单号进行匹配的数据，共: {len(match_paymentCode)} 条")
            if cmp_paymentcode_hm_result:
                for _ in cmp_paymentcode_hm_result:
                    """ 原始hm单据 移除已经进行外部交易id的数据"""
                    hm_reconcilable_detail.remove(_)

            log.info(f"支付渠道少结的数据共：{len(hm_reconcilable_detail)}")

            log.info(f"支付渠道多结的数据共：{len(payment_channel_reconcilable_detail1)}")





