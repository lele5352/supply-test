from logics.ums_logics import UmsLogics
from logics.ims_logics import ImsLogics
from logics.wms_logics import WmsLogics
from api_request.scm_request import ScmRequest
from api_request.wms_app_request import WmsAppRequest
from api_request.ums_request import UmsRequest
from api_request.ims_request import ImsRequest

ums_request = UmsRequest()
ims_request = ImsRequest()


ums_logics = UmsLogics(ums_request)
ims_logics = ImsLogics(ims_request)

app_headers = ums_logics.get_app_headers()
service_headers = ums_logics.get_service_headers()

scm_request = ScmRequest(app_headers)
wms_request = WmsAppRequest(app_headers, service_headers)
wms_logics = WmsLogics(wms_request)