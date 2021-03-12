import  unittest,HTMLTestRunner,datetime
from untils.init_folder import init_html_folder
from untils.upload_file import set_uploader
suite=unittest.defaultTestLoader.discover('./../case_manage/',pattern='test_*.py')



if __name__=='__main__':

    date_time=datetime.datetime.now()
    date=date_time.strftime('%Y-%m-%d')
    report_time=date_time.strftime('%H%M%S')
    init_html_folder(date)
    filename='./../report/html/'+date+'/'+report_time+'report.html'
    runner=HTMLTestRunner.HTMLTestRunner(open(filename,'wb'),title='测试报告',description='现在还在调试阶段')
    runner.run(suite)

    # unittest.TestSuite()
    # suite.addTest(AppManageMent('test_app'))
    # runner=unittest.TextTestRunner()
    # runner.run()