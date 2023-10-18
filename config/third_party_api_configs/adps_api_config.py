from config.third_party_api_configs import BizEnum
from models.adps_model import ReHmBill


class Fee(BizEnum):
    CHARGE = ("FYX001", "回款")
    REFUND = ("FYX002", "退款")


class AccountStatus(BizEnum):
    INIT = (10, "待对账")
    CONFIRM = (20, "入账确认中")
    ACCOUNT = (30, "已入账")
    ABORT = (40, "已作废")


class BrainTreeMap(BizEnum):
    payment_code = (ReHmBill.payment_code.column_name, "Invoice ID")
    card_group_code = (ReHmBill.card_group_code.column_name, "Reference Txn ID")
    external_transaction_id = (ReHmBill.external_transaction_id.column_name, "Transaction ID")
    refund_no = (ReHmBill.refund_no.column_name, "Invoice ID")
    currency = (ReHmBill.currency.column_name, "Currency")
    pay_amount = (ReHmBill.pay_amount.column_name, "Net")
