from logics.ums_logics import UmsLogics
from logics.ims_logics import ImsLogics
from api_request.scm_request import ScmRequest
from api_request.wms_app_request import WmsAppRequest

ums_logics = UmsLogics()
ims_logics = ImsLogics()
app_headers = ums_logics.get_app_headers()
service_headers = ums_logics.get_service_headers()

ims_request = ims_logics.ims_request
ums_request = ums_logics.ums_request

scm_request = ScmRequest(app_headers)
wms_request = WmsAppRequest(app_headers, service_headers)
