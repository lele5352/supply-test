import concurrent.futures
import random
import time

from cases import *
from transfer_data_generator import WmsTransferDataGenerator
from robot_run.run_transfer import run_transfer, TransferProcessNode


class CdsDataGenerator:
    def create_cabinet_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code_list, bom,
                             demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成海柜单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param any trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param any trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param list sale_sku_code_list: 调拨的商品的销售sku列表
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        :param bom: bom版本
        """

        def bind_sub_pick(sku_code):
            demand_no = WmsTransferDataGenerator().create_transfer_demand(
                trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sku_code, bom, demand_qty, demand_type,
                customer_type, remark
            )
            if not demand_no:
                print("创建调拨拣货单失败")
                return
            # 执行调拨流程到扫货绑定交接单
            result, _order_no = run_transfer(demand_no, TransferProcessNode.bind_box, kw_force=True)
            return _order_no

        # 生成调拨需求
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            to_do = []
            order_no = ''
            for sale_sku_code in sale_sku_code_list:  # 模拟多个任务
                future = executor.submit(bind_sub_pick, sale_sku_code)
                to_do.append(future)
            for future in concurrent.futures.as_completed(to_do):  # 并发执行
                order_no = future.result()
            return order_no

    def submit_cabinet_order(self, order_no, container_no=None, so_number=None):
        """
        提交发货交接单
        :param int order_no: 交接单号
        :param int container_no: 默认自动获取空闲海柜，指定该值将会拼柜（cds海柜单未发柜前有效）
        :param int so_number: 默认自动获取订舱号，与海柜号绑定
        """
        # 获取交接货单id
        order_detail = wms_app.transfer_handover_order(handoverNos=[order_no]).get('data').get('records')[0]
        handover_id = order_detail.get('id')
        # 获取海运柜号信息并更新
        cabinet_info = random.choice(
            [cabinet for cabinet in wms_app.transfer_cabinet_list().get('data') if cabinet.get('cabinetNumber')])
        container_no = cabinet_info.get('cabinetNumber') if container_no is None else container_no
        so_number = cabinet_info.get('soNumber') if so_number is None else so_number
        wms_app.transfer_out_update_delivery_config(handover_id, container_no, so_number)
        wms_app.transfer_out_delivery(order_no)
        print('交接单号:{},交接单id:{},海柜信息:{}:{}'.format(order_no, handover_id, container_no, so_number))
        return container_no, so_number

    def generate_cds_cabin_order(self, sku_list, step=12, container_no=None, so_number=None, trans_out_id=542,
                                 trans_in_id=539):
        """
        生成退税海柜单
        :param list[str] sku_list: 需要发柜的sku
        :param int step: 每个交接单的sku个数，list不可超过15个sku，否则会导致wms发货接口死锁
        :param str container_no: 默认自动获取空闲海柜，指定该值将会拼柜（cds海柜单未发柜前有效）
        :param str so_number: 默认自动获取订舱号，与海柜号绑定
        :param int trans_out_id: 发货仓id
        :param int trans_in_id: 收货仓id
        """
        handover_order_list = []
        for i in range(0, len(sku_list), step if step <= 15 else 15):
            # 自动将大批量sku拆解为15个箱单一组的交接单，并自动进行拼柜处理
            sec_sku_list = sku_list[i:i + step - 1]
            order = self.create_cabinet_order(
                trans_out_id, trans_out_id, trans_in_id, trans_in_id, sec_sku_list, "A", 1)
            handover_order_list.append(order)
            container_no, so_number = self.submit_cabinet_order(order, container_no, so_number)
        else:
            # 单量较小时，可能出现cds后台未同步更新的情况
            time.sleep(5)
        return handover_order_list

    def create_declaration_order(self, hand_over_no_list=None, cabinet_no_list=None, vesse_booking_no_list=None):
        """创建报关单
        :param list[str] hand_over_no_list: 筛选需要生成报关单的交接单号
        :param list[str] cabinet_no_list: 筛选需要生成报关单的海柜号
        :param list[str] vesse_booking_no_list: 筛选需要生成报关单的订舱号
        """
        if not (hand_over_no_list or cabinet_no_list or vesse_booking_no_list):
            print('警告：未传入查询海柜单，默认将所有待发柜的海柜单发柜生单')
        cabinet_list = cds_app.get_cabinet_order(
            handOverNoList=hand_over_no_list or [],
            cabinetNoList=cabinet_no_list or [],
            vesselBookingNoList=vesse_booking_no_list or [],
            statusList=["1"]  # 选定待确认状态
        ).get('data')['list']
        cabinet_id_list = [cabinet_info['id'] for cabinet_info in cabinet_list]
        for cabinet_id in cabinet_id_list:
            cds_app.confirm_cabinet_order(cabinet_id)
            print('{}发柜完成'.format(cabinet_id))
            goods_list_origin = cds_app.cabinet_order_detail(cabinet_id).get('data')['seaCabinetGoodsVOList']
            # 校验退税类型商品sku是否维护申报信息和税收信息，若没有则自动维护
            drawback_sku_dict = {
                info['salesSkuCode']: info['salesSkuName'] for info in goods_list_origin if info['drawbackType'] == 1
            }
            drawback_sku_list = list(drawback_sku_dict.keys())
            goods_declaration_sku_list = [_['salesSkuCode'] for _ in
                                          cds_app.get_goods(salesSkuCodeList=drawback_sku_list).get('data')['list']]
            taxation_sku_list = [_['salesSkuCode'] for _ in
                                 cds_app.get_taxation(salesSkuCodes=drawback_sku_list).get('data')['list']]
            if len(drawback_sku_list) > len(goods_declaration_sku_list):
                for sku_id, sku_name in drawback_sku_dict.items():
                    if sku_id not in goods_declaration_sku_list:
                        cds_app.add_good(salesSkuCode=sku_id, salesSkuName=sku_name)
                        print('新增商品申报信息:{}'.format(sku_id))
            if len(drawback_sku_list) > len(taxation_sku_list):
                for sku_id, sku_name in drawback_sku_dict.items():
                    if sku_id not in taxation_sku_list:
                        cds_app.add_taxation(salesSkuCode=sku_id, salesSkuName=sku_name)
                        print('新增商品税收信息:{}'.format(sku_id))
            # 获取所有明细并生成报关单
            goods_list = [
                {"drawbackType": info['drawbackType'], "seaCabinetGoodsId": info['id']} for info in goods_list_origin
            ]
            cds_app.edit_cabinet_order(sea_cabinet_order_id=cabinet_id, goods_list=goods_list)
            print('{}生单成功'.format(cabinet_id))
        else:
            declaration_list = cds_app.get_declaration(
                containerNos=cabinet_no_list or [],
                vesselBookingNos=vesse_booking_no_list or [],
                declarationStatusList=["0"],
                createUserId=cds_app.get_user_info().get('userId')
            ).get('data')['list']
            result = [info['systemDeclarationOrderNo'] for info in declaration_list if
                      info['seaCabinetId'] in cabinet_id_list]
            print('生成报关单完成: {}'.format(result))


if __name__ == '__main__':
    transfer_data = CdsDataGenerator()
    # 调拨出库，生成海柜单
    multi_sku_list = [
        'JF067T801S', 'JF31665XD8', 'JF2KB93311'
        # 'JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P52601628', 'JF954856UJ', 'JF389G7H75', 'JF68Z9301V',
        # 'JF067T801S', 'JF31665XD8', 'JF40130HR7', 'JFW95751S0', 'HWIT187548', 'HW9W44M768', 'HW332S63I7', 'HW1711P3M7',
        # 'HW203YE645', 'JFH4V76784', 'JFP171H106', 'JF8I4R7270', 'JFW5G63036', 'JF434R46Q4', 'JJ5E8055G4', 'JJS5B07625',
        # 'ZSF30624L5', 'JJ528061NA', 'JJU389856V', 'PAN38335IL2', 'PAN09X7N757', 'PAN72H343A7', 'PAN004183AF',
        # 'PAN96737UO5', 'PAN03HU1744', 'PAN3N38E090', 'PANY00695I5', 'PAN64T4883J', 'HWG2X83063', 'HW05N7T199',
        # 'HWD833074R', 'JF570DY209', 'JF973Q4C44', 'JF57650TN8', 'JF02FX6668', 'JJ85990HZ4', 'JJ22155EF1', 'DJA9828C16',
        # 'DJY9895U92', 'DJP352954J', 'DJUT880040', 'JF5891A6J4', 'JJ22V28I66', 'JFQ17267D2', 'JF5F11Z633', 'JF128Z202I',
        # 'JF71Y908Q2', 'JFP07D6867', 'JF48Z2691G', 'PRE1000001', 'JJPY283153', 'JFGU822634', 'JF2KB93311', 'PRE_TEST4',
        # 'PRE_TEST3', 'PRE_TEST2', 'PRE_TEST1', 'HANGE_PRE7', 'HANGE_PRE6', 'HANGE_PRE5', 'HANGE_PRE4', 'PRE_THREE',
        # 'PRE_TWO', 'PRE_ONE', 'SKU_ATTR_DEFAULT', 'HANGE_PRE_NEW', 'HANGE_PRE', 'DJ690WS210', 'JFN124045S',
        # 'JFZ06986D3', 'HWU72U2280', 'JF710294KC', 'JF002Z8F55', 'JF902K38B1', 'JFR06Y0103', 'JJ8L7B1005', 'JJ454072GE',
        # 'JJ52L6C245', 'JF06728I8T', 'JF5D41G211', 'JJ2PI66951', 'JFL2847K46', 'JF9496MS19', 'JF86PM7085', 'JF2181O7E9',
        # 'JF20O7A332', 'HW691E9F15', 'JF698LM501', 'JJH22251X0', 'JJ253R4X93', 'JJ77QH3613', 'JJJ3E57318', 'JJ8SM72435',
        # 'JJ9R0Q1900', 'JF5555U5A3', 'JFMD427628', 'JF4P1582W3', 'JJ95900O1F', 'JF36567JT9', 'JFW28445H5', 'JF6300R13H',
        # 'JF27P1419G', 'JF8T3M4789', 'GGG517', 'TESTNEW517', 'TEST517', 'JF091H128H', 'JF73231T5W', 'JF31564K2R',
        # 'JF408PD244', 'JF0W26C942', 'JF1C2Q4008', 'HW372W2N04', 'JF07701PJ7', 'JF830537IK', 'JF681I4F73', 'WY8219Q39W',
        # 'WY540T946Q', 'WY411H82M6', 'WY21M267E8', 'HW13835ZH0', 'HW3I128N68', 'HWZ6852N41', 'HW7222G4F0', 'JF32H16W70',
        # 'JF2Q7538E0', 'JFF582Y514', 'JFL96792J1', 'JJW56O3441', 'JJ06Z0S128', 'JJ700B9Y45', 'JJ8322D5K2', 'JF94I4230E',
        # 'JJ4368K46M', 'JJG1203V17', 'JF88X641Q4', 'JF81F69G03', 'JJ0895GR64', 'JF7R6497Z8', 'JF2224L1G4', 'JF0561XP63',
        # 'JF8P629R88', 'JF4F17929R', 'JFN65Y6867', 'JFY30S9478', 'JF6620J22G', 'JJG802I913', 'JJZ064416Q', 'JJ0G1431T0'
    ]
    handover_order_no_list = transfer_data.generate_cds_cabin_order(sku_list=multi_sku_list, step=8)
    # 根据交接单号获取海柜单，并生成报关单
    transfer_data.create_declaration_order(hand_over_no_list=handover_order_no_list)
