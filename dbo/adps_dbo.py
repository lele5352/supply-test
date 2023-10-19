import json

from models.adps_model import database as adps_db, ReHmBill
from utils.log_handler import logger


class ADPSDBOperator:

    @staticmethod
    def query_hm_detail(payment_channel, channel_account, pay_at):
        """
        获取HM的对应渠道和签约主体的单据
        :param payment_channel: 支付渠道，str
        :param channel_account: 签约主体，str
        """
        with adps_db.cursor() as cursor:
            raw_sql = (
                "select id,payment_code,card_group_code,external_transaction_id,fee_item_code "
                "from re_hm_bill "
                "where payment_channel = %s and del_flag = 0 and channel_account = %s and pay_at <= %s;"
            )
            cursor.execute(raw_sql, (payment_channel, channel_account, pay_at))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def query_base_fee_item():
        """
        获取目前生效的费用项信息
        :param payment_channel: 支付渠道，str
        :param channel_account: 签约主体，str
        """
        with adps_db.cursor() as cursor:
            raw_sql = (
                "select fee_item_name,fee_item_code,fee_item_category,amount_conf "
                "from base_fee_item "
                "where del_flag=0 ;"
            )
            cursor.execute(raw_sql)
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def query_payment_channel_detail(payment_channel_code, legal_entity):
        """
        获取HM的对应渠道和签约主体的单据
        :param payment_channel: 支付渠道，str
        :param channel_account: 签约主体，str
        """
        with adps_db.cursor() as cursor:
            raw_sql = (

                "select rbd.bill_code,rbd.payment_code,rbd.item_code,rbd.trade_out_id,rbd.card_group_code,rbd.commission_relate_id "
                "from re_payment_channel_bill_detail rbd "
                "left join  re_payment_channel_bill rb on rbd.bill_code = rb.bill_code where rb.payment_channel_code= %s and  rb.legal_entity= %s  and  rbd.state =10 and rbd.del_flag=0;"
            )
            cursor.execute(raw_sql, (payment_channel_code, legal_entity))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def batch_insert_hm(hm_list: list, batch_size):
        """
        批量 insert hm 账单
        :param hm_list: list of hm
        :param batch_size:  number of batch
        """
        if not isinstance(hm_list, list):
            raise TypeError('Parameter hm_list is expected to be of type list')

        all_cnt = len(hm_list)

        for i in range(0, all_cnt, batch_size):

            batch = hm_list[i:i + batch_size]
            logger.info(f"执行分批写入hm账单，总条数 {all_cnt} ，本次提交数量{len(batch)}")

            with adps_db.atomic():
                ReHmBill.insert_many(batch).execute()


# if __name__ == '__main__':
#     adps = ADPSDBOperator()
#     print(adps.query_payment_channel_detail("Airwallex", "HOMARY SERVICE (UK) LIMITED"))
