from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
# import numpy as np

class ExcelHandler():
    '''
    操作Excel
    '''

    def __init__(self, file):
        '''初始化函数'''
        self.file = file

    def open_sheet(self, sheet_name) -> Worksheet:
        '''打开表单'''
        wb = load_workbook(self.file)
        sheet = wb[sheet_name]
        return sheet

    def read_header(self, sheet_name):
        '''获取表单的表头'''
        sheet = self.open_sheet(sheet_name)
        headers = []
        for i in sheet[1]:
            headers.append(i.value)
        return headers

    # 读取除表头外所有数据（除第一行外的所有数据）返回的内容是一个二维列表
    def read_rows(self,sheet_name):
        sheet = self.open_sheet(sheet_name)
        rows = list(sheet.rows)[1:]
        data = []
        for row in rows:
            row_data = []
            for cell in row:
               row_data.append(cell.value)
            data.append(row_data)
        return data

    # 读取一个二维列表的每一项
    def read_rows_key(self, matrix):
        cols = self.read_rows(matrix)
        res = list(zip(*cols))
        res_data = []
        for i in res:
            res_data.append(i)
        return res_data


    # 获取所有表格内表头+字段数据
    def read_key_value(self,sheet_name):
        sheet = self.open_sheet(sheet_name)
        rows = list(sheet.rows)

        # 获取标题
        data = []
        for row in rows[1:]:
            rwo_data = []
            for cell in row:
                rwo_data.append(cell.value)
                # 列表转换成字典，与表头里的内容使用zip函数进行打包
            data_dict = dict(zip(self.read_header(sheet_name),rwo_data))
            data.append(data_dict)
        return data
