from cases import *


def create_spu(**kwargs):
    spu_id = pms_app.add_product(**kwargs).get('data')
    spu_price_detail = pms_app.calculate_product_price(
        spu_id).get('data', {}).get('fixedPricelVoList', [])[0].get('priceVoList')
    price_detail_list = []
    sku_id = None
    for idx, i in enumerate(spu_price_detail):
        tmp = i['priceVoList'][0]
        sku_id = tmp.get('skuId')
        tmp.update({'check': True, "fixedPricelVoListIndex": 0, 'priceVoListIndex': idx})
        price_detail_list.append(tmp)
    pms_app.save_product_price(price_detail_list)
    pms_app.audit_product(sku_id)


if __name__ == '__main__':
    create_spu(productName="wenhao_automatic_insert_product")
