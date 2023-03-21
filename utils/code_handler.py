# -*- coding: utf-8 -*-
import os
import time
from threading import Thread
import json

from pystrich.code128 import Code128Encoder
import segno

distribute_order_code_path = "../codes/barcodes/distribute_order/{0}.png"
transfer_pick_order_code_path = "../codes/barcodes/transfer/pick_order/{0}.png"
distribute_order_ware_sku_label_path = "../codes/qrcodes/{0}.png"


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


def create_folder(folder):
    abs_folder = os.path.abspath(folder)
    if not os.path.exists(abs_folder):
        try:
            os.makedirs(abs_folder)
        except Exception as e:
            print('Create folder fail:{}'.format(e))


class GenerateCode:
    def __init__(self, code_type, order_type, code_str):
        self.generate_code(code_type, order_type, code_str)

    @async_call
    def generate_code(self, code_type, order_type, code_str):
        if code_type == "barcode":
            if order_type == "distribute_order":
                self.barcode_generate(code_str, distribute_order_code_path.format(code_str))
            elif order_type == "transfer_pick_order":
                self.barcode_generate(code_str, transfer_pick_order_code_path.format(code_str))
            else:
                pass
        elif code_type == "qrcode":
            if order_type == "distribute_order":
                info = json.loads(code_str)
                distribute_order_code = info.get("SOURCE_ORDER_CODE")
                ware_sku_code = info.get("SKU_CODE")
                self.qrcode_generate(code_str, distribute_order_ware_sku_label_path.format(
                    "_".join([distribute_order_code, ware_sku_code])))
            else:
                pass

    @classmethod
    def barcode_generate(cls, info, save_path):
        asb_save_path = os.path.abspath(save_path)
        folder = os.path.dirname(asb_save_path)
        create_folder(folder)
        options = {"bottom_border": 10, "height": 200, "label_border": 2}
        try:
            encoder = Code128Encoder(info, options=options)
            encoder.save(asb_save_path)
            # print('Generate bar code success, save to:{}'.format(asb_save_path))
            print("barcode {}".format(time.time()))
        except Exception as e:
            print('Generate bar code fail:{}'.format(e))

    @classmethod
    def qrcode_generate(cls, info, save_path):
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

    code = "SH1667739890436"
    code_path = "../codes/barcodes/locations/{}.png".format(code)
    GenerateCode.barcode_generate(code, code_path)

    # info = json.dumps({"SKU_CODE": "63203684930J02", "SOURCE_ORDER_CODE": "FH2303211135"})
    # GenerateCode("qrcode", "distribute_order", info)
