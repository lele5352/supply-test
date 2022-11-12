from robots.oms_robot import OMSAppRobot, OMSAppIpRobot
from robots.wms_robot import WMSAppRobot, WMSTransferServiceRobot
from robots.ims_robot import IMSRobot
from robots.scm_robot import SCMRobot
from utils.excel_handler import get_excel_data

ims = IMSRobot()

wms_app = WMSAppRobot()
wms_transfer = WMSTransferServiceRobot()
oms_app = OMSAppRobot()
oms_app_ip = OMSAppIpRobot()
scm_app = SCMRobot()

default_delivery_warehouse_id = 513
default_stock_warehouse_id = 512
default_exchange_warehouse_id = 511

default_bom_version = 'A'
