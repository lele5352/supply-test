import barcode
from barcode.writer import ImageWriter
from barcode import generate


def barcode_generate(code_str, dir_name):
    name = generate('code128', code_str, output='../barcodes/{0}/{1}'.format(dir_name, code_str))
    return name


if __name__ == '__main__':
    string = "FH23423424421"
    type = "entry_order"
    barcode_generate(string, type)
