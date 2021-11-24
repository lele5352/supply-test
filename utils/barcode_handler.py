from barcode.writer import ImageWriter
from barcode import generate


def barcode_generate(code_str, barcode_type):
    generate('code128', code_str, writer=ImageWriter(), output='../barcodes/%s/%s' % (barcode_type, code_str))


if __name__ == '__main__':
    # barcode_generate('PRE-BG2111150001', 'express')
    barcode_generate('CKYCKW-001', 'locations')
    # barcode_generate('SHKW001', 'locations')
    # barcode_generate('sjkw-003', 'locations')

