from robots.oms_robot import OMSAppRobot, OMSAppIpRobot
from robots.wms_robot import WMSAppRobot
from robots.ims_robot import IMSRobot

ims_robot = IMSRobot()

wms_app_robot = WMSAppRobot()
oms_app_robot = OMSAppRobot()
oms_app_ip_robot = OMSAppIpRobot()

default_delivery_warehouse_id = 513
default_stock_warehouse_id = 512
default_exchange_warehouse_id = 511

default_bom_version = 'A'

