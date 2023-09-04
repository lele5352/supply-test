部署说明：

    1.安装python，使用的是3.X版本
    2.安装依赖：pip install -r requirements.txt
    3.通过gitlab clone代码到本地
    4.修改config目录下 __init__.py 文件,配置要对接的环境和登录用户信息，具体如下：

        在__init__.py文件中，写入以下内容：

            from config.env_config import prefix_config, mysql_config
            
            # 指定环境：'test160'/'test25'/'test26'/'uat'
            env = 'test160'
            
            env_prefix_config = env_config.prefix_config.get(env)
            scms_db_config = env_config.mysql_config.get(env).get("scms")
            tms_db_config = env_config.mysql_config.get(env).get("tms")
            rds_config = env_config.redis_config.get(env)
            
            user = {
                'username': '', # 你的账号
                'password': '' # 你的密码
            }
            
            xmind_config = {
                'xmind_file_path': '',
                'excel_file_path': ''
            }
            
            console_log = False  # 日志是否输出到控制台配置，默认否

使用redis:

    1.在 config目录下，env_config 文件中，添加redis配置
    2.在 config目录下，__init__.py文件中，添加配置 rds_config = env_config.redis_config.get(env)
    3.在继承了Robot的对应业务Robot类中初始化redis连接，并且执行切换db，例子如下：

        class WMSAppRobot(AppRobot):

            def __init__(self, **kwargs):
                self.dbo = WMSDBOperator
                super().__init__(**kwargs)
        
                # 初始化redis连接
                self.init_redis_client('scm')
                if self.rds:
                    self.rds.switch_db(6)
        
        初始化完成后，即可通过 self.rds 调用 get(),hget(),hgetall() 等方法操作redis


模块说明：

    - supply-test 根目录
        - config 配置文件
            - third_party_api_configs 接口配置文件夹，存放各系统接口配置文件
            - env_config 系统配置文件，用于配置域名配置和数据库配置
            - server_config 服务器账号、日志路径
            - __init__ 账号配置、环境配置引入

        - testcase 测试用例,（预期废弃，迁移到cases）
        - cases 测试用例,基于robots的业务行为方法编排测试场景

        - data_generator 基于robots的业务行为方法编排业务，用于生成业务数据
        - script 脚本文件夹，存放一些独立的测试脚本，如库存增删、xmind转化、语言包对比等测试脚本

        - robots 逻辑层，封装调用api的方法，理论上每一个业务行为封装成独立的方法
        - robot_run 基于robots的业务行为方法编排业务，用于跑各系统的业务全流程

        - dbo 各系统数据库操作
        - utils 通用工具模块
            - barcode_handler.py 生成条形码工具
            - excel_handler.py  excel操作工具类
            - log_handler.py  日志工具类
            - rsa_handler.py  rsa加密工具
            - ssh_handler.py  ssh 工具
            - time_handler.py  日期时间工具类，封装了一些常用的日期时间转换方法
            - wait_handler.py  延迟等待装饰器，可以用于异步业务场景自定义等待重试
    
        - models 数据库表模型类
        - barcodes 条形码图片文件夹
        - logs 日志文件夹
    

model生成：

    接入了ORM框架peewee，使用下面命令将现有数据库表反向生成model
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_auth > models/ums_model.py
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_wms > models/wms_model.py
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_ims > models/ims_model.py
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_oms > models/oms_model.py
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_scm > models/scm_model.py
    python3 -m pwiz -e mysql -H 10.0.0.156 -p 3306 -u erp -P supply_logistics_base > models/tms_base.py


