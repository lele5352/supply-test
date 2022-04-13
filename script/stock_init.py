from controller.ims_controller import ImsController
from controller.ums_controller import UmsController
from controller.wms_app_controller import WmsAppController

ums = UmsController()
wms = WmsAppController(ums)
ims = ImsController()


# 获取初始库存
def get_wares_inventory_total(sale_sku, target_warehouse_id):
    wares_inventory = ims.get_wares_inventory_by_target_warehouse_id(sale_sku, target_warehouse_id)
    return wares_inventory


def get_wares_inventory(sale_sku, warehouse_id):
    wares_inventory = ims.get_wares_inventory_by_warehouse_id(sale_sku, warehouse_id)
    return wares_inventory


def get_format_excel_data(excel):
    excel_data = ims.get_import_stock_excel_data(excel)
    result_dict = dict()
    for data in excel_data:
        if data['status'] != '良品':
            continue
        warehouse_id = wms.ck_code_to_id(data['warehouseCode'])
        location_id = wms.kw_code_to_id(data['storageLocationCode'])

        if warehouse_id not in result_dict:
            result_dict.update({
                warehouse_id: {
                    data['wareSkuCode']: {
                        location_id: {'stock': data['stock'], 'block': 0},
                        '0': {'stock': data['stock'], 'block': 0},
                        '3': {'stock': data['stock'], 'block': 0}
                    }
                }})
        elif data['wareSkuCode'] not in result_dict[warehouse_id]:
            result_dict[warehouse_id].update({
                data['wareSkuCode']: {
                    location_id: {'stock': data['stock'], 'block': 0},
                    '0': {'stock': data['stock'], 'block': 0},
                    '3': {'stock': data['stock'], 'block': 0}
                }
            })
        elif location_id not in result_dict[warehouse_id][data['wareSkuCode']]:

            result_dict[warehouse_id][data['wareSkuCode']].update(
                {location_id: {'stock': data['stock'], 'block': 0}}
            )
            result_dict[warehouse_id][data['wareSkuCode']]['0']['stock'] += data['stock']
            result_dict[warehouse_id][data['wareSkuCode']]['3']['stock'] += data['stock']

    return result_dict


def asset_wares_inventory_init(origin_data, excel_data, sale_sku, warehouse_id):
    # print(excel_data)
    for data in excel_data:
        for type_data in excel_data[data]:
            # print(data)
            if data not in origin_data:
                origin_data.update({
                    data: excel_data[data]
                })
            # print(origin_data)
            elif type_data not in origin_data[data]:
                # print(111)
                origin_data[data].update({
                    str(type_data): excel_data[data][type_data]
                })
            # print(type_data,excel_data[data][type_data])
            else:
                # print(origin_data[data][type_data]['stock'],excel_data[data][type_data]['stock'])
                origin_data[data][type_data]['stock'] += excel_data[data][type_data]['stock']
    current_wares_inventory = get_wares_inventory(sale_sku, warehouse_id)

    # print('计算出来的wares_inventory表期望库存：\n%s' % origin_data)
    # print('执行后查询出wares_inventory表的库存：\n%s' % current_wares_inventory)
    # print('测试结果---：%s' % origin_data == current_wares_inventory)
    print('wares_inventory:%s' % origin_data == current_wares_inventory)
    return origin_data == current_wares_inventory


def asset_goods_inventory_init(wares_inventory, sale_sku, warehouse_id, target_warehouse_id):
    calculate_data = calculate_goods_inventory_stock(wares_inventory)
    print(calculate_data)
    total = 0
    if calculate_data:
        for type in calculate_data:
            total += calculate_data[type][sale_sku]
    else:
        total = 0
    current_stock = ims.get_goods_inventory(sale_sku, warehouse_id, target_warehouse_id)['spot_goods_stock']
    # print('计算出来的goods表期望库存：%s' % total)
    # print('执行后查询出goods表的库存：%s' % current_stock)
    print('goods_inventory:%s' % current_stock == total)
    return current_stock == total


def asset_central_inventory_init(wares_inventory, sale_sku, warehouse_id, target_warehouse_id):
    expect_central_stock = calculate_central_inventory_stock(wares_inventory)[sale_sku]
    current_stock = ims.get_central_inventory(sale_sku, warehouse_id, target_warehouse_id)['central_stock']
    print('销售sku%s计算出来central_inventory表中的期望库存：%s' % (sale_sku, expect_central_stock))
    print('销售sku%s执行后查询出central_inventory表中的库存：%s' % (sale_sku, current_stock))
    return current_stock == expect_central_stock


def calculate_central_inventory_stock(wares_inventory):
    ware_sky_qty_list_0 = list()

    for ware_inventory in wares_inventory:
        for inventory in wares_inventory[ware_inventory]:
            if inventory == 0:
                ware_sky_qty_list_0.append(
                    (ware_inventory, wares_inventory[ware_inventory][inventory]['stock']))

    result_dict = dict()
    if ware_sky_qty_list_0:
        purchase_on_way_goods_sets = ims.calculate_sets(ware_sky_qty_list_0)
        result_dict.update(purchase_on_way_goods_sets)
    return result_dict


def calculate_goods_inventory_stock(wares_inventory):
    ware_sky_qty_list_1 = list()
    ware_sky_qty_list_2 = list()
    ware_sky_qty_list_3 = list()

    for ware_inventory in wares_inventory:
        # print(ware_inventory)
        for inventory in wares_inventory[ware_inventory]:
            # print(inventory,wares_inventory[ware_inventory][inventory])

            if inventory == '1':
                ware_sky_qty_list_1.append(
                    (ware_inventory, wares_inventory[ware_inventory][inventory]['stock']))
            if inventory == '2':
                ware_sky_qty_list_2.append(
                    (ware_inventory, wares_inventory[ware_inventory][inventory]['stock']))
            if inventory == '3':
                ware_sky_qty_list_3.append(
                    (ware_inventory, wares_inventory[ware_inventory][inventory]['stock']))
    # print(ware_sky_qty_list_1)
    # print(ware_sky_qty_list_2)
    # print(ware_sky_qty_list_3)

    result_dict = dict()
    if ware_sky_qty_list_1:
        purchase_on_way_goods_sets = ims.calculate_sets(ware_sky_qty_list_1)
        result_dict.update({
            "1": purchase_on_way_goods_sets
        })
    if ware_sky_qty_list_2:
        transfer_on_way_goods_sets = ims.calculate_sets(ware_sky_qty_list_2)
        result_dict.update({
            "2": transfer_on_way_goods_sets
        })
    if ware_sky_qty_list_3:
        location_total_goods_sets = ims.calculate_sets(ware_sky_qty_list_3)
        result_dict.update({
            "3": location_total_goods_sets
        })
    return result_dict


def stock_check(sale_skus, warehouse_id, to_warehouse_id, excel_name):
    ware_sku_inventory_dict = dict()
    # ware_sku_inventory_total_dict = dict()

    for sale_sku in sale_skus:
        print(sale_sku)
        ware_sku_inventory_dict.update(
            {sale_sku: get_wares_inventory(sale_sku, warehouse_id)}
        )
        # ware_sku_inventory_total_dict.update(
        #     {sale_sku: get_wares_inventory_total(sale_sku, to_warehouse_id)}
        # )
    # 获取导入excel的数据，格式化成指定格式
    formatted_excel_data = get_format_excel_data(excel_name)

    # 导入现货库存
    import_stock_res = ims.import_stock_excel_data(excel_name)

    assert import_stock_res['code'] == 200
    ware_check_fail_result = list()
    for sale_sku in sale_skus:
        result = asset_wares_inventory_init(ware_sku_inventory_dict[sale_sku], formatted_excel_data[warehouse_id],
                                            sale_sku, warehouse_id)
        if not result:
            ware_check_fail_result.append(sale_sku)
        asset_goods_inventory_init(ware_sku_inventory_dict[sale_sku], sale_sku, warehouse_id, to_warehouse_id)
        # asset_central_inventory_init(ware_sku_inventory_total_dict[sale_sku], sale_sku, warehouse_id, to_warehouse_id)


if __name__ == '__main__':
    excel_name = "USNJ02.xlsx"
    # USTX01_warehouse_id = 530
    # USTX01_target_warehouse_id = 530
    USNJ02_warehouse_id = 528
    USNJ02_target_warehouse_id = 528
    # USNJ01_warehouse_id = 543
    # USNJ01_target_warehouse_id = 543
    # USAT01_warehouse_id = 531
    # USAT01_target_warehouse_id = 531
    # USLA02_warehouse_id = 529
    # USLA02_target_warehouse_id = 529
    sale_skus = ['J020765', 'J04MCW000233GR', 'J04CJ000115B', 'J04MSZ000008S_DIS', 'J04MZY000002PK', 'J04MZY000002PK',
                 'J020772-US-16IN-STSV-WL-WM', 'J021099', 'J040436-5-WB', 'J040436-5-WB', 'J040436-5-WHITE',
                 'J040436-5-WHITE', 'J040436-5-WHITE', 'J04MSZ000008L', '0020987-US-BG-16IN', '07961535097',
                 'J04CJ000124BS', 'J04MCW000233GR', 'J04MCZ000004L', 'J04CJ000668NA', 'J04MSZ000008L', 'J04MSZ000051BS',
                 'J04MTZ000002', 'J04MTZ000002', 'J04MTZ000002', '37559979008', 'HM-020018-SET', 'HMUS-020002MB',
                 'J020987-US-16IN-THSV', 'J04CJ000702', 'J04MSZ000051BS', 'J04SCZ000016S', 'J04YSG000008S', 'J040719-W',
                 'J04SCZ000003W', 'J04SCZ000029', 'J040394-WHITE_NATURAL', 'J040394-WHITE_NATURAL', 'J04MTZ000015',
                 'J04MTZ000015', 'J04SCZ000008S-FRAME', 'J040436-WHITE', 'J040181-MARBLE_WHITE', 'J04MSZ000008L',
                 'J04YSG000010', 'J020001-79', 'J04CTG000027GE', 'J04CTG000052', 'J04CTG000069BL', 'J04XXJ000061BW',
                 'J09CWS000011BL', 'J04CJG000031CG', 'J04MSZ000008L', 'J04MSZ000085', 'J040143', 'J04SCZ000032',
                 'J06ZWJ000004G', 'J040734-GRAY', 'J04CJ000154A', 'J04SCZ000030', 'J04BTY000012BL', 'J020524-12-US',
                 'J020753-US', 'J021010-1', 'J021099', 'J021757-US-BG-10IN', 'J04CJ000022', 'J04RCD000070LGRL',
                 'J020363-US', 'J04MSZ000004', 'J04MSZ000004', 'J04MCW000233W', 'J04SCZ000051', 'J040402-LARGE',
                 'J040578-1-S', 'J04MSZ000008L', 'J04MSZ000008L', 'J040609', 'J020594', 'J04MST000014CG-TABLETOP',
                 'J04MSZ000008L', 'J040222-WANDN-LARGE', 'J040222-WANDN-SMALL', 'J04SJ000038W', 'J04XXJ000061GE',
                 'J040285-BLACK', 'J04MBT000024', 'J04MBT000024', 'J040181-WHITE_NATURAL', 'J040746-BEIGE',
                 '17385034717', 'J04CJ000093B', 'J04MBT000024', 'J020850-US-CHROME', 'J040410-SMALL', 'J04CJ000155',
                 'J04CTG000172W', 'J04MSZ000037L', 'J020087-4-GOLD-UK', 'J020121-1', 'J040232-BLUE', 'J040404-BLACK-S',
                 'J04CJG0000126TR', 'J04CJ000046', 'J04MSZ000051WL', 'J04CJ000124WL', 'J040241-SMALL', 'J04SCZ000033W',
                 'J09CWS000011W', 'J04CJ000268', 'J04CTG000126NA', 'J04MSZ000056', 'J040636-BLUE', 'J04YSG000004BLS',
                 'J04MBT000006S', 'J04MSZ000008L_DIS', 'J04MSZ000072', 'J04MSZ000072', 'J04MTZ000015', 'J06MMJ000010NA',
                 'J020017-32-CHROME', 'J020855-US-BLACK', 'J040181-WHITE_NATURAL', 'J04CJ000046', 'J04MST000040S',
                 'J04MSZ000033S', 'J04MSZ000033S', 'J04MSZ000033S', 'J04MSZ000033S', 'J06ZWJ000394', '17385034717',
                 'J03JGZ000024A', 'J04CJ000591', 'J04MST000032', '31247677909', 'J020021-43', 'J020987-US-16IN-THSV',
                 'J020987-US-BG', 'J04MST000011WANDB', 'J04SCZ000013L', 'J04YSG000015', 'J04SJ000030W',
                 'J040181-WHITE_BLACK', 'J040285-BLACK', 'J040636-W', 'J040181-WHITE_NATURAL', 'J040181-WHITE_NATURAL',
                 'J040636-BLUE', 'J040285-BLACK', 'J04CJG000032A', 'J040285-BLACK', 'J04CJ000154A', 'HMUS-020012CH-8IN',
                 'J020855-US-CHROME', 'J04MSZ000008L', 'J04MTZ000029', 'J040522-2-WHITE', 'J04JCY000022GR',
                 'J040436-4-BLACK', 'J040578-1-L', 'J020001-58', 'J020721-GOLD', 'J021076-US-12IN', 'J04MCW000021GR',
                 'J04MSZ000008L', 'J06ZWJ000353S', 'J040181-WHITE_NATURAL', 'J040181-WHITE_NATURAL', 'J020987-US-BG',
                 'J040671-B', 'J04CJ000046', 'J04DSG000011A', 'J04MSZ000008L', 'J04MSZ000008S_DIS', 'J04MSZ000008S',
                 'J04YSG000023', 'J06MMJ000008W', 'J070003', 'J04XXJ000061GE', 'J04MSZ000042WL', 'J040320-2-B',
                 'J04MSZ000042WL', 'J040024', 'J060033', 'J04MZY000002PK', 'J04SCZ000013S', 'J040232-BLACK',
                 'J040734-GRAY', 'J04MTZ000041L', 'J04MZY000002GE', '17385034717', 'J03JGZ000024A',
                 'J040222-WANDN-SMALL', 'J040222-WANDN-SMALL', 'J040222-WANDN-SMALL', 'J040631', 'J04MSZ000008L',
                 'J04MSZ000008L', 'J04MSZ000008L', 'J020021-44-US', 'J021112', 'J04MSZ000008S', 'J04MTZ000028',
                 'J04MZY000002PK', 'J020524-11', 'J040241-SMALL', 'J020837-MATTE_WHITE', 'J040728-W', 'J040546-L',
                 'J04JCY000015RC', 'J04MCW000011', 'J04MSZ000008L', 'J04MSZ000008L', 'J04MSZ000008L', 'J040285-BLACK',
                 'J04CJ000124WL', 'J04CJ000124WL', 'J06ZWJ000431', 'J040436-WHITE', 'J04CJ000230B', 'J04CJ000268',
                 'J04MTZ000041L', 'J09CWS000011BL', 'J040181-WHITE_NATURAL', 'J02LBF000001CH', 'J04SCZ000023',
                 'J04SCZ000023', '03300890411', 'J040232-BLACK', 'J040640-W', 'J040671-B', 'J04BTY000045GR',
                 'J04CJ000046', 'J04JCY000103DGR', 'J060033', 'J040663', 'J04MTZ000024', 'J06ZWJ000130S',
                 'J020767-US-12IN-THSV-WM', 'J021063-CH', 'J040636-BLUE', 'J04SCZ000027', 'J010980-1V-WHITE-6L',
                 'J010980-1V-WHITE-8L', 'J04CJ000591', 'J020354-US-12IN-STSV-WL', 'J04CJ000224B', 'J040546-L',
                 'J040181-WHITE_NATURAL', 'J020001-84', 'J020017-32-CHROME', 'J04JCY000076W', 'J04JXJ000004',
                 'J020725-BLACK', 'J03JHJ000017B', 'J03JHJ000024', 'J040181-WHITE_NATURAL', 'J020021-44-US',
                 'J020725-BLACK', 'J03JHJ000024', 'J03JHJ000024', 'J040162-BLANDW', 'J040181-WHITE_NATURAL',
                 'J040394-WHITE_NATURAL', 'J040394-WHITE_NATURAL', 'J040528-WHITE', 'J04BSF000059', 'J040636-BLUE',
                 'J020725-BLACK', 'J020967-US', 'J04MZY000002PK', 'J020021-43', 'J04JCY000013GR', 'J020725-BLACK',
                 'J020967-US', 'J020987-US-16IN-THSV', 'J03JHJ000017B', 'J03JHJ000024', 'J040626-WG', 'J04MCW000021GR',
                 'J04SCZ000038', 'J04CTG000171NA', 'J04SCZ000016M', 'J04MXJ000065S', 'J04MXJ000065S', 'J040241-B-S',
                 'J09CWS000011W', 'J040636-PINK', 'J040663', 'J04CJ000118', 'J040181-MARBLE_WHITE', 'J020021-43',
                 'J020987-US-16IN-THSV', 'J020987-US-20IN-THSV', 'J04CTG000171NA', 'J04BSF000121',
                 'J040222-WANDB-LARGE', 'J040241-B-S', 'J040610-GOLD', 'J04SCZ000029', 'J040571-LG-L', 'J040241-B-M',
                 'J040528-WHITE', 'J04SCZ000032', 'J04SCZ000032', 'J040528-WHITE', 'J040652', 'J04MBT000024',
                 'J040441-WHITE_WALNUT', 'J04YSG000024', '77423284394', '77423284394', 'J040652', 'J040652',
                 'J04MCW000196WN', 'J040652', 'J040652', 'J04JCY000002DGE', 'J040156-LARGE', 'J040441-WHITE_WALNUT',
                 'J04MCW000007', 'J020887-US', 'J020993-UK', 'J021010-1', 'J040232-BLACK', 'J040719-W',
                 'J04JCY000002OR', 'J04MSZ000040LA', 'J010655-1V', 'J020850-US-CHROME', 'J04SCZ000013S', 'J010655-1V',
                 'J020850-US-CHROME', 'J04MTZ000029', 'HMUS-020007BN', 'J04JCY000076W', 'J021771-US-BG-8IN',
                 'J04SCZ000007M', 'J04SCZ000007S', 'J04SCZ000033W', 'J040546-L', 'J040546-L', 'J040546', 'J04SCZ000053',
                 'J04YSG000010', 'J040360-S', 'J04JCY000076W', 'J04CJ000515', 'J04MCY000018B', 'J04MDG000159NAS',
                 'J04MSZ000008S', 'J04XXJ000061GE', 'J040360-L', 'J04PSF000039', 'J04CJ000668NA', 'J04MSZ000008S_DIS',
                 'J04MTZ000028', 'J04YSG000026L', 'J040162-BLANDW', 'J040162-BLANDW', 'J04CJ000022',
                 'HMUS-020014BN-12IN', 'J020721922', 'J040546-L', 'J04SCZ000016L', 'J04YSG000024', 'J010445-1V',
                 'J020770-US-12IN-STSV-WM', 'J040137', 'J04BSF000122', 'J04CJ000005W', 'J04YSG000027BL', 'J040455-BLUE',
                 'J04CTG000017W', 'J04CTG000171NA', 'J04CTG000205W', 'J04MCY000006BL', 'J040181-WHITE_BLACK',
                 'J040546-L', 'J010556-1V-BLACK', 'J020069-25-CH', 'J020592', 'J04YSG000027BS', 'J04SCZ000023',
                 'J11ZYT000007', 'J11ZYT000021', 'J04MSZ000008S', 'J04MSZ000037S', 'J11ZYT000007', 'J040162-BLANDW',
                 'J040609-1', 'J040738', 'J04MXJ000065L', 'J040655', 'J040655', 'J11ZYT000020', 'J04MSZ000008S_DIS',
                 'J11OXY000096K', 'J040436-5-WB', 'J04JCY000044GR', 'J04SCZ000047', 'J04MCD000025', 'J04MDG000012S',
                 'J09CJ000004G', 'H8866233-13692498', 'J04CJ000253GE', 'J04MSZ000036LA', 'J040652', 'J040360-L',
                 'J04SCZ000007S', 'J04MSZ000034WS', 'J04JXJ000004', 'J04YSG000025S', 'J070003', 'J03JGZ000082A',
                 'J04SCZ000007S', 'J04SCZ000007S', 'J04MCZ000006M', 'J04MSZ000006L', 'J040536-BLACK', 'J04CJ000515',
                 'J04CTG000205W', 'J04YSG000002BS', 'J09CJ000004G', 'J09CWS000011BL', 'J03JGZ000024A', 'J04CTG000003W',
                 'J040285-BLACK', 'J04CTG000096A', 'J06ZWJ000353S', 'J040609-1', 'J040615-W', 'J040627',
                 'HMUS-020004CH', 'J020001-84', 'J020770-US-12IN-STSV-WM', 'J04CJ000602', 'J04MST000032',
                 'J04MST000032', 'J04XXJ000043LGR', '15257553752', '17373124478', '41499245302', 'J040652',
                 'J04BTY000010B', 'J04CJ000515', 'J040181-WHITE_BLACK', 'J040285-BLACK', 'J040610-GOLD',
                 'J04SCZ000007S', 'J040441-WHITE_BLACK', 'J040664-BROWN', 'J040719-W', 'J04MDG000053CG',
                 'J04SCZ000016L', 'J04MCZ000004L', 'J04MCZ000004S', 'J04MCZ000004S', 'J11ZYT000020', 'J040734-GRAY',
                 'J04MSZ000008L', '14195358594-LOCKER', 'HMUS-020004BG', 'J020993-UK', 'J02FSF000003BN',
                 'J04CTG000175GE', 'J04MZY000002Y', 'J04YSG000025S', 'J060029-WHITE', 'HMUS-020005BG',
                 'HMUS-020012BN-10IN', 'HMUS-020012BN-8IN', 'J020025-4', 'J020069-27-MB', 'J020579', 'J020580-US',
                 'J021004', 'J021052-1-BLACK', 'J04MTZ000002', 'J070003', 'J04CTG000222GR', 'J04MTZ000041L',
                 'J04MTZ000041L', 'J06ZWJ000275L', 'J040285-BLACK', 'J04MSZ000008L_DIS', '82584022276',
                 'J040222-WANDB-LARGE', 'J04BTY000045GR', 'J04CJG000004', 'J04CTG000017B', 'J04MCZ000006S',
                 'J04BTY000027NA', 'J04BTY000046BE', 'J04SCZ000023', 'HMUS-020014BN-12IN', 'J020967-US',
                 'J020987-US-16IN-THSV', 'J040222-WANDN-LARGE', 'J040156-LARGE', 'J040733-B-NOSC', 'J04MCW000143L',
                 'J04YSG000004BLL', 'J011120-1V-BLUE', 'J020001-59', 'J020985-16IN', 'J021007-US-BG-10IN',
                 'J021052-1-BG', 'J04MSZ000008L_DIS', '11337089384', '39112371955', '39112371955', 'J04XXJ000144GE',
                 'J04CJ000022', 'J04JCY000013W', 'J04MXJ000065S', 'J04YSG000034L', 'J040162-BLANDW', 'J040162-BLANDW',
                 'J040738', 'J04CTG000175GE', 'J04MXJ000065L', 'J04YSG000009', 'J040404-WHITE-S', 'J04MSZ000008L_DIS',
                 'J04JCY000013B', 'J04MSZ000008L', 'J04MSZ000008L', 'J04MSZ000008L', 'J04CTG000135', 'J04MBT000004',
                 'J040707-1_CHAIR', 'J04CJ000022', 'J04CJ000115B', 'J04MSZ000008S_DIS', 'J04MDG000030', 'J04MDG000171',
                 'J040546-M', 'J040664-GRAY', 'J04CJ000559W', 'J04CJ000591', 'J04CJ000591', 'J040664-BROWN',
                 'J040687-LARGE', 'J04SCZ000007S', 'J04CJ000241', 'J04CTG000135', 'J04MSZ000085', 'J04SCZ000013L',
                 'J04YSG000008S', 'J040181-MARBLE_WHITE', '41499245302', 'J04SCZ000007S', 'J020520', 'J040285-BLACK',
                 'J04MSZ000008L', 'J040733-W-NOSC', 'J04CTG000135', 'J04MZY000002PK', 'J04MZY000002PK', 'J04YSG000013',
                 'J04YSG000014', 'J040636-PINK', 'J040636-PINK', 'J040636-PINK', 'J040156-LARGE', 'J04CJ000011B',
                 'J04YSG000026S', 'J011246-1V', 'J040370-WHITE', 'J04MCW000233GR', 'J04SJ000032', 'J040522-2-WHITE',
                 'J04JCY000022GR', 'J04CJ000046', 'J04SCZ000003W', '11234713765', 'J040710-S', 'J11ZYT000003',
                 'J11ZYT000003', '17373124478', 'J04CJ000124WL', 'J04CJ000124WL', '55038925677', 'J040024', 'J040024',
                 'J040232-BLACK', 'J040237798', 'J04MZY000002BL', '20433094612', '36527055284', '36527055284',
                 'J04MZY000002BL', 'J04MZY000002BL', 'J03JGZ000024A', 'J04CTG000003W', 'J04MCY000018B', 'J040536-BLACK',
                 'J04MDG000013', '77423284394', 'HMUS-020009BN', 'J040232-BLUE', 'J04CTG000210W', 'J04MSZ000017A',
                 'J04SCZ000023', 'H8866233-13692498', 'J04CTG000069BL', 'J04XXJ000061BW', 'J04YSG000002BS',
                 'J04YSG000009', 'J04YSG000015', 'J040546-M', 'J04SCZ000022', 'J040320-2', 'J060033', 'J020985-US-20IN',
                 'J04CJ000116PKANDW', 'J04CJG000060L', 'J04MCW000140', 'J04MCW000233GR', 'J04MSZ000008L_DIS',
                 'J060016-9', '32818478129', 'J04MDG000171', 'J04SCZ000003W', '96674133456', '41438148209',
                 'HM-020018-SET', 'J020149-10-US', 'J020787-9', 'J021083-US-BG', 'J02FSF000003BN', 'J040331-PINK',
                 'J04CTG000231L', 'H8866233-13692498', 'J02TSN000001GR', 'J040525-B', 'J040546-M', 'J04MDG000012S',
                 'J040134-WHITE-L', 'J04JCY000022GR', 'J04JCY000036GE', 'HMUS-020011MB-8IN', 'J020053-12-US-HOT_COLD',
                 'J020787-7', 'J04MSZ000006L', 'J04MSZ000008L', 'J11ZYT000020', 'J040181-WHITE_BLACK',
                 'J020987-US-20IN-THSV', 'J03JGZ000024A', 'J04BTY000013NA', 'J04JCY000022GR', 'J04SCZ000051',
                 'HMUS-020006MB', 'J020770-US-12IN-THSV-WM', 'J021112', 'J040156-LARGE', '14827443783', 'J03JHJ000017G',
                 'J04MSZ000007S', 'J06ZWJ000097G', '37528153385', '37528153385', 'J04MSZ000007S', 'J11ZYT000003',
                 'J04MST000040S', 'J04MXJ000039W', 'J04SCZ000013L', 'J04CTG000043', 'J04MCW000161OR', '98648607225',
                 'J04CJ000154A', 'J04CTG000135', 'J040181-MARBLE_WHITE', 'J040578-1-S', '41438148209',
                 'HMUS-020012BN-8IN', 'J020025-64', 'J040439-1-WHITE', 'J04CTG000017B', '25297066635', 'J020841-US',
                 'J04XXJ000144GE', 'J04YSG000023', 'J04SCZ000003W', 'J040636-BLUE', 'J04MSZ000085',
                 'J020725-BRUSHED_NICKEL', 'J040636-BLUE', 'J04MSZ000008L', 'J04MSZ000085', 'J04MSZ000008L',
                 'J04MSZ000008L', 'J040285-BLACK', 'J04MTZ000041L', 'HMUS-020012BN-10IN', 'J011005-1V-WHITE-S',
                 'J011249-1V-GOLD-4L', 'J01ZXD000001V1', 'J020069-27-MB', 'J040436-WHITE', 'J04JCY000080B', 'J020182',
                 'J04SJ000019GS', 'J11ZYT000020', 'J040610-GOLD', 'J04CJ000845W', 'J04CJG000011', 'J04JCY000022GR',
                 'J04CTG000025', 'J04MBT000010', 'J04CJ000189', 'J04MDG000009', 'J04MST000012', 'J11ZYT000003',
                 'J04BSF000121', 'J04CJ000375', 'J040181-WHITE_NATURAL', '77423284394', 'J04CJ000155', 'J04CJ000591',
                 'J04MSZ000008L', 'J020171-23-WITH_LED', 'J04MTZ000028', 'J04MXJ000065S', 'J04MZY000002Y',
                 'J04MZY000002Y', 'J04YSG000003BS', 'J04YSG000003GRS', 'J04YSG000006M', '39112371955',
                 'J040181-WHITE_NATURAL', 'J020025-64', 'J040232-BLUE', 'J040451', 'J040719-W', 'J04PCCY000001',
                 'J04CJ000599', 'J04SJ000030W', 'J040595', 'J04CTG000108NA', '74443094066', 'J020354-US-12IN-STSV-WL',
                 'J040285-BLACK', 'J040610-CH', 'J040320-2', 'J04CTG000199GE', 'J04SCZ000007S', 'J04SJ000010',
                 '13859145598', '13859145598', '13859145598', '13859145598', 'J04SCZ000051', 'J040181-WHITE_BLACK',
                 '07961535097', 'J040375-WHITE', 'J04CJ000022', 'J04MCW000021GR', 'J04MSZ000051BS', 'J04SCZ000051',
                 'J04MSZ000036LA', 'J04SCZ000044PK', 'J040232-BLACK', 'J04SCZ000007S', 'J04SCZ000013M', '78668192064',
                 'J020001-66', 'J020002-5-WHS', 'J020034-1-GOLD', 'J020053-13', 'J020087-4-GOLD', 'J020208-15',
                 'J020467', 'J020725-BLACK', 'J020997', 'J04CJ000124WS', 'J020001-80', 'J020069-15', 'J020084-2',
                 'J020354-US-12IN-THSV-WL', 'J021007-US-BG-10IN', 'J021771-US-BG-8IN', 'J02FSF000005', 'J040156-LARGE',
                 'J020034-1-AB', 'J04CJG000004', 'J04SCZ000038', 'J04CJ000115W', 'J04MSZ000119', 'J04MTZ000002',
                 'J04MTZ000002', 'J04MTZ000002', '11337089384', '11337089384', '11337089384', 'J040546-L',
                 '55038925677', 'J06MMJ000071B', 'J04CTG000135', 'J04MTZ000015', 'J04YSG000007S', 'J04MCD000008',
                 'J04CTG000003W', 'J04CTG000122', '40554397768', 'HMUS-020012BN-10IN', 'J020053-1-BN',
                 'J021007-US-BG-8IN', 'J04JCY000002OR', 'J04MSZ000008S', 'HMUS-020001BN', 'J020069-10',
                 'J020721-CHROME', 'J02FSF000003BN', 'J040436-4-WB', 'J040439-2-BLUE', 'J04CTG000017B', 'J020001-82',
                 'J020021-38', 'J020021-8-ABR', 'J020467', 'J020725-BLACK', 'J020725-CHROME', 'J020841-US', 'J020997',
                 'J021055-US-BLACK', 'J021067-1', 'J021073', 'J021076-US-12IN', 'J04CJ000298', 'J04MSZ000008454',
                 'J04MSZ000088B', 'J06ZWJ000098', 'HMUS-020014CH-10IN', 'J020669-WHITE', 'J020787-9', 'J040717',
                 'J04YSG000004BLM', 'J06ZWJ000098', 'J040285-BLACK', '13859145598', '13859145598', '13859145598',
                 'J04CTG000069BL', 'J04CTG000084', 'J04CTG000123', 'J04JCY000013W', 'J04JCY000065GE', 'J04JIS000068B',
                 'J04MTZ000002', 'J04YSG000009', 'J04YSG000010', 'J04JCY000013W', 'J04MST000004', 'J06MMJ000008W',
                 'J040183', 'J040615-B', '17793845829', 'HMUS-020014CH-10IN', 'J020967-US', 'J04MSZ000055W',
                 'J040522-2-WHITE', 'J04JCY000022GR', 'J09CWS000011BL', 'J03JHJ000007', 'J04CTG000069BL', 'J040360-L',
                 'J04SCZ000013M', 'H25790482-6546105', 'J04MST000032', 'J06MMJ000153B', 'J04MCW000021W',
                 'J04MSZ000006L', 'J04MSZ000008L', 'J04SCZ000038', 'J03JHJ000017G', 'J04MSZ000007S', 'J040637-ORANGE',
                 'J04YSG000021L', 'J040157-MEDIUM', 'J04BSF000121', 'J04CTG000231S', 'J04YSG000013', 'J04JCY000013B',
                 'J04MCW000011', 'J04MCZ000002M', 'J04MSZ000008L', '41996638688', 'J09CWS000011W', '64828241203',
                 'J040436-WHITE', 'J040436-WHITE', 'J040436-WHITE', 'HM-020018-SET', 'J020001-85-BG', 'J021108-BG',
                 'J040546', 'J04CJ000124WL', 'J04CJ000319W', 'J04CJ000515', 'J04CJ000591', 'J04MBT000028',
                 'J04MCZ000003CS', 'J04MSZ000051BS', 'J040603-WHITE', 'J040687-LARGE', 'J040436-WHITE', 'J040436-WHITE',
                 'J040181-MARBLE_WHITE', 'J020021-44-US', 'J04CJ000115B', 'J04YSG000024', 'J04YSG000048', 'J040696',
                 'J04BTY000045GR', 'J04MTZ000022', 'J040339', 'J040719-W', '66912117131', '66912117131', '66912117131',
                 'J04MTZ000041L', '37528153385', 'J040432-A', 'J04MSZ000007S', 'J09CJ000004G', 'J040232-BLACK',
                 'J040232-BLUE', 'J040232-BLUE', 'J040237-WITH_CHAIR', 'J040360-S', 'J040634-WHITE', 'J04MCW000015',
                 'J04YSG000023', 'J020075-15-UK', 'J040436-BLACK-MET_BASE', 'J04CJ000897', 'J04MSZ000038WL-TOP',
                 'J06ZWJ000359NA', 'J06ZWJ000359WN', 'J020001-61', 'J04CTG000121B-LEFT', 'J04JCY000080B', 'J040137',
                 'J040436-4-WHITE', 'J04MCY000016B', 'J04MXJ000065S', 'J06ZWJ000437W', 'J04MSZ000051WL', 'J060032',
                 '36367767082', 'J040360-L', 'J04SCZ000016S', 'J040222-WANDN-LARGE', '97872631499', 'J040162-BLANDW',
                 'J040603-WHITE', 'J04MTZ000024', 'J04MXJ000065L', 'HMUS-020004CH', 'J021069', 'J04CJ000483B',
                 'J040536-BLACK', 'J09CWS000011PK', 'J040609-1', 'J040615-W', '71383530929', 'J011234-1V', 'J020208-10',
                 'J04MST000011WANDB', 'J04MSZ000094B', 'J04MXJ000060W', 'J04SJ000056A', 'J020987-US-BG',
                 'J040181-WHITE_NATURAL', 'J04CJ000093B', 'J04MBT000024', 'J04MSZ000037L', 'J04MSZ000037L',
                 'J04MDG000012S', 'J020069-27-MB', 'J020572-US', 'J020993-UK', 'J04CJG000011', 'J04CJG000011',
                 'J04MSZ000040LA', 'J020855-US-BLACK', 'J04SCZ000026', 'J04YSG000003GRS', 'J04CJ000624W',
                 'J04MSZ000038WL-TOP', 'J020770-US-12IN-STSV-WM', 'J04CJ000515', 'J020053-1-BN', 'J020524-15-MB',
                 'J11ZYT000020', 'J11ZYT000020', 'J11ZYT000020', 'J11ZYT000020', 'J040231-WHITE', 'J04CJ000222B',
                 'J04MST000012', 'J04MSZ000038WL-TOP', 'J04MTZ000015', 'J04YSG000002BM', '13859145598', '13859145598',
                 'J04MSZ000038WL-TOP', 'J11ZYT000007', 'J04MTZ000041L', 'J04MTZ000041L', 'J040637-ORANGE',
                 'J04CJ000515', 'J04MBT000028', 'J04CJ000124WL', 'J06ZWJ000431', 'J04CJ000591', 'J040181-WB-BLACK-BASE',
                 'J040370-WHITE', 'J04CJG000031CG', 'J04MSZ000017B', 'J04SCZ000003W', 'J04SJ000038W', 'J04JCY000013GR',
                 'J04MXJ000065L', 'J04MZY000002Y', 'J04MZY000002Y', 'J01BXD000004V1', 'J03JHJ000017B',
                 'J040222-WANDN-LARGE', 'J040652', 'J04MCZ000004S', '71383530929', 'J04CJ000022', 'J04CJ000591',
                 'J04CTG000192B', 'J010453-1V', 'J011234-1V', 'J04MCW000021W', '45970557876', '81923784044',
                 '82584022276', 'J04MCZ000019', 'J04MSZ000056', 'J04SCZ000012', 'J060016-6', 'J06ZWJ000098',
                 'J020001-59', 'J04MCZ000016', 'J04MSZ000033S', 'J040222-WANDN-LARGE', 'J04CJ000483A', 'J04CJG000031B',
                 'J04CJ000298', 'J04XXJ000144OR', 'J06ZWJ000098', 'J040222-WANDN-LARGE', 'J040713-WHITE',
                 'J04CJG000209WS', 'J04MTZ000002', '13859145598', '13859145598', '13859145598', '13859145598',
                 'J06ZWJ000353L', 'J040181-WHITE_NATURAL', 'J04CJ000155', 'J11ZYT000020', 'J04CJ000124WL',
                 '77423284394', 'J04CTG000015', 'J04MDG000012L', 'J04MSZ000008S', 'J040609-1', 'J040222-WANDN-LARGE',
                 'J04BTY000083NA', 'J04MZY000002Y', 'J04MZY000002Y', 'J04SCZ000013M', 'J070003', 'J020001-83-US-8IN-WL',
                 'J020354-US-12IN-STSV-WL', 'J020557-US', 'J040656-WS', 'J04MSZ000045', 'J021071-MATTE_BLACK',
                 'J040615-W', 'J04CJG000209WL', 'J04MSZ000008S', 'J040592-BANDW', 'J04MCW000015', 'J04CJ000733B',
                 'J04JCY000044GR', 'J04MST000011WANDB', 'J04MSZ000017A', 'J04MCZ000004S', 'J04MCZ000004S',
                 'J04MST000014CG-FRAME', 'J04MST000014CG-TABLETOP', 'J04PCCY000001', 'J04MSZ000085', 'J04MZY000002Y',
                 'J06MMJ000021A', '71994233001', 'J040222-WANDB-SMALL', 'J040285-BLACK', 'J04CJG000209WS',
                 '30CM_EXTENSION_POLE-AB', 'HMUS-020004MB', 'J04MSZ000034WS', 'J04MZY000002Y', 'J04XXJ000061BW',
                 'J04CJ000309', 'J04CJ000515', 'J04CTG000169', 'J04MDG000013', 'J04SCZ000028', 'J04MTZ000002',
                 'J04SCZ000022', 'J020767-US-12IN-THSV-WM', 'J04BSF000139', 'J04CJ000546', 'J04CJ000668B',
                 'J04MSZ000086G', 'J06ZWJ000048G', 'J040181-WHITE_NATURAL', 'J04YSG000023', '33146587278',
                 '33146587278', 'HMUS-020007MB', 'J011250-1V', 'J020001-85-BG', 'J04BTY000045GR', 'J04CJ000124WL',
                 'J04MSZ000008S', 'J020770-US-12IN-STSV-WM', 'J040375-WHITE', 'J04CJ000483B', 'J020069-27-MB',
                 'J020323', 'J021117-US', 'J04CJ000380A', 'J04MTZ000009W', 'J04BTY000046BE', 'J04MSZ000045',
                 'J04YSG000012GR', 'J04YSG000023', 'J021117-US', 'J04BTY000045GR', 'J04CJ000591', 'J040719-W',
                 'J04SCZ000029', 'J09CWS000011W', 'J040728-W', '13859145598', '13859145598', '76584038332', 'J020182',
                 'J04CJ000277', 'J04JCY000013GR', 'J04JCY000013W', 'J04PCCY000001', 'J04SCZ000003W', '33146587290',
                 'J04BSF000019BES', 'J04MSZ000042WS', 'J04SCZ000013L', 'J020021-8-ABR', 'J020034-1-ABR', 'J020053-13',
                 'J020467', 'J020721-CHROME', 'J021069', 'J021074-CH', 'J04BTY000012BL', 'JJ04XXJ000152GR',
                 'J02ALY000001BGUSC', 'J04MSZ000088B', 'J04XXJ000016', 'J06ZWJ000098', '30804698278',
                 'J020767-US-12IN-THSV-WM', 'J04BSF000202GR', 'J11OXY000096K', 'J040658-W', 'J04CJ000668B',
                 'J04MSZ000006L', 'J04CJ000767', 'J04CJ000668NA', 'J04MDG000029', 'J09CWS000011BL', 'J040162-BLANDW',
                 'J04MSZ000007L', 'J04MSZ000007L', 'J04MSZ000007S', 'J06MMJ000049G', 'J06MMJ000049G', 'J04CTG000043',
                 'J04CTG000189NA', 'J06ZWJ000309NA', 'J04JCY000080B', 'J04MBT000004', 'J04MZY000002PK', '82584022276',
                 'J040615-B', '77423284394', 'J06MMJ000004', 'J09CWS000011BL', 'J040222-WANDB-SMALL', 'J04CJ000124WL',
                 'J04JXJ000004', 'J04XXJ000061BW', 'J040536-BLACK', 'J04CJ000804', 'J04BTY000046OR', 'J04MCZ000008',
                 'J04MSZ000036LA', 'J04MZY000002Y', 'J040436-WHITE', 'J04CJG000052PK', 'J060032', 'J040222-WANDN-LARGE',
                 'J040548-BLUE', 'J04MCZ000004S', 'J04MCZ000004S', 'J040546-L', 'J04CJ000022', 'J04SCZ000033B',
                 'J040615-B', 'J04CJ000051W', 'J04CTG000017B', 'J020065-4', 'J020208-15', 'J020210-4', 'J020359',
                 'J020576-US', 'J020721-GOLD', 'J020727-US', 'J020770-US-12IN-THSV-WM', 'J020841-US', 'J020987-US-BG',
                 'J020998-US-16IN-THSV', 'J021073', 'J021094-BLACK', 'J04BJT000048BW', 'J04MCZ000008', 'HMUS-020004BN',
                 'HMUS-020008CH', 'J04CJ000212Y', 'J04MST000023WN', 'J04MZY000002PK', 'J020034-1-ABR', 'J020701-WHITE',
                 'J020721-GOLD_CHROME', 'J021101', 'J04CJ000046', 'J11OSF000069K', 'J04JIS000023B', 'J06YWS000009',
                 'J040222-WANDN-LARGE', 'J04CJ000118', 'J04CJ000260-MARBLETOP', 'J04JCY000013W', 'J04YSG000009',
                 'J020001-66', 'J020053-10', 'J020053-16-BN', 'J020053-20', 'J020065-4', 'J020084-2', 'J020087-4-GOLD',
                 'J020210-4', 'J020467', 'J020721-GOLD', 'J020725-BLACK', 'J020987-US-BG', 'J020996', 'J021060-BN',
                 'J021087', 'J021095-BLACK', 'J02ALY000001BUSC', 'J02FSF000003BG', 'J02FSF000004BG', 'J02TSF000009WUSC',
                 'J04CJ000096GE', 'J04YSG000004GRL', 'J04YSG000023', 'J04BSF000121', 'J040410-SMALL', 'J04MSZ000006L',
                 'J04SCZ000016M', 'J04XXJ000138Y', 'J04YSG000026S', 'J020182', 'J040285-BLACK', 'J04CJG000031B',
                 '13859145598', '13859145598', '13859145598', 'J020001-79', 'J04CJ000804', 'J04MSZ000036MA',
                 'J04YSG000002WS', 'J040359', 'J04CTG000135', 'J060029-WHITE', 'J040535-WHITE', 'J040222-WANDN-LARGE',
                 'J040592-W', 'J040592-W', 'J040592-W', 'J04SCZ000013L', 'J04CTG000135', 'J040436-WHITE',
                 'J040536-BLACK', 'J04MSZ000037L', 'J04CJ000124WL', 'J04CJ000124WL', 'J06ZWJ000431', 'J040536-BLACK',
                 'J04BTY000012W', 'J040436-4-WB', 'J040436-BLACK', 'J04SCZ000032', 'J010655-1V', 'J020001-66',
                 'J020001-82', 'J020002-5-WHS', 'J020021-38', 'J020021-8-ABR', 'J020034-1-ABR', 'J020038-18',
                 'J020069-25-CH', 'J020087-4-GOLD', 'J020208-15', 'J020210-4', 'J020719', 'J020725-BLACK', 'J020841-US',
                 'J020987-US-BG', 'J021013-US', 'J021067-1', 'J021109-BLACK', 'J02FSF000006', 'J03JHJ000017G',
                 'J040432-A', 'J04MSZ000008454', 'J040285-BLACK', 'J040436-1-WHITE', 'J04CJ000604', 'J04MST000002B',
                 'J03JHJ000017G', 'J04MSZ000007L', 'J04MSZ000007S', 'J040154-MIDIUM', 'J040154-MIDIUM',
                 'J04MSZ000051WL', 'J04MSZ000063B', 'J020001-59', 'J04MCZ000016', 'J04MCZ000016', 'J04MSZ000045',
                 'J040213', 'J040278-WHITE', 'J040436-4-WB', 'J040154-MIDIUM', 'J040154-MIDIUM', 'J060033', 'J020182',
                 'J04CJ000115B', 'J04YSG000023', 'J040531-WHITE', 'J040531-WHITE', 'H8866233-13692084', 'J04PSF000088',
                 'J04CTG000043', 'J040410-SMALL', 'J040436-1-WHITE', 'J04CJ000591', 'J020001-13', 'J040610-CH',
                 'J04CJ000155', 'J04MBT000006S', 'J040592-W', 'J04CJ000033WW', 'J04MSZ000006L', 'J040232-CHAMPAGNE',
                 'J040410-SMALL', 'J040620-SET', 'J04SCZ000016M', 'J04CJ000733B', 'J04CJG000209WS', 'J04MSZ000008L',
                 'J040181-MARBLE_WHITE-WHITE_TABLE', 'J040554-WHITE', 'J04YSG000009', 'J09CWS000011PK',
                 'J04CTG000171NA', 'J040285-BLACK', 'J04CJG000209WL', '15341730838', 'HMUS-020004CH', 'HMUS-020004MB',
                 'J020354-US-12IN-STSV-WL', 'J04MST000040S', 'J04MSZ000033S', 'J04MSZ000033S', 'J04SJ000038W',
                 'J040181-WHITE_NATURAL', '76584038332', 'J040505B', 'J04CJ000351B', 'J04MXJ000004', 'P66512222',
                 'J040222-WANDB-LARGE', 'J04CTG000210CG', '88216193320', 'J040222-WANDN-LARGE', 'J06MMJ000048G',
                 'J040626-WG', 'J040626-WG', 'HMUS-020003CH', 'HMUS-020005MB', 'J020069-25', 'J020121-1',
                 'J020212-1-UK', 'J020354-US-12IN-STSV-WL', 'J04BSF000209', 'J04CJ000033WW', 'J060013-4',
                 'J040592-BANDW', 'J040592-BANDW', 'J040734-GRAY', 'J04CTG000122', 'J010917-1V-6-LIGHT',
                 'J04MSZ000030W', 'J06MMJ000021B', '98648607225', '98648607225', 'J020001-79', 'J040713-WHITE',
                 'J04MST000004', 'J06ZWJ000359WN', 'J04CJ000439SL', 'J04CTG000171NA', 'J04CTG000205W', 'J04MZY000002PK',
                 '51251156840', 'J03JGZ000024A', 'J04CTG000076L', 'J04SCZ000003W', 'J04XXJ000061GE', '17385034717',
                 'J040637-ORANGE', 'J04CJ000093B', 'J040320-2', 'H8866233-13692498', 'H8866233-13692498',
                 'J03JHJ000007', 'J040222-WANDN-LARGE', 'HMUS-020012BN-8IN', 'J020001-59', 'J020001-66', 'J020524-11',
                 'J020576-US', 'J020720-2-BLACK', 'J021091-US-MB', 'J02FSF000003BN', 'J04CJG000011', 'US1-A-PARTS',
                 'J040181-WHITE_NATURAL', 'J040181-WHITE_NATURAL', 'J020087-4-GOLD', 'J020254-US-12IN-STSV-WL',
                 'J021071-BN', 'J04MCW000187B', 'J04MSZ000008454', 'J04MSZ000040LB', 'J04XXJ000144OR', 'J06ZWJ000098',
                 'JJ04XXJ000152GR', 'J04CJ000154A', 'J04MST000002B', 'J04XXJ000071BL', 'J011249-1V-GOLD-4L',
                 'J04CJ000293B', 'J04MTZ000002', 'J04SCZ000016L', 'J040609-1', 'J040181-WHITE_NATURAL', 'J04CTG000101',
                 'J04JXJ000004', 'J04MST000040S', 'J04MST000040S', 'J04YSG000010', 'J06MMJ000008G',
                 'J040181-WHITE_NATURAL', 'J040181-WHITE_NATURAL', 'J021071-MATTE_BLACK', 'J03QS000008',
                 'J04MSZ000008S_DIS', 'J04MSZ000051BL', 'J04CJ000190', 'J04MZY000002BL', 'J04MZY000002GR',
                 'J04MZY000002Y', 'J04MZY000002Y', 'J020025-66', 'J020323', 'J020524-2', 'J04MSZ000008L_DIS',
                 'J04MZY000002PK', 'J04JXJ000004', 'J04JXJ000004', 'J04MSZ000008S_DIS', 'J04CJ000668NA',
                 'J04MSZ000008S_DIS', 'J040609-1', 'J040375-WHITE', 'J040213', 'J040455-BLUE', 'J04MTZ000041L',
                 'J04SJ000030W', 'J04MST000004', 'J04MSZ000008L_DIS', 'J040213', 'J040554-WHITE', 'J04MSZ000085',
                 'J04MZY000002GR', 'J04MZY000002Y', 'J04JCY000024OR', 'J04JCY000080B', 'J040522-1-W-L', 'J04CJ000781W',
                 'J04MSZ000051BS', 'J04YSG000010', 'J06ZWJ000359NA', 'J04CJG000209WS', 'J040636-PINK', 'J04YSG000007L',
                 'J04YSG000007L', 'J040636-PINK', 'J04JCY000001', 'J04MST000006GE', 'J04MST000006GE', 'J04CJ000190',
                 'J04CJ000190', 'J04MBT000004', 'J04MTZ000028', 'J020001-79', 'J04JCY000056GR', 'J04YSG000007L',
                 'J06MMJ000048G', 'J04MSZ000008L', 'J06MMJ000183G', 'J04CJ000057', 'J04CTG000003W', 'J04CTG000123',
                 'J040658-W', 'J04CJG000011', 'HM-020018-SET', 'HM-020018-SET', 'J020787-9', 'J021083-US-BG',
                 'J04MTZ000029', 'J020837-MATTE_WHITE', 'J040468-PINK', 'J04BSF000007S', 'J04MSZ000051WL',
                 'J06ZWJ000353S', 'J040609', 'J04YSG000010', 'J021117-US', 'J04MSZ000008S', 'J040181-WHITE_NATURAL',
                 'J04SCZ000007M', '11772900811', 'J03JHJ000017B', 'J04YSG000037', 'J04CJG000011', 'HMUS-020006BG',
                 'J021091-US-BG', 'J021108-BG', 'J04YSG000037', '20037992622', '30CM_EXTENSION_POLE-AB',
                 'J010917-1V-6-LIGHT', 'J020025-4', 'J020069-27-MB', 'J020171-5-WL-ORB', 'J020787-9', 'J021108-CH',
                 'J04BTY000011', 'J04CJ000754', 'J04CTG000205B', 'J04JCY000013B', 'J04MXJ000065L', 'J04MZY000002GE',
                 'J04MZY000002GE', 'J06MMJ000021B', 'J06MMJ000021B', 'J04CJ000115B', 'J11ZYT000021', 'J021117-US',
                 'J04MZY000002BL', 'J04MZY000002GR', 'J04MZY000002Y', 'J04MZY000002Y', 'J04CJ000754', 'J04MSZ000085',
                 'J06MMJ000021B', 'J010655-1V', 'J04CJG0000126TR', 'J04CTG000135', 'J040546-M', 'J04CJ000489A',
                 'J04MSZ000108', 'J04MSZ000108', 'J04MTZ000024', 'J04YSG000006S', 'J020021-2-ABR', 'J020021-8-ABR',
                 'J020034-1-ABR', 'J020171-17-BN', 'J020171-5-WITH_LED-BN', 'J020210-4', 'J020467', 'J020592',
                 'J020701-WHITE', 'J020719', 'J020725-BLACK', 'J020787-9', 'J020996', 'J021095-BLACK',
                 'J02ALY000001BGUSC', 'J02ASF000005USC', 'J040546-M', 'J04MSZ000040LB', 'J03JHJ000039B',
                 'J04JCY000080B', 'J04MST000005', 'J09CWS000011W', 'J03JHJ000056G', 'J04SJ000019GL', 'J04SJ000019GS',
                 'J040285-BLACK', 'J040285-BLACK', 'J04CJ000033WN', 'J04MCZ000006S', 'J040436-4-WB', 'J04CJ000037B',
                 'J04SCZ000008S-FRAME', 'J04CJG000004', 'J04SCZ000008S-TABLETOP', 'J040580-S', 'J04CTG000063',
                 'J04CTG000232', 'J011208-1-1V-5L', 'J020001-59', 'J04CJ000024B', 'J04MCW000021W', 'J04SCZ000027',
                 'J040222-WANDN-LARGE', 'J040285-BLACK', 'J04MSZ000040LB', 'J040285-BLACK', 'J04CJ000453W',
                 'J040436-WHITE', 'J020065-4', 'J020788-CHROME', 'J040576', 'J040670-W', 'J040670-W', 'J040157-MEDIUM',
                 'J04MSZ000040MA', 'J04SCZ000038', '69938157850', 'HMUS-020006BG', 'J010453-1V', 'J020361',
                 'J020863-US', 'J04CJ000858B', 'J04JCY000044GR', 'J020208-12-GOLD', 'J040181-WHITE_NATURAL',
                 'J040237-WITH_CHAIR', 'J04JCY000013GR', 'J06ZWJ000097G', 'J040436-WHITE', 'J04MDG000191WL',
                 'J09CWS000011BL', '98648607225', 'J04SJ000038W', 'J020001-13', 'J020069-19-US', 'J021019',
                 'J06ZWJ000275L', 'J04CJ000016B', 'J04MBT000028', '35253645752', 'HMUS-020004BN', 'HMUS-020012BN-8IN',
                 'J020001-59', 'J020001-66', 'J020069-27-MB', 'J021056-WITH_OVERFLOW', 'J021091-US-MB', 'J020069-27-MB',
                 'J04BTY000012W', 'J04BTY000045GR', 'J04CJ000591', 'J04SJ000019GS', 'J04MCW000192S', 'J040620-SET',
                 'J040620-SET', 'J040620-SET', 'J021112', 'J04JCY000045', 'J04MST000005', 'J04MSZ000008L',
                 'J04YSG000048', 'J040436-1-WHITE', 'J020174-BRUSHED_NICKEL', 'J020254-US-12IN-STSV-WL', 'J021029',
                 'J04MSZ000034WL', 'J04XXJ000069LGE', 'J04YSG000017M', 'J020065-4', 'J04MBT000008S', 'J04SJ000030W',
                 'J04YSG000004BLS', 'J020025-4', 'J020787-9', 'J020987-US-20IN-THSV', 'J04CTG000226GR', 'J04MSZ000085',
                 'J04XXJ000138GR', 'J04JCY000080B', 'J04MZY000002GR', 'J04RCD000070LGRL', 'J06MMJ000008G',
                 'J04BGY000031BL', 'J04CJ000107', 'J04CTG000123', 'J04MCY000022OR', 'J04MTZ000015', 'HMUS-020012BN-8IN',
                 'HMUS-020014CH-10IN', 'J04YSG000014', 'J04CTG000003W', 'HMUS-020012CH-8IN', 'J021019', 'J04MCY000018B',
                 'J040578-1-S', 'J01LDD000007WNUS', 'J020987-US-BG', 'J04JCY000066', 'J04MSZ000022', 'J04MSZ000040LA',
                 'J040162-BLANDW', 'J040295-WHITE', 'J040295-WHITE', 'J040582-BANDW-A', 'J04YSG000021L', 'J04CJ000051W',
                 'J04MDG000174', 'J04MSZ000055W', 'J04MSZ000088B', 'J020021-43', 'J020053-12-US-HOT_COLD', 'J021088',
                 'J04MCW000021W', 'J04MST000011W', 'J04MTZ000015', 'J040181-WHITE_NATURAL', 'J04YSG000027WL',
                 'J020171-25', 'J020320', 'J020364', 'J020575', 'J04MST000008', 'J04MST000008', '77423284394',
                 'J04CJG000210WL', 'J04JCY000044GR', 'HM-020018-SET', 'J04CJ000638', 'J04SCZ000033W', 'J06MMJ000004',
                 '83773228281', 'J040531-WHITE', 'J020065-4', 'J020182', 'J040528-BLACK', 'J040603-WHITE',
                 'J04MSZ000008L', 'J04MZY000002BL', 'J04SCZ000007M', 'J04CJ000668NA', 'J06ZWJ000098', '39963936518',
                 '39963936518', '41438148209', 'HM-020018-SET', 'J020579', 'J021083-US-BG', 'J040143', 'J04YSG000008S',
                 'J04CJ000124WL', 'J04CJ000831', 'J04MSZ000051181', 'J020053-20', 'J04MSZ000094B', 'J04YSG000032S',
                 'J020001-13', 'J04CJ000241', 'J04XXJ000049GE', 'J04YSG000002BS', 'J04YSG000021S', 'J03JHJ000063G',
                 'J040222-WANDN-LARGE', 'J04MST000005', 'J06MMJ000048G', 'J03JGZ000117', 'J04MST000004', 'J11ZYT000001',
                 'J04SCZ000008S-TABLETOP', 'J04SCZ000023', 'HMUS-020005CH', 'J010933-3-1V-3L', 'J011137-1V-BLACK',
                 'J04RCD000003', 'J040656-WS', 'J040733-W-WSC', 'J04MSZ000033S', 'J11ZYT000020', '21116135362',
                 '83941858387', 'J040652', 'J040652', 'J04MSZ000034WS', 'J04YSG000004BLS', 'J04JCY000012BE',
                 'J04MBT000028', 'J040592-W', 'J040592-W', 'J04CJ000146', 'J04CTG000180', 'HMUS-020003BN',
                 'HMUS-020005GW', 'J020001-66-BG', 'J021108-CH', 'J04CJG000052PK', 'J04CTG000118', 'J040528-BLACK',
                 'J040592-W', 'J040603-WHITE', 'J04SCZ000016S', 'J04CJ000241', 'J04CJG000011', 'J04CJG000209WL',
                 'J04YSG000012GR', '21598144837', '30CM_EXTP-ABR', '83941858387', 'HMUS-020003CH', 'HMUS-020009BG',
                 'J010655-1V', 'J020053-12-US-HOT_COLD', 'J020592', 'J021039-1', 'J070003', 'H8866233-13692084',
                 'J04SCZ000042', 'J04YSG000027BS', 'J04MCW000021W', 'J04MSZ000008L', 'J040260', 'J040410-SMALL',
                 'J04YSG000017M', 'J020788-CHROME', 'J040232-BLUE', 'J040410-SMALL', 'J040410-SMALL', 'J040615-B',
                 'J04YSG000010', 'P11736994', 'P24615865', 'J040162-BLANDW', 'J04MDG000158L', 'J04YSG000004GRS',
                 'J04YSG000013', 'J04YSG000026S', 'J040546-L', 'J040696', 'J010655-1V', 'J021029', 'J04JCY000002DGE',
                 'J04MSZ000055W', 'J020001-59', 'J04MSZ000033S', 'J04MSZ000055W', 'J04MZY000002PK', 'J06ZWJ000353S',
                 'HM-020019-SET', 'J04MZY000002Y', 'J04YSG000008S', 'J04CJ000154A', 'H8866233-13692498', 'J040668-S',
                 'J040181-WHITE_BLACK', 'J040518-GRAY', 'J04MTZ000025', 'J04MTZ000025', 'J070003', 'J04MSZ000036LB',
                 'J04XXJ000049K', 'J04MTZ000025', 'J04MTZ000025', 'J04MTZ000025', 'J040536-BLACK', 'J040733-B-NOSC',
                 'J04CJ000241', 'J04CJ000241', 'J04MTZ000041L', 'J04SCZ000053', 'H8866233-13692498', 'J04MZY000002PK',
                 'J04YSG000021S', 'J04BTY000012W', 'J04JCY000002DGE', 'J040620-SET', 'J04MDG000218L', 'J04MST000005',
                 'HMUS-020012BN-10IN', 'J020069-27-MB', 'J021108-CH', 'J021117-US', 'J070003', '33146587290',
                 'H8866233-13692498', 'J020524-12-US', 'J04CTG000022', 'J04MSZ000008L', 'J04SCZ000051', 'J03JHJ000017B',
                 'J040402-LARGE', 'J040402-LARGE', 'J040525-A', 'J04CJ000602', 'J04CTG000017W', 'J04JCY000022GR',
                 'J09CWS000011W', '35275309622', '35275309622', 'J02TSN000001GR', 'J040671-B', 'J04CJ000046',
                 'J06ZWJ000353S', 'J02TSN000001GR', 'J040232-BLACK', 'J040360-L', 'J040370-WHITE_WALNUT',
                 'J040370-WHITE_WALNUT', 'J020025-68', 'J020053-12-US-HOT_COLD', 'J020720-2-BLACK', 'J020887-US',
                 'J040402-LARGE', 'J040402-LARGE', 'J04CJ000189', 'J04MSZ000008L', 'J04XXJ000049K',
                 'J040222-WANDN-LARGE', 'J04RCD000001GR', 'J09CWS000011BL', 'J09CWS000011W', 'J04SCZ000013S',
                 'J020524-11', 'J020576-US', 'J020770-US-12IN-STSV-WM', 'J02ASF000007USC', 'J06ZWJ000353L',
                 'J11ZYT000020', 'J11ZYT000020', 'J11ZYT000020', 'J040436-4-BLACK', 'J040578-1-L', 'J04CJG000209WL',
                 'J04YSG000025S', 'J011005-1V-WHITE-S', 'J020701-WHITE-UK', 'J020931-CHROME', 'J04MSZ000008L_DIS',
                 'J04MSZ000034WS', 'J04MSZ000040LA', 'J040320-2', 'J040378', 'J04MXJ000065L', 'J04SCZ000013M',
                 'J040285-BLACK', 'J04YSG000027WL', 'J020001-77-US-12IN-WL', 'J040404-BLACK-S', 'J04CJ000347',
                 'J04YSG000026S', 'HMUS-020004CH', 'J010556-1V-BLACK', 'J011188-1V-PINK', 'J020602-ANTIQUE_BLACK-UK',
                 'J03SNJ000035', 'J04CJ000599', 'J04MCW000021W', 'J04MST000040L', 'J04CJ000003DGR', 'J04MSZ000051BS',
                 'J04SCZ000033B', 'J04SCZ000051', 'J04YSG000027WS', 'J040522-2-WHITE', 'J09CWS000011BL', 'J03MWD000112',
                 'J04MSZ000008S_DIS', 'J04MSZ000036MA', 'J040620-SET', 'J04MCW000007', 'J04YSG000021S', 'J04MCW000007',
                 'J04MSZ000008L_DIS', 'J04CJ000046', 'J040156-LARGE', 'J04MSZ000008L_DIS', 'J04MSZ000008L_DIS',
                 'J020053-12-US-HOT_COLD', 'J020524-12-US', 'J020787-7', 'J021117-US', 'J040232-BLACK',
                 'J04BTY000027NA', 'J04CJ000115B', 'J04CJ000230B', '14827443681', 'J04CJ000124WL', 'J04CJ000124WL',
                 '14195358594', '74443094066', '77423284394', '77423284394', 'J040241-B-L', 'J040241-B-M',
                 'J040241-B-S', 'J040241-G-L', 'J040241-LARGE', 'J040241-LARGE', 'J040241-MEDIUM', 'J040241-SMALL',
                 'J040245', 'J040249', 'J040249', 'J040339', 'J040339-DG', 'J040339-DG', 'J040339-DG', 'J040339-DG',
                 'J040339-DG', 'J040339-DG', 'J040339-DG', 'J040339-DG', 'J040339-DG', 'J040339', 'J040339-K',
                 'J040339-K', 'J040339-LG', 'J040339-LG', 'J040339-LG', 'J040339-LG', 'J040339-LG', 'J040339-LG',
                 'J040339-LG', 'J040339', 'J040339', 'J040339', 'J040359', 'J040378', 'J040655', 'J04BSF000014SA',
                 'J04BSF000043B', 'J04BSF000048', 'J04BSF000048', 'J04BSF000087', 'J04CTG000126NA', 'J04SCZ000013S',
                 'J11OXY000004', '28832344730', '51938339163', '81923784044', '24110968924', '41996638688',
                 '82972106189', '87590070775', '87590070775', 'H8866233-13692085', 'HM-020018-SET', 'HM-020018-SET',
                 'HMUS-020002MB', 'J020053-10', 'J021117-US', 'J040181-WHITE_NATURAL', 'J040241-LARGE', 'J040546-L',
                 'J040688-L', 'J04BSF000048', 'J04CJ000108', 'J04CJ000124WL', 'J04CJ000268', 'J04MSZ000040SA',
                 'J04MSZ000055W', 'J04XXJ000017', 'J04XXM000019', 'J06MMJ000049G', 'J11OSF000003', 'J11ZYT000020',
                 '44329049275', 'J040161-WHITE-L', 'J040636-W', 'J04JCY000056GR', '11337089384', '11337089384',
                 '11337089384', '11337089384', 'HMUS-020006MB', 'J020756-GOLD', '11772900811', '28508839235',
                 'J020797-MATTE_WHITE', 'J020828-MATTE_WHITE', 'J021050', 'J040241-G-L', 'J040241-LARGE',
                 'J040241-MEDIUM', 'J040245', 'J040378', 'J040609-1', 'J040615-B', 'J040631', 'J040728-W', 'J040728-W',
                 'J04BGY000031GR', 'J04BSF000183GR', 'J04CJ000047B', 'J04CJ000115W', 'J04CJ000115W', 'J04CJ000123W',
                 'J04CJ000155', 'J04CJ000375', 'J04CJ000441', 'J04CJ000591', 'J04CJ000591', 'J04CJG000060L',
                 'J04CJG000061L', 'J04CTG000001_GR_A', 'J04CTG000022', 'J04CTG000153', 'J04JCY000059PK',
                 'J04MDG000191WL', 'J04MSZ000022', 'J04MSZ000051601', 'J04MSZ000051601', 'J04MSZ000051601',
                 'J04MSZ000088W', 'J04MSZ000120', 'J04MTZ000029', 'J04SCZ000012', 'J04SCZ000012', 'J04SCZ000016L',
                 'J04SCZ000016L', 'J04SCZ000023', 'J04SCZ000033B', 'J04SCZ000033B', 'J04SCZ000033W', 'J04SCZ000033W',
                 'J04SJ000056A', 'J04XXJ000122']

    stock_check(sale_skus, USNJ02_warehouse_id, USNJ02_target_warehouse_id, excel_name)
