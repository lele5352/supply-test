import openpyxl


class ExcelTool:
    def __init__(self, filename):
        self.filename = filename
        self.workbook = openpyxl.load_workbook(self.filename)

    def read_data(self, sheet_name=None, start_row=1):
        if sheet_name is None:
            sheet_name = self.workbook.sheetnames[0]
        sheet = self.workbook[sheet_name]

        data = []
        for row in sheet.iter_rows(min_row=start_row, values_only=True):
            data.append(row)
        return data

    def write_data(self, data, sheet_name=None, start_row=None):
        if sheet_name is None:
            sheet_name = 'Sheet1'

        if sheet_name not in self.workbook.sheetnames:
            self.workbook.create_sheet(sheet_name)
        sheet = self.workbook[sheet_name]

        if start_row is None:
            start_row = sheet.max_row + 1

        for row_data in data:
            sheet.append(row_data)

        self.workbook.save(self.filename)


if __name__ == '__main__':
    # data = ExcelTool("../test_data/transfer_test_data.xlsx")
    fhc_cp_other_in_data = ExcelTool("../test_data/ims_test_data.xlsx").read_data("fhc_cp_other_in",2)

    print(fhc_cp_other_in_data)
