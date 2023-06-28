from models.warehouse_manage_model import *
from playhouse.shortcuts import model_to_dict
from utils.log_handler import logger


class WarehouseManageDBOperator:
    @classmethod
    def query_warehouse_info_by_id(cls, id):
        """
        :param int warehouse_id: 仓库id
        :return: 查询结果数据，字典格式
        """
        item = TsoStocktakingOrder.get_or_none(TsoStocktakingOrder.id == id)
        if not item:
            return
        return model_to_dict(item)

if __name__ == '__main__':
    wm = WarehouseManageDBOperator()
    print(wm.query_warehouse_info_by_id(2))

