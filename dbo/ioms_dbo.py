from models.ioms_model import database as ioms_db


class IOMSDBOperator:

    @staticmethod
    def calculate_sales_snapshot(cal_date, stock_type):
        """
        计算指定日期 销售sku成套库存快照
        :param cal_date: 日期  %Y-%m-%d
        :param stock_type: 库存类型 10 现货 20 在途
        """
        with ioms_db.cursor() as cursor:
            raw_sql = (
                "select warehouse_code, sum(sku_qty) as sku_qty, sum(total_price) as price "
                "from io_sale_sku_stock_snapshot "
                "where business_time = %s and del_flag = 0 and stock_type = %s "
                "group by warehouse_code;"
            )

            cursor.execute(raw_sql, (cal_date, stock_type, ))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def calculate_stock_snapshot(cal_date, stock_type):
        """
        计算指定日期 不成套库存快照
        :param cal_date: 日期  %Y-%m-%d
        :param stock_type: 库存类型 10 现货 20 在途
        """
        with ioms_db.cursor() as cursor:
            raw_sql = (
                "select warehouse_code, sum(sku_qty*bom_percentage/100) as sku_qty, sum(total_price) as price "
                "from io_not_complete_stock_snapshot "
                "where business_time = %s and del_flag = 0 and stock_type = %s "
                "group by warehouse_code;"
            )
            cursor.execute(raw_sql, (cal_date, stock_type, ))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def calculate_sales_flow(start_date, end_date, stock_type, flow_type):
        """
        计算指定日期范围 销售sku 流水汇总
        :param start_date: 开始日期  %Y-%m-%d
        :param end_date: 结束日期  %Y-%m-%d
        :param stock_type: 库存类型 10 现货 20 在途
        :param flow_type: 流水类型 10 入库 20 出库
        """
        with ioms_db.cursor() as cursor:
            raw_sql = (
                "select warehouse_code, SUM(sku_deal_qty) AS sku_qty, SUM(total_price) AS price "
                "from io_sale_sku_business_flow "
                "where del_flag = 0 and business_time between %s and %s and stock_type = %s and flow_type = %s "
                "group by warehouse_code;"
            )
            cursor.execute(raw_sql, (start_date, end_date, stock_type, flow_type, ))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    @staticmethod
    def calculate_stock_flow(start_date, end_date, stock_type, flow_type):
        """
        计算指定日期范围 不成套流水汇总
        :param start_date: 开始日期  %Y-%m-%d
        :param end_date: 结束日期  %Y-%m-%d
        :param stock_type: 库存类型 10 现货 20 在途
        :param flow_type: 流水类型 10 入库 20 出库
        """
        with ioms_db.cursor() as cursor:
            raw_sql = (
                "select warehouse_code, SUM((sku_deal_qty * bom_percentage) / 100) as sku_qty, "
                "sum(total_price) as price "
                "from io_not_complete_stock_business_flow "
                "where del_flag = 0 and business_time between %s and %s and stock_type = %s and flow_type = %s "
                "group by warehouse_code;"
            )
            cursor.execute(raw_sql, (start_date, end_date, stock_type, flow_type,))
            cursor.connection.commit()

            columns = [desc[0] for desc in cursor.description]

            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result


