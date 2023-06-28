from cases import *
from transfer_data_generator import WmsTransferDataGenerator
from utils.log_handler import logger


def create_export_order(hand_over_no_list=None, cabinet_no_list=None, vesse_booking_no_list=None, **kwargs):
    if not (hand_over_no_list or cabinet_no_list or vesse_booking_no_list):
        print('警告：未传入查询海柜单')
    cabinet_list = cds_app.get_cabinet_order(
        handOverNoList=hand_over_no_list or [],
        cabinetNoList=cabinet_no_list or [],
        vesselBookingNoList=vesse_booking_no_list or [],
        statusList=["1"]  # 选定待确认状态
    ).get('data')['list']
    for cabinet_info in cabinet_list:
        cabinet_id = cabinet_info['id']
        cds_app.confirm_cabinet_order(cabinet_id)
        goods_list_origin = cds_app.cabinet_order_detail(cabinet_id).get('data')['seaCabinetGoodsVOList']
        goods_list = [
            {"drawbackType": info['drawbackType'], "seaCabinetGoodsId": info['id']} for info in goods_list_origin
        ]
        cds_app.edit_cabinet_order(sea_cabinet_order_id=cabinet_id, goods_list=goods_list)
    else:
        print('生成报关单完成')


if __name__ == '__main__':
    transfer_data = WmsTransferDataGenerator()
    # 调拨出库，生成海柜单
    multi_sku_list = ['JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P52601628']
    handover_order_no_list = transfer_data.generate_cds_cabin_order(sku_list=multi_sku_list, step=2)
    # 根据交接单号获取海柜单，并生成报关单
    create_export_order(hand_over_no_list=handover_order_no_list)
