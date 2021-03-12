from openpyxl import load_workbook
import  os,datetime
class ParseExcel():
    def __init__(self,excel_path,sheetname):
        self.wb=load_workbook(excel_path)
        self.sheet=self.wb[sheetname]
    def getDataFromSheet(self):
        datalist=[]
        for line in self.sheet:
            # datalist.append(line[1].value)
            datacell = []
            for i in line:
                datacell.append(i)
            # datacell.pop(0
            datalist.append(datacell)
        datalist.pop(0)
        return datalist
# if __name__=='__main__':
#     excelPath = './../data_manage/csv_file/login_user.xlsx'
#     sheetName = 'Sheet1'
#     excel = ParseExcel(excelPath, sheetName)
#     print(excel.getDataFromSheet())