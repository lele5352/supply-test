from pdf2docx import Converter


def pdf_convert(pdf_file, docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()


if __name__ == '__main__':
    pdf_file = '/Users/essenxu/Desktop/线上故障处理规范V1.0.pdf'
    docx_file = '/Users/essenxu/Desktop/线上故障处理规范V1.0.docx'
    pdf_convert(pdf_file, docx_file)
