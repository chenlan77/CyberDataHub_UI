import  os,datetime
def init_html_folder(date):
   #创建html测试报告目录
    html_folder_path='./../report/html/'
    folder_path=html_folder_path+date
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
   # 创建png错误截图报告目录
    png_folder_path = './../report/png/'
    folder_path = png_folder_path + date
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
   # 创建log错日志报告目录
    log_folder_path = './../report/log/'
    folder_path = log_folder_path + date
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# if __name__=='__main__':
#     datatime=datetime.date.today()
#     init_html_folder(datatime.strftime('%Y-%m-%d'))