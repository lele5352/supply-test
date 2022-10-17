from utils.excel_handler import get_excel_data

# 其他入库数据
fhc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "fhc_cp_other_in")
bhc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "bhc_cp_other_in")
zzc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "zzc_cp_other_in")
fhc_lp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "fhc_lp_other_in")
bhc_lp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "bhc_lp_other_in")
zzc_lp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "zzc_lp_other_in")

if __name__ == '__main__':
    print(fhc_cp_other_in_data)
