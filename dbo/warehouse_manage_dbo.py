from models.warehouse_manage_model import *
from playhouse.shortcuts import model_to_dict
from utils.log_handler import logger


class WarehouseManageDBOperator:
    @classmethod
    def stocktaking_task_by_order_code(cls, stocktaking_order_code):
        """
        盘点任务表-通过盘点单编码查询盘点任务单id和单号
        :param str stocktaking_order_code: stocktaking_order_code
        :return: 查询结果数据，列表格式:[(id,no)]
        """
        query = TsoStocktakingTask.select().where(TsoStocktakingTask.stocktaking_order_code == stocktaking_order_code)
        tast_list = [(i.id, i.stocktaking_task_code) for i in query]
        if not query:
            return
        return tast_list


if __name__ == '__main__':
    wm = WarehouseManageDBOperator()
    print(wm.stocktaking_task_by_order_code("PD2306280008"))

