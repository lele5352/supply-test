from robots.oms_robot import OMSAppRobot, OMSAppIpRobot
from robots.wms_robot import WMSAppRobot, WMSTransferServiceRobot
from robots.ims_robot import IMSRobot
from robots.scm_robot import SCMRobot
from utils.excel_handler import get_excel_data

ims_robot = IMSRobot()

wms_app = WMSAppRobot()
wms_transfer = WMSTransferServiceRobot()
oms_app = OMSAppRobot()
oms_app_ip = OMSAppIpRobot()
scm_app = SCMRobot()