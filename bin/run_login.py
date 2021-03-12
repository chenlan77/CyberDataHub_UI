import unittest,HTMLTestRunner,datetime
from untils.init_folder import init_html_folder
from case_manage.test_login  import Test_Login
from case_manage.test_login.test_login  import Test_Login
suite=unittest.defaultTestLoader.discover('./../case_manage/',pattern='test_login.py')

if __name__=='__main__':

    date_time=datetime.datetime.now()
    date=date_time.strftime('%Y-%m-%d')
    report_time=date_time.strftime('%H%M%S')
    init_html_folder(date)
    filename='./../report/html/'+date+'/'+report_time+'report.html'
    runner=HTMLTestRunner.HTMLTestRunner(open(filename,'wb'),title='测试报告',description='现在还在调试阶段')
    runner.run(suite)


    # suite=unittest.TestSuite()
    # suite.addTest(Test_Login('test_longin2'))
    # suite.addTest(Test_Login('test_login1'))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)