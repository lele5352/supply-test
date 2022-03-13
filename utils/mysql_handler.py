import pymysql
from utils.log_handler import logger as log


class MysqlHandler:
    # 构造函数
    def __init__(self, mysql_info, db):
        mysql_info['db'] = db

        try:
            self.conn = pymysql.connect(**mysql_info, charset='utf8')
        except:
            log.error("connectDatabase failed")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None):
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql, params)
                self.conn.commit()
        except:
            log.error("execute failed: " + sql)
            log.error(params)
            self.close()
            return False
        return True

    def executemany(self, sql, params=None):
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.executemany(sql, params)
                self.conn.commit()
        except:
            log.error("execute failed: " + sql)
            log.error(params)
            self.close()
            return False
        return True

    # 用来查询表数据
    def get_all(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchall()

    def get_one(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchone()


if __name__ == '__main__':
    wms_db = MysqlHandler('test_26', 'supply_wms')
    out_one = wms_db.get_one("select id from en_entry_order where entry_order_code = '%s'" % 'RK2107220002')
    print(out_one)
