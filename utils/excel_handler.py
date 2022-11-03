import openpyxl
import json


def get_excel_data(file, sheet_name=''):
    file = openpyxl.load_workbook(file)
    a = file.active
    if sheet_name:
        a = file[sheet_name]
    d = []
    for x in range(2, a.max_row + 1):
        c = []
        for y in range(1, a.max_column + 1):
            if y == 1:
                c.append(json.loads(a.cell(row=x, column=y).value))
            else:
                c.append(a.cell(row=x, column=y).value)
        tup = tuple(c)
        d.append(tup)
    return d
