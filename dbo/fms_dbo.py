from models.fms_model import *
from playhouse.shortcuts import model_to_dict


class FMSDBOperator:

    @staticmethod
    def bulk_insert_currency(currency_list):
        """
        :param currency_list: 汇率列表
        """
        with database.atomic():
            CurrencyRate.insert_many(currency_list).execute()


