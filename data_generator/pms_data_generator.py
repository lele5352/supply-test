import time

from cases import *
from receipt_data_generator import WmsReceiptDataGenerator


def create_spu(package_num=1, single_package_num=1, up_shelf=True, **kwargs):
    """
    创建商品，默认单品单间商品
    :param int package_num: 单个sku的包裹数（对应品数）
    :param int single_package_num: 单个包裹的包装数量（对应件数）
    :param bool up_shelf: 创建后审核上架
    :param kwargs: 创建参数，不传则默认
    :return: 返回销售sku编码
    """
    spu_id = pms_app.add_product(package_num=package_num, single_package_num=single_package_num, **kwargs).get('data')
    print('新增商品，商品进入新建状态')
    resp = pms_app.calculate_product_price(spu_id).get('data', {}).get('fixedPricelVoList', [])[0]
    spu_price_detail = resp.get('priceVoList')
    sku_code = resp.get('sku')
    sku_id = None
    price_detail_list = []
    for idx, i in enumerate(spu_price_detail):
        tmp = i['priceVoList'][0]
        sku_id = tmp.get('skuId')
        tmp.update({'check': True, "fixedPricelVoListIndex": 0, 'priceVoListIndex': idx})
        price_detail_list.append(tmp)
    pms_app.save_product_price(price_detail_list)
    print('提交商品审核，商品进入待审核状态')
    pms_app.audit_product(sku_id)
    print('审核商品通过，商品进入待售状态')
    if up_shelf:
        pms_app.approve_sku_attribution(sku_id)
        print('审核sku属性通过，商品进入在售状态，sku编码：{}'.format(sku_code))
    # 创建完商品后，scm需要延迟一段时间后才可以拉取到
    time.sleep(5)
    return sku_code


def create_product_bom(sale_sku_code):
    # 获取供应商商品sku信息
    sale_sku_id_list = scm_app.get_supplier_product(sale_sku_code).get('data', {})['list']
    used_supplier_list = [_['supplierInfo']['supplierName'] for _ in sale_sku_id_list]
    # 组装新增bom的参数
    supplier_list = scm_app.get_supplier().get('data', {})['list']
    for supplier_info in supplier_list:
        # 获取未使用的供应商创建新bom
        if supplier_info['supplierName'] not in used_supplier_list:
            sku_id = sale_sku_id_list[-1]['id']
            product_detail = scm_app.get_supplier_product_detail(sku_id).get('data', {})
            product_detail.pop('id')
            product_detail.pop('supplierProductStatus')
            product_detail['purchaseMethod'] = 0
            product_detail['supplierId'] = supplier_info['id']
            product_detail['supplierName'] = supplier_info['supplierName']
            product_detail['purchasePrices'][0]['id'] = -1
            product_detail['purchasePrices'][0]['disabled'] = True
            scm_app.add_supplier_product(**product_detail)
            product_list = scm_app.get_supplier_product(sale_sku_code, status=0).get('data', {})['list']
            audit_sku_list = [_['id'] for _ in product_list]
            scm_app.audit_supplier_product(audit_sku_list)
            print('审核当前sku下所有待审核的bom及部件:{}'.format(audit_sku_list))
            return
    else:
        print('已创建超过50个供应商的bom，创建bom失败')


if __name__ == '__main__':
    sale_sku_code = create_spu(productName="测试单品单件", package_num=1, single_package_num=1)
    # sale_sku_code = create_spu(productName="测试单品多件", package_num=1, single_package_num=3)
    # sale_sku_code = create_spu(productName="测试多品多件", package_num=3, single_package_num=3)
    # create_product_bom(sale_sku_code)
    # 补充库存
    # sale_sku_code = 'KK931075TA'
    # recp_data = WmsReceiptDataGenerator()
    # recp_data.create_other_in_order_and_up_shelf(
    #     sale_sku_code=sale_sku_code, bom="A", qty=10, warehouse_id=542, to_warehouse_id=542)
