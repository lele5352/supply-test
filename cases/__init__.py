from robots.cds_robot import CDSAppRobot
from robots.oms_robot import OMSAppRobot, OMSAppIpRobot
from robots.wms_robot import WMSAppRobot, WMSTransferServiceRobot
from robots.ims_robot import IMSRobot
from robots.scm_robot import SCMRobot
from robots.pms_robot import PMSAppRobot
from robots.pwms_robot import PWMSRobot
from robots.tms_robot import HomaryTMS, TMSChannelService
from robots.adps_robot import ADPSRobot
from utils.excel_handler import ExcelTool

ims_robot = IMSRobot()

wms_app = WMSAppRobot()
wms_transfer = WMSTransferServiceRobot()
oms_app = OMSAppRobot()
oms_app_ip = OMSAppIpRobot()
scm_app = SCMRobot()
pms_app = PMSAppRobot()
cds_app = CDSAppRobot()
pwms_app = PWMSRobot()
tms_api = HomaryTMS()
tms_channel = TMSChannelService()
adps_app = ADPSRobot()
