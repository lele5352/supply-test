# -*- coding: utf-8 -*-
import os

from pystrich.code128 import Code128Encoder
import segno
import json

def create_folder(folder):
    abs_folder = os.path.abspath(folder)
    if not os.path.exists(abs_folder):
        try:
            os.makedirs(abs_folder)
        except Exception as e:
            print('Create folder fail:{}'.format(e))


def barcode_generate(info, save_path):
    asb_save_path = os.path.abspath(save_path)
    folder = os.path.dirname(asb_save_path)
    create_folder(folder)
    options = {"bottom_border": 10, "height": 200, "label_border": 2}
    try:
        encoder = Code128Encoder(info, options=options)
        encoder.save(asb_save_path)
        # print('Generate bar code success, save to:{}'.format(asb_save_path))
    except Exception as e:
        print('Generate bar code fail:{}'.format(e))


def qrcode_generate(info, save_path):
    asb_save_path = os.path.abspath(save_path)
    folder = os.path.dirname(asb_save_path)
    create_folder(folder)
    try:
        sku_label_info = segno.make(info)
        sku_label_info.save(asb_save_path)
    except Exception as e:
        print('Generate qrcode fail:{}'.format(e))


if __name__ == '__main__':
    # code = "63203684930J01"
    # code_path = "../barcodes/sku/{}.png".format(code)
    # generate(code, code_path)

    # code = "SH1667739890436"
    # code_path = "../barcodes/locations/{}.png".format(code)
    # barcode_generate(code, code_path)

    info = {"SKU_CODE": "63203684930J02", "SOURCE_ORDER_CODE": "FH2303211135"}
    code_path = "../qrcodes/{}.png".format("_".join([info["SOURCE_ORDER_CODE"], info["SKU_CODE"]]))
    qrcode_generate(json.dumps(info), code_path)
