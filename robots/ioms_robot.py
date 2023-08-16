import json
from robots.robot import AppRobot
from dbo.ioms_dbo import IOMSDBOperator
from utils.time_handler import HumanDateTime
from utils.log_handler import logger as log
from utils.json_handler import DecimalEncoder


class IOMSRobot(AppRobot):

    def __init__(self):
        self.dbo = IOMSDBOperator
        super().__init__()

    @staticmethod
    def get_stock_data(data_list, warehouse_code, negate=False):

        # 是否进行数值取反标识
        negate_flag = 1
        if negate:
            negate_flag = -1

        stock_data = next(filter(lambda x: x['warehouse_code'] == warehouse_code, data_list), {})
        return negate_flag*stock_data.get('sku_qty', 0), negate_flag*stock_data.get('price', 0)

    def cal_date_vo(self, warehouse_code, cal_date):
        """获取 期初、期末 库存数据
        :param warehouse_code: 仓库编码
        :param cal_date: 期初/期末 日期  %Y-%m-%d
        """
        sale_spot_snapshot = self.dbo.calculate_sales_snapshot(cal_date, stock_type=10)  # 成套现货
        sale_on_way_snapshot = self.dbo.calculate_sales_snapshot(cal_date, stock_type=20)  # 成套在途

        stock_spot_snapshot = self.dbo.calculate_stock_snapshot(cal_date, stock_type=10)  # 不成套现货
        stock_on_way_snapshot = self.dbo.calculate_stock_snapshot(cal_date, stock_type=20)  # 不成套在途

        complete_set_spots_num, complete_set_spots_amount = self.get_stock_data(sale_spot_snapshot, warehouse_code)
        complete_set_on_way_num, complete_set_on_way_amount = self.get_stock_data(sale_on_way_snapshot, warehouse_code)
        not_complete_set_on_way_num, not_complete_set_on_way_amount = self.get_stock_data(stock_on_way_snapshot, warehouse_code)
        not_complete_set_spots_num, not_complete_set_spots_amount = self.get_stock_data(stock_spot_snapshot, warehouse_code)

        return {
            "completeSetSpotsNum": complete_set_spots_num,
            "completeSetSpotsAmount": complete_set_spots_amount,
            "completeSetOnWayNum": complete_set_on_way_num,
            "completeSetOnWayAmount": complete_set_on_way_amount,
            "notCompleteSetOnWayNum": not_complete_set_on_way_num,
            "notCompleteSetOnWayAmount": not_complete_set_on_way_amount,
            "notCompleteSetSpotsNum": not_complete_set_spots_num,
            "notCompleteSetSpotsAmount": not_complete_set_spots_amount,
            "totalNum": sum((complete_set_spots_num, complete_set_on_way_num,
                             not_complete_set_on_way_num, not_complete_set_spots_num, )),
            "totalAmount": sum((complete_set_spots_amount, complete_set_on_way_amount,
                                not_complete_set_on_way_amount, not_complete_set_spots_amount, ))
        }

    def cal_date_flow(self, warehouse_code, start_date, end_date):
        """
        获取周期流水记录
        :param warehouse_code: 仓库编码
        :param start_date: 开始日期  %Y-%m-%d
        :param end_date: 结束日期  %Y-%m-%d
        """
        sale_in_flow = self.dbo.calculate_sales_flow(start_date, end_date, 10, 10)  # 现货成套入库
        sale_out_flow = self.dbo.calculate_sales_flow(start_date, end_date, 10, 20)  # 现货成套出库
        stock_in_flow = self.dbo.calculate_stock_flow(start_date, end_date, 10, 10)  # 现货不成套入库
        stock_out_flow = self.dbo.calculate_stock_flow(start_date, end_date, 10, 20)  # 现货不成套出库

        sale_in_on_way = self.dbo.calculate_sales_flow(start_date, end_date, 20, 10)  # 在途成套入库
        sale_out_on_way = self.dbo.calculate_sales_flow(start_date, end_date, 20, 20)  # 在途成套出库
        stock_in_on_way = self.dbo.calculate_stock_flow(start_date, end_date, 20, 10)  # 在途不成套入库
        stock_out_on_way = self.dbo.calculate_stock_flow(start_date, end_date, 20, 20)  # 在途不成套出库

        complete_spot_in_num, complete_spot_in_amount = self.get_stock_data(sale_in_flow, warehouse_code)
        complete_spot_out_num, complete_spot_out_amount = self.get_stock_data(sale_out_flow, warehouse_code, True)
        not_complete_in_num, not_complete_in_amount = self.get_stock_data(stock_in_flow, warehouse_code)

        not_complete_out_num, not_complete_out_amount = self.get_stock_data(stock_out_flow, warehouse_code, True)

        complete_way_in_num, complete_way_in_amount = self.get_stock_data(sale_in_on_way, warehouse_code)
        complete_way_out_num, complete_way_out_amount = self.get_stock_data(sale_out_on_way, warehouse_code, True)

        not_complete_way_in_num, not_complete_way_in_amount = self.get_stock_data(stock_in_on_way, warehouse_code)
        not_complete_way_out_num, not_complete_way_out_amount = self.get_stock_data(stock_out_on_way, warehouse_code, True)

        return {
            "completeSetSpotsInNum": complete_spot_in_num,
            "completeSetSpotsInAmount": complete_spot_in_amount,
            "completeSetSpotsOutNum": complete_spot_out_num,
            "completeSetSpotsOutAmount": complete_spot_out_amount,
            "notCompleteSetSpotsInNum": not_complete_in_num,
            "notCompleteSetSpotsInAmount": not_complete_in_amount,
            "notCompleteSetSpotsOutNum": not_complete_out_num,
            "notCompleteSetSpotsOutAmount": not_complete_out_amount,
            "completeSetOnWayInNum": complete_way_in_num,
            "completeSetOnWayInAmount": complete_way_in_amount,
            "completeSetOnWayOutNum": complete_way_out_num,
            "completeSetOnWayOutAmount": complete_way_out_amount,
            "notCompleteSetOnWayInNum": not_complete_way_in_num,
            "notCompleteSetOnWayInAmount": not_complete_way_in_amount,
            "notCompleteSetOnWayOutNum": not_complete_way_out_num,
            "notCompleteSetOnWayOutAmount": not_complete_way_out_amount,
            "totalNum": sum((complete_spot_in_num, complete_spot_out_num, not_complete_in_num,
                             not_complete_out_num, complete_way_in_num, complete_way_out_num,
                             not_complete_way_in_num, not_complete_way_out_num)),
            "totalAmount": sum((complete_spot_in_amount, complete_spot_out_amount, not_complete_in_amount,
                                not_complete_out_amount, complete_way_in_amount, complete_way_out_amount,
                                not_complete_way_in_amount, not_complete_way_out_amount))
        }

    def get_report_by_warehouse(self, warehouse_code, start_date, end_date):
        """
        获取指定仓库的进销存报表
        :param warehouse_code: 仓库编码
        :param start_date: 开始日期 %Y-%m-%d
        :param end_date: 结束日期 %Y-%m-%d
        """
        this_day = HumanDateTime().human_date()
        if end_date > this_day:
            end_date = this_day

        # 获取期初库存数据
        start_vo = self.cal_date_vo(warehouse_code, start_date)
        # 获取期末库存数据
        end_vo = self.cal_date_vo(warehouse_code, end_date)

        # 获取周期流水记录
        period_vo = self.cal_date_flow(warehouse_code, start_date, end_date)

        inventory_vo = {
            "warehouseCode": warehouse_code,
            "beginOfPeriodVo": start_vo,
            "endOfPeriodVo": end_vo,
            "ioFlowSumVo": period_vo
        }
        inventory_vo_json = json.dumps(inventory_vo, cls=DecimalEncoder)

        log.info(f"进销存报表计算结果: {inventory_vo_json}")

        return inventory_vo




