from barcode.writer import ImageWriter
from barcode import generate


def barcode_generate(code_str, barcode_type):
    generate('code128', code_str, writer=ImageWriter(), output='../barcodes/%s/%s' % (barcode_type, code_str))

