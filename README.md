部署说明：

    1.安装python，使用的是3.X版本
    2.安装依赖：pip install -r requirements.txt
    3.通过gitlab clone代码到本地
    4.修改config目录下sys_config文件,配置要对接的环境和登录用户

模块说明：

    - supply-test 根目录
    - config 配置文件
        - api_config 接口配置文件夹，存放各系统接口配置文件
        - sys_config 系统配置文件，用于配置全局变量
        - __init__ 域名配置和数据库配置
    - testcase 测试用例,基于api_request编排测试场景
    - data_generator 基于api_request编排业务流程，生成业务数据
    - script 脚本文件夹，存放脚本

    - logics 逻辑层，基于api_request编排业务逻辑
    - db_operator 各系统数据库操作
    - api_request 各系统接口原子封装

    - utils 通用工具模块
    - models 数据库表模型
    - barcodes 条形码生成文件夹
    - logs 日志文件夹


拓展说明：

    1.在config下的api_config文件夹中修改或增加系统接口配置文件，增加或修改相关接口配置
    2.在controller文件夹下增加或需改系统接口控制器，添加对应的接口调用逻辑
    3.在testcase或script中编写对应的controller引用，实现对应测试用例或脚本功能
    

model生成：

    接入了ORM框架peewee，使用下面命令将现有数据库表反向生成model
    python3 -m pwiz -e mysql -H 10.0.0.127 -p 3306 -u erp -P supply_auth > models/ums_model.py