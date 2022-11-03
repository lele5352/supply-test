from testcase import wms_logics

ck_order_list = ["PRE-CK2205060577", "PRE-CK2205060578", "PRE-CK2205060579", "PRE-CK2205060580", "PRE-CK2205060581",
                 "PRE-CK2205060582", "PRE-CK2205060583", "PRE-CK2205060584", "PRE-CK2205060585", "PRE-CK2205060586",
                 "PRE-CK2205060587", "PRE-CK2205060588", "PRE-CK2205060589", "PRE-CK2205060590", "PRE-CK2205060591",
                 "PRE-CK2205060592", "PRE-CK2205060593", "PRE-CK2205060594", "PRE-CK2205060595", "PRE-CK2205060596",
                 "PRE-CK2205060597", "PRE-CK2205060598", "PRE-CK2205060599", "PRE-CK2205060600", "PRE-CK2205060601",
                 "PRE-CK2205060602", "PRE-CK2205060603", "PRE-CK2205060604", "PRE-CK2205060605", "PRE-CK2205060606",
                 "PRE-CK2205060607", "PRE-CK2205060608", "PRE-CK2205060609", "PRE-CK2205060610", "PRE-CK2205060611",
                 "PRE-CK2205060612", "PRE-CK2205060613", "PRE-CK2205060614", "PRE-CK2205060615", "PRE-CK2205060616",
                 "PRE-CK2205060617", "PRE-CK2205060618", "PRE-CK2205060619", "PRE-CK2205060620", "PRE-CK2205060621",
                 "PRE-CK2205060622", "PRE-CK2205060623", "PRE-CK2205060624", "PRE-CK2205060625", "PRE-CK2205060626",
                 "PRE-CK2205060627", "PRE-CK2205060628", "PRE-CK2205060629", "PRE-CK2205060630", "PRE-CK2205060631",
                 "PRE-CK2205060632", "PRE-CK2205060633", "PRE-CK2205060634", "PRE-CK2205060635", "PRE-CK2205060636",
                 "PRE-CK2205060637", "PRE-CK2205060638", "PRE-CK2205060639", "PRE-CK2205060640", "PRE-CK2205060641",
                 "PRE-CK2205060642", "PRE-CK2205060643", "PRE-CK2205060644", "PRE-CK2205060645", "PRE-CK2205060646",
                 "PRE-CK2205060647", "PRE-CK2205060648", "PRE-CK2205060649", "PRE-CK2205060650", "PRE-CK2205060651",
                 "PRE-CK2205060652", "PRE-CK2205060653", "PRE-CK2205060654", "PRE-CK2205060655", "PRE-CK2205060656",
                 "PRE-CK2205060657", "PRE-CK2205060658", "PRE-CK2205060659", "PRE-CK2205060660", "PRE-CK2205060661",
                 "PRE-CK2205060662", "PRE-CK2205060663", "PRE-CK2205060664", "PRE-CK2205060665", "PRE-CK2205060666",
                 "PRE-CK2205060667", "PRE-CK2205060668", "PRE-CK2205060669", "PRE-CK2205060670", "PRE-CK2205060671",
                 "PRE-CK2205060672", "PRE-CK2205060673", "PRE-CK2205060674", "PRE-CK2205060675", "PRE-CK2205060676",
                 "PRE-CK2205060677", "PRE-CK2205060678", "PRE-CK2205060679", "PRE-CK2205060680", "PRE-CK2205060681",
                 "PRE-CK2205060682", "PRE-CK2205060683", "PRE-CK2205060684", "PRE-CK2205060685", "PRE-CK2205060686",
                 "PRE-CK2205060687", "PRE-CK2205060688", "PRE-CK2205060689", "PRE-CK2205060690", "PRE-CK2205060691",
                 "PRE-CK2205060692", "PRE-CK2205060693", "PRE-CK2205060694", "PRE-CK2205060695", "PRE-CK2205060696",
                 "PRE-CK2205060697", "PRE-CK2205060698", "PRE-CK2205060699", "PRE-CK2205060700", "PRE-CK2205060701",
                 "PRE-CK2205060702", "PRE-CK2205060703", "PRE-CK2205060704", "PRE-CK2205060705", "PRE-CK2205060706",
                 "PRE-CK2205060707", "PRE-CK2205060708", "PRE-CK2205060709", "PRE-CK2205060710", "PRE-CK2205060711",
                 "PRE-CK2205060712", "PRE-CK2205060713", "PRE-CK2205060714", "PRE-CK2205060715", "PRE-CK2205060716",
                 "PRE-CK2205060717", "PRE-CK2205060718", "PRE-CK2205060719", "PRE-CK2205060720", "PRE-CK2205060721",
                 "PRE-CK2205060722", "PRE-CK2205060723", "PRE-CK2205060724", "PRE-CK2205060725", "PRE-CK2205060726"]

for ck_order in ck_order_list:
    package_list = wms_logics.query_delivery_order_package_list(ck_order)
    result = wms_logics.mock_label_callback(ck_order, package_list)
    if not result:
        print("%s回调失败！" % ck_order)
        break
