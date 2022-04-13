from logics.ums_logics import UmsLogics
from logics.ims_logics import ImsLogics

ums_logics = UmsLogics()
ims_logics = ImsLogics()
app_headers = ums_logics.get_app_headers()
service_headers = ums_logics.get_service_headers()

ims_request = ims_logics.ims_request
