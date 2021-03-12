import unittest,time,datetime
from  ddt import ddt,data
from selenium import webdriver
from untils.excel_read import ParseExcel
from untils.log import Log
excelpath='./../data_manage/csv_file/login_user.xlsx'
sheetname='Sheet1'
excel=ParseExcel(excelpath,sheetname)
date_time = datetime.datetime.now()
date = date_time.strftime('%Y-%m-%d')
logpath='./../report/log/'+date+'/'+date+'.log'
@ddt
class Test_Login(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # 类加载初始加载的前置初始化
        # self.driver=webdriver.Chrome()
        # self.driver.get('http://192.168.199.235:38092/oauth/authorize?client_id=mJrcghz5g6&response_type=code&redirect_uri=http%3A%2F%2F192.168.199.143%3A17080%2Fgateway')
           pass
    @classmethod
    def tearDownClass(self):
        # 类运行完毕后的后置处理
        # self.driver.quit()
        pass
    def setUp(self):
        """每条用例执行前的初始化"""
        self.driver = webdriver.Chrome()
        self.driver.get('http://192.168.199.235:38092/oauth/authorize?client_id=mJrcghz5g6&response_type=code&redirect_uri=http%3A%2F%2F192.168.199.143%3A17080%2Fgateway')
        self.data_time=datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        self.pngpath='./../report/png/' + date + '/' +self.data_time
        self.log=Log(logpath)
        time.sleep(1)
    def tearDown(self):
         """每条用例执行后关闭浏览器"""
         self.driver.quit()
         # pass
    # 用例部分
    @data(*excel.getDataFromSheet())
    def test_login(self,data):
        """测试用户登录"""
        self.driver.maximize_window()
        # 登录用户名与密码，及点击登录
        try:
            """用户名为空密码为空、用户名为空密码不为空、用户名不为空密码为空的情况及其他情况填充文本框"""
            if data[0].value is None and data[2].value is None:
                self.driver.find_element_by_id('username').send_keys('')
                self.driver.find_element_by_id('password').send_keys('')
            elif data[2].value is None:
                self.driver.find_element_by_id('username').send_keys(data[0].value)
                self.driver.find_element_by_id('password').send_keys('')
            elif data[0].value is None:
                self.driver.find_element_by_id('username').send_keys('')
                self.driver.find_element_by_id('password').send_keys(data[2].value)
            else:
                self.driver.find_element_by_id('username').send_keys(data[0].value)
                self.driver.find_element_by_id('password').send_keys(data[2].value)
            #点击登录按钮
            self.driver.find_element_by_xpath('//*[@id="subform"]/button').click()
            time.sleep(2)
            print("用户名：%s,姓名：%s,密码：%s,备注：%s" % (data[0].value, data[1].value, data[2].value, data[3].value))
            #多种情况的登录验证：错误密码、错误账号、用户名为空密码为空，用户名及密码错误等
            if (data[3].value=='错误密码' or data[3].value=='错误账号'):
                   # self.assertEqual('您输入的用户名密码错误', 1)
                  self.assertEqual('您输入的用户名密码错误',self.driver.find_element_by_css_selector('div.error-msg').text)
            elif (data[0].value is None or data[2].value is None):
                # self.assertEqual('您输入的用户名或密码不能为空', 2)
                self.assertEqual('您输入的用户名或密码不能为空', self.driver.find_element_by_css_selector('div.error-msg').text)
            else:
                # print(self.driver.find_element_by_xpath('//*[@id="cyber-datahub"]/main/header/div[2]/a/span').text)
                #  self.assertEqual(data[1].value,'优秀')
                self.assertEqual(data[1].value,self.driver.find_element_by_xpath('//*[@id="cyber-datahub"]/main/header/div[2]/a/span').text)
        except AssertionError as e:
            self.log.add_log(str(data[0].value), str(data[2].value), format(e))
            self.pngpath =self.pngpath+'test_login'+'.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            #错误验证内容
            if (data[3].value == '错误密码' or data[3].value == '错误账号'):
                # self.assertEqual('您输入的用户名密码错误', 1)
                self.assertEqual('您输入的用户名密码错误', self.driver.find_element_by_css_selector('div.error-msg').text)
            elif (data[0].value is None or data[2].value is None):
                # self.assertEqual('您输入的用户名或密码不能为空', 2)
                self.assertEqual('您输入的用户名或密码不能为空', self.driver.find_element_by_css_selector('div.error-msg').text)
            else:
                # print(self.driver.find_element_by_xpath('//*[@id="cyber-datahub"]/main/header/div[2]/a/span').text)
                #  self.assertEqual(data[1].value,'优秀')
                self.assertEqual(data[1].value, self.driver.find_element_by_xpath(
                    '//*[@id="cyber-datahub"]/main/header/div[2]/a/span').text)

            time.sleep(1)
        else:
            self.log.add_log(str(data[0].value),str(data[2].value),'用例执行成功')
    def test_register(self):
        """测试跳转注册页面"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()
            self.assertEqual('用户注册', self.driver.find_element_by_xpath('//*[ @id ="app1"]/div[2]/div/div[1]/span').text)
        except AssertionError as e:
            self.log.add_log('','',format(e))
            self.pngpath =self.pngpath+'test_register'+'.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('用户注册', self.driver.find_element_by_xpath('//*[ @id ="app1"]/div[2]/div/div[1]/span').text)
        else:
            self.log.add_log('用户注册界面', "验证成功", '用例执行成功')
        time.sleep(1)
    def test_register_name_null(self):
        """测试注册页name空值情况:鼠标聚焦'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()#查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="name"]').click()#查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').click()#把姓名文本框鼠标焦点转移到其他文本框
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_null' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户为空验证", '用例执行成功')
        time.sleep(1)
    def test_register_name_null_register(self):
        """用户名为空时，点击注册按钮"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[8]/input').click()  #点击注册按钮
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath(
                '//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_null_register' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户为空验证", '用例执行成功')
        time.sleep(1)
    def test_register_name_Chinese(self):
        """测试注册页name文字类型验证情况:规定长度内中文非中文'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="name"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('中文')
            self.driver.find_element_by_xpath('//*[@id="account"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_Chinese' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户中文验证", '用例执行成功')
        time.sleep(1)
    def test_register_name_Chinese_length_less(self):
        """测试注册页name文字类型验证情况:长度小于2的中文'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="name"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('中')
            self.driver.find_element_by_xpath('//*[@id="account"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_Chinese_length_less' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户中文长度", '用例执行成功')
        time.sleep(1)
    def test_register_name_Chinese_length_more(self):
        """测试注册页name文字类型验证情况:长度大于40的中文'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="name"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('中')
            self.driver.find_element_by_xpath('//*[@id="account"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_Chinese_length_more' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户中文长度", '用例执行成功')
        time.sleep(1)
    def test_register_name_notChinese(self):
        """测试注册页name文字类型验证情况:数字'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="name"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('！@#￥%……&*（）——+123213jggjk')
            self.driver.find_element_by_xpath('//*[@id="account"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_notChinese' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('姓名为2-40位中文字符！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[1]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户非中文验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_null(self):
        """测试注册页account空值情况:鼠标聚焦'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦用户名文本框
            self.driver.find_element_by_xpath('//*[@id="name"]').click()  # 把用户名文本框鼠标焦点转移到其他文本框
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_null' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户名为空验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_null_register(self):
        """用户名为空时，点击注册按钮"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[8]/input').click()  # 点击注册按钮
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_name_null_register' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('请填写信息！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户名为空验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_alph(self):
        """测试注册页account文字类型验证情况:字母'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('aaaaaa')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_alph' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户名字母验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_number(self):
        """测试注册页account文字类型验证情况:数字'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('123456')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_number' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户数字验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_Chinese(self):
        """测试注册页account文字类型验证情况:中文'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('中文')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_Chinese' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户中文验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_specialchar(self):
        """测试注册页account文字类型验证情况:特殊字符'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('!@#$%^&*(){}|<>?')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_specialchar' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户特殊字符验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_alph_number_(self):
        """测试注册页account文字类型验证情况:字母数字下划线'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('qw123_')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_alph_number_' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('通过信息验证！', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户字母数字下划线验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_number_alph_(self):
        """测试注册页account文字类型验证情况:数字字母下划线'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('12daasd123_')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_number_alph_' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户字母数字下划线验证", '用例执行成功')
        time.sleep(1)
    def test_register_account__number_alph(self):
        """测试注册页account文字类型验证情况:下划线数字字母'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('12daasd123_')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account__number_alph' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户字母数字下划线验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_alph_number_less(self):
        """测试注册页account文字类型验证情况:下划线数字字母少'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('q1_')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account_alph_number_less' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户字母数字下划线验证", '用例执行成功')
        time.sleep(1)
    def test_register_account_alph_number_more(self):
        """测试注册页account文字类型验证情况:下划线数字字母多'"""
        try:
            self.driver.find_element_by_xpath('//*[@id="subform"]/div[4]/span/a').click()  # 查询点击这里进入注册页面
            self.driver.find_element_by_xpath('//*[@id="account"]').click()  # 查询点击聚焦姓名文本框
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('xiaolanlan12345667712_')
            self.driver.find_element_by_xpath('//*[@id="name"]').click()
            print(self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        except AssertionError as e:
            self.log.add_log('', '', format(e))
            self.pngpath = self.pngpath + 'test_register_account__number_alph' + '.png'
            self.driver.get_screenshot_as_file(self.pngpath)
            self.assertEqual('4-20个字符，只能包含字母、数字、下划线，必须以字母开头', self.driver.find_element_by_xpath('//*[@id="app1"]/div[2]/div/div[2]/form/div[2]/div/span[2]').text)
        else:
            self.log.add_log('用户注册界面', "用户字母数字下划线验证", '用例执行成功')
        time.sleep(1)
    def test_login1(self):
        print(1)
    def test_longin2(self):
        print(2)
if __name__=='__main__':
    # pass
    suite = unittest.TestSuite()
    suite.addTest(Test_Login('test_login'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
     # unittest.main()
