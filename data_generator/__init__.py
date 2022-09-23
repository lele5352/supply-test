from logics.ums_logics import UmsLogics
from logics.ims_logics import ImsLogics
from logics.wms_logics import WmsLogics
from robots.scm_robot import SCMRobot
from robots.wms_robot import WMSRobot
from robots.ums_robot import UmsRequest
from robots.ims_robot import IMSRobot

ums_request = UmsRequest()
ims_request = IMSRobot()


ums_logics = UmsLogics(ums_request)
ims_logics = ImsLogics(ims_request)

app_headers = ums_logics.get_app_headers()
service_headers = ums_logics.get_service_headers()

scm_request = SCMRobot(app_headers)
wms_request = WMSRobot(app_headers, service_headers)
wms_logics = WmsLogics(wms_request)