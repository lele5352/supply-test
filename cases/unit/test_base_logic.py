"""
用于内部逻辑的单元测试
"""
from dbo.adps_dbo import ADPSDBOperator
from config.third_party_api_configs.adps_api_config import BrainTreeMap
import uuid
from utils.time_handler import HumanDateTime
from cases import adps_app


class TestDBMethod:
    """
    测试数据库操作方法
    """
    def test_batch_insert_hm(self):

        hm_list = [
            {
                "payment_channel": "HelloWorld",
                "channel_account": "Homary",
                "payment_code": str(uuid.uuid4()).split('-')[0],
                "refund_no": None,
                "fee_item_name": "回款",
                "fee_item_code": "FYX001",
                "currency": "USD",
                "pay_amount": 123.23,
                "pay_at": HumanDateTime().human_time(),
                "account_status": 10,
                "country_code": "US",
                "site": "us",
                "del_flag": 0
            },
            {
                "payment_channel": "HelloWorld",
                "channel_account": "Homary",
                "refund_no": str(uuid.uuid4()).split('-')[0],
                "fee_item_name": "退款",
                "fee_item_code": "FYX002",
                "currency": "USD",
                "pay_at": HumanDateTime().human_time(),
                "pay_amount": 123.23,
                "account_status": 10,
                "country_code": "US",
                "site": "us",
                "del_flag": 0
            }
        ]
        print(hm_list)
        ADPSDBOperator.batch_insert_hm(hm_list, batch_size=5)

    def test_create_braintree_hm(self):

        file = "../../test_data/Braintree_Popi.xlsx"
        payment_channel = 'Braintree'
        channel_account = 'POPICORNS E-COMMERCE CO., LIMITED'
        adps_app.create_hm_from_file(file, BrainTreeMap, payment_channel, channel_account, random_mis=True)

