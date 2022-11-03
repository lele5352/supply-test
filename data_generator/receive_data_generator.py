from robots.wms_robot import WMSAppRobot


class ReceiveDataGenerator:
    def __init__(self):
        self.wms_app_robot = WMSAppRobot()

    def receive(self, distribute_order_code, warehouse_id, to_warehouse_id):
        # 切换到收货仓
        switch_result = self.wms_app_robot.switch_default_warehouse(warehouse_id)
        if not switch_result['code']:
            return
        # 调用入库单列表页接口根据分货单号获取入库单信息
        search_result = self.wms_app_robot.entry_order_page([distribute_order_code])
        if not search_result['code']:
            return

        # 提取入库单信息
        entry_order_info = search_result['data']['records'][0]

        entry_order_code = entry_order_info.get('entryOrderCode')
        scan_result = self.wms_app_robot.entry_order_detail(entry_order_code)
        if not scan_result['code']:
            return
        entry_order_detail = scan_result.get('data')
        pre_receive_order_code = entry_order_detail.get('predictReceiptOrderCode')
        receive_sku_list = entry_order_detail.get("skuInfos")

        get_sh_kw_result = self.wms_app_robot.get_kw(2, 1, len(receive_sku_list), warehouse_id, to_warehouse_id)
        if not get_sh_kw_result['code']:
            return
        sh_kw_codes = get_sh_kw_result['data']

        get_sj_kw_result = self.wms_app_robot.get_kw(2, 5, len(receive_sku_list), warehouse_id, to_warehouse_id)
        if not get_sj_kw_result['code']:
            return
        sj_kw_codes = get_sj_kw_result['data']

        for sku, kw in zip(receive_sku_list, sh_kw_codes):
            sku.update({
                "locationCode": kw,
                "skuNumber": sku['totalNumber']
            })
        receive_result = self.wms_app_robot.confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
        if not receive_result['code']:
            return

        pre_receive_order_list = [pre_receive_order_code]

        submit_pre_receive_order_result = self.wms_app_robot.submit_pre_receive_order(pre_receive_order_list)
        if not submit_pre_receive_order_result['code']:
            return

        # 跳过质检，直接上架交接
        handover_result = self.wms_app_robot.handover_to_upshelf(sh_kw_codes)
        if not handover_result['code']:
            return

        # 整托上架
        for sh_kw_code, sj_kw_code in zip(sh_kw_codes, sj_kw_codes):
            kw_detail_result = self.wms_app_robot.location_detail(sh_kw_code)
            if not kw_detail_result['code']:
                return
            upshelf_result = self.wms_app_robot.upshelf_whole_location(sh_kw_code, sj_kw_code)
            if not upshelf_result['code']:
                return
        # 最后需要再调用上架完成接口，结束流程
        complete_upshelf_result = self.wms_app_robot.complete_upshelf()
        if not complete_upshelf_result['code']:
            return
        return True


if __name__ == '__main__':
    re = ReceiveDataGenerator()
    print(re.receive('FH2211033562', 566, 568))
