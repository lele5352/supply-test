import random
import time
import concurrent.futures

from cases import *

from utils.log_handler import logger as log
from utils.code_handler import GenerateCode
from utils.wait_handler import until

from data_generator.receipt_data_generator import WmsReceiptDataGenerator
from robot_run.run_transfer import run_transfer


class WmsTransferDataGenerator:
    def __init__(self):
        self.wms_app = wms_app
        self.wms_transfer = wms_transfer
        self.ims = ims_robot
        self.wms_data = WmsReceiptDataGenerator()

    def create_transfer_demand(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
                               trans_qty, demand_type=1, customer_type=1, remark=''):
        """
        创建调拨需求

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param int trans_out_to_id: 调出仓库的目的仓id
        :param int trans_in_to_id: 调入仓库的目的仓id
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int trans_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        :param bom: bom版本
        """
        self.wms_app.common_switch_warehouse(trans_out_id)

        # 判断bom版本库存是否足够
        is_stock_enough = self.ims.is_bom_stock_enough(sale_sku_code, bom, trans_qty, trans_out_id, trans_out_to_id)

        if not is_stock_enough:
            add_stock_res = self.wms_data.create_other_in_order_and_up_shelf(
                sale_sku_code, bom, trans_qty, trans_out_id, trans_out_to_id
            )
            if not add_stock_res or add_stock_res.get("code") != 1:
                log.error('创建调拨需求失败：加库存失败！')
                return

        # 用户检查库存是否加成功了，加库存需要时间
        until(120, 0.1)(
            lambda: trans_qty <= self.ims.dbo.query_central_inventory(
                sale_sku_code, trans_out_id, trans_out_to_id).get("remain", 0)
        )()

        # 仓库id转换为code
        trans_out_code = self.wms_app.db_ck_id_to_code(trans_out_id)
        trans_out_to_code = self.wms_app.db_ck_id_to_code(trans_out_to_id)
        trans_in_code = self.wms_app.db_ck_id_to_code(trans_in_id)
        trans_in_to_code = self.wms_app.db_ck_id_to_code(trans_in_to_id)
        # 调用创建调拨需求接口
        create_demand_res = self.wms_transfer.transfer_out_create_demand(
            trans_out_code, trans_out_to_code, trans_in_code, trans_in_to_code, sale_sku_code, bom, trans_qty,
            demand_type, customer_type, remark)
        if not create_demand_res or create_demand_res['code'] != 1:
            log.error('创建调拨需求失败！')
            return
        print('生成调拨需求：%s' % create_demand_res['data']['demandCode'])
        return create_demand_res['data']['demandCode']

    def create_transfer_pick_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
                                   demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成调拨拣货单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param int trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param int trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        :param bom: bom版本
        """
        self.wms_app.common_switch_warehouse(trans_out_id)
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom, demand_qty, demand_type,
            customer_type, remark
        )
        if not demand_no:
            print('创建调拨拣货单失败：需求创建失败！')
            return
        # 创建调拨拣货单
        result, order_no = run_transfer(demand_no, "create_pick_order")
        if not result:
            print('创建调拨拣货单失败！')
            log.error('创建调拨拣货单失败！')
            return
        pick_order_code = order_no

        GenerateCode("barcode", "transfer_pick_order", pick_order_code)
        print('生成调拨拣货单：%s' % pick_order_code)
        return pick_order_code

    def create_handover_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
                              demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成调拨出库单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param any trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param any trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        :param bom: bom版本
        """
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom, demand_qty, demand_type,
            customer_type, remark
        )
        if not demand_no:
            print('创建调拨拣货单失败')
            return
        # 执行调拨流程到发货交接节点
        result, order_no = run_transfer(demand_no, "handover")
        print("创建调拨出库成功,调拨交接单号：%s" % order_no)
        return order_no

    def create_cabinet_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code_list, bom,
                             demand_qty, demand_type=1, customer_type=1, remark='', process_flag='bind'):
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
        :param process_flag: 流程标志位： bind，submit
        """

        def bind_sub_pick(sku_code):
            demand_no = self.create_transfer_demand(
                trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sku_code, bom, demand_qty, demand_type,
                customer_type, remark
            )
            if not demand_no:
                print("创建调拨拣货单失败")
                return
            # 执行调拨流程到扫货绑定交接单
            result, _order_no = run_transfer(demand_no, "bind", kw_force=True)
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
        # 获取交接货单id
        order_detail = self.wms_app.transfer_handover_order(handover_ids=[order_no]).get('data').get('records')[0]
        handover_id = order_detail.get('id')
        # 获取海运柜号信息并更新
        cabinet_info = random.choice(
            [cabinet for cabinet in self.wms_app.transfer_cabinet_list().get('data') if cabinet.get('cabinetNumber')])
        container_no = cabinet_info.get('cabinetNumber') if container_no is None else container_no
        so_number = cabinet_info.get('soNumber') if so_number is None else so_number
        self.wms_app.transfer_out_update_delivery_config(handover_id, container_no, so_number)
        self.wms_app.transfer_out_delivery(order_no)
        print('交接单号:{},交接单id:{},海柜信息:{}:{}'.format(order_no, handover_id, container_no, so_number))
        return container_no, so_number


if __name__ == '__main__':
    transfer_data = WmsTransferDataGenerator()
    # sku_list = ['JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P31559628', 'BPJF067T801SB01']
    """
    收货仓：
    广州1号（warehouseId: 594, warehouseCode: "GZFH01"），退税类型=不限
    新泽西1号仓（warehouseId: 543, warehouseCode: "USNJ01"），退税类型=非退税
    英国1号仓（warehouseId: 539, warehouseCode: "UKBH01"），退税类型=退税

    发货仓：
    洛杉矶1号仓，warehouseId: 542, warehouseCode: "USLA01"

    非退税商品：
    销售SKU：
    JF067T801S,供应商：coco测试
    JF31665XD8,供应商：coco测试

    零部件商品：
    P52601628 关联的SKU：JF067T801S 供应商：coco测试

    退税商品：
    销售SKU：
    JF954856UJ,供应商：coco雪1
    JF389G7H75,供应商：coco雪1

    零部件商品：
    P31559628   关联的SKU：JF954856UJ 供应商：coco雪1

    内部BOM，供应商为空：
    BPJF067T801SB01
    """
    # sku_list = [['JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P31559628', 'P52601628']]
    # sku_list = [['JF954856UJ', 'JF389G7H75', 'JF68Z9301V']]
    # sku_list = [['JF68Z9301V']]
    sku_list = [['BP77593016151B01']]
    sku_list = [
     ['BP77593016151B01','JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P31559628', 'P52601628','JF954856UJ', 'JF389G7H75', 'JF68Z9301V'],
     ['JF067T801S', 'JF31665XD8', 'JF40130HR7', 'JFW95751S0', 'HWIT187548', 'HW9W44M768', 'HW332S63I7', 'HW1711P3M7',],
     ['HW203YE645', 'JFH4V76784', 'JFP171H106', 'JF8I4R7270', 'JFW5G63036', 'JF434R46Q4', 'JJ5E8055G4', 'JJS5B07625',],
     ['ZSF30624L5', 'JJ528061NA', 'JJU389856V', 'PAN38335IL2', 'PAN09X7N757', 'PAN72H343A7', 'PAN004183AF',],
     ['PAN96737UO5', 'PAN03HU1744', 'PAN3N38E090', 'PANY00695I5', 'PAN64T4883J', 'HWG2X83063', 'HW05N7T199',],
     ['HWD833074R', 'JF570DY209', 'JF973Q4C44', 'JF57650TN8', 'JF02FX6668', 'JJ85990HZ4', 'JJ22155EF1', 'DJA9828C16',],
     ['DJY9895U92', 'DJP352954J', 'DJUT880040', 'JF5891A6J4', 'JJ22V28I66', 'JFQ17267D2', 'JF5F11Z633', 'JF128Z202I',],
     ['JF71Y908Q2', 'JFP07D6867', 'JF48Z2691G', 'PRE1000001', 'JJPY283153', 'JFGU822634', 'JF2KB93311', 'PRE_TEST4',],
     ['PRE_TEST3', 'PRE_TEST2', 'PRE_TEST1', 'HANGE_PRE7', 'HANGE_PRE6', 'HANGE_PRE5', 'HANGE_PRE4', 'PRE_THREE',],
     ['PRE_TWO', 'PRE_ONE', 'SKU_ATTR_DEFAULT', 'HANGE_PRE_NEW', 'HANGE_PRE', 'DJ690WS210', 'JFN124045S', 'JFZ06986D3',],
     ['HWU72U2280', 'JF710294KC', 'JF002Z8F55', 'JF902K38B1', 'JFR06Y0103', 'JJ8L7B1005', 'JJ454072GE', 'JJ52L6C245',],
     ['JF06728I8T', 'JF5D41G211', 'JJ2PI66951', 'JFL2847K46', 'JF9496MS19', 'JF86PM7085', 'JF2181O7E9', 'JF20O7A332',],
     ['HW691E9F15', 'JF698LM501', 'JJH22251X0', 'JJ253R4X93', 'JJ77QH3613', 'JJJ3E57318', 'JJ8SM72435', 'JJ9R0Q1900',],
     ['JF5555U5A3', 'JFMD427628', 'JF4P1582W3', 'JJ95900O1F', 'JF36567JT9', 'JFW28445H5', 'JF6300R13H', 'JF27P1419G',],
     ['JF8T3M4789', 'JJJ517', 'GGG517', 'TESTNEW517', 'TEST517', 'JF091H128H', 'JF73231T5W', 'JF31564K2R', 'JF408PD244',],
     ['JF0W26C942', 'JF1C2Q4008', 'HW372W2N04', 'JF07701PJ7', 'JF830537IK', 'JF681I4F73', 'WY8219Q39W', 'WY540T946Q',],
     ['WY411H82M6', 'WY21M267E8', 'HW13835ZH0', 'HW3I128N68', 'HWZ6852N41', 'HW7222G4F0', 'JF32H16W70', 'JF2Q7538E0',],
     ['JFF582Y514', 'JFL96792J1', 'JJW56O3441', 'JJ06Z0S128', 'JJ700B9Y45', 'JJ8322D5K2', 'JF94I4230E', 'JJ4368K46M',],
     ['JJG1203V17', 'JF88X641Q4', 'JF81F69G03', 'JJ0895GR64', 'JF7R6497Z8', 'JF2224L1G4', 'JF0561XP63', 'JF8P629R88',],
     ['JF4F17929R', 'JFN65Y6867', 'JFY30S9478', 'JF6620J22G', 'JJG802I913', 'JJZ064416Q', 'JJ0G1431T0']
    ]
    # c_no, s_no = 'panbao120', 'panbao120'
    c_no, s_no = None, None
    for i in sku_list:
        order = transfer_data.create_cabinet_order(542, 542, 539, 539, i, "A", 1)  # 扫描当前sku并绑定到发货单，退税
        time.sleep(5)
        if c_no and s_no:
            transfer_data.submit_cabinet_order(order, c_no, s_no)
        else:
            c_no, s_no = transfer_data.submit_cabinet_order(order)
        # transfer_data.submit_cabinet_order(order)