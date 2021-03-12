import unittest,time,ddt
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from untils.excel_read import  ParseExcel
excelPath = './../../data_manage/csv_file/login_user.xlsx'
sheetName = 'Sheet1'
excel = ParseExcel(excelPath, sheetName)
from untils.upload_file import set_uploader
from untils.upload_file import set_uploader

@ddt.ddt
class Test_MyResources(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # 类加载初始加载的前置初始化
        self.driver=webdriver.Chrome()
        self.driver.get('http://192.168.199.235:38092/oauth/authorize?client_id=mJrcghz5g6&response_type=code&redirect_uri=http%3A%2F%2F192.168.199.143%3A17080%2Fgateway')
    @classmethod
    def tearDownClass(self):
        # 类运行完毕后的后置处理
        self.driver.quit()
    def setUp(self):
        pass
    def tearDown(self):
        pass
    # 用例部分
    @ddt.data(*excel.getDataFromSheet())
    def test_login(self,data):
        # 登录部分
        # 放大窗口
        print(data)
        self.driver.maximize_window()
        # 登录用户名与密码，及点击登录
        self.driver.find_element_by_id('username').send_keys('chenlan')
        self.driver.find_element_by_id('password').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="subform"]/button').click()
        time.sleep(2)
    def test_myresources_newbuild_file_csv(self):
        '''数据发布中心-我的资源-资源新建：csv文件上传'''
        # 登录后切换至数据发布中心模块
        self.driver.find_element_by_xpath('//a[@href="/dataset"]').click()
        # self.driver.find_element_by_xpath('//header[@class="app-header"]/div[1]/a[6]').click()
        time.sleep(2)
        # 转换至ifram框才可以定位里面的元素
        iframe=self.driver.find_element_by_xpath('//iframe[@id="dataset"]')
        self.driver.switch_to.frame(iframe)
        # 定位我的资源模块元素并点击展开我的资源菜单列表
        self.driver.find_element_by_xpath('//*[@id="cyber-dataset"]/div/main/ul/li[2]').click()
        # 定位我的资源下的资源目录并点击进入资源目录列表
        self.driver.find_element_by_xpath('//ul[@id="/private$Menu"]/li[1]').click()
        time.sleep(1)
        # 定位新建按钮并点击进入新建资源页
        self.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-two-chinese-chars"]').click()
        time.sleep(2)

        # 新建资源页输入内容
        # 获取上传按钮元素
        upload_element =self.driver.find_element_by_xpath('//div[@class="block"]/div/div[2]/div[1]/div[2]/div/span/span/div/span/span/span/span')
        # 点击弹窗上传文件弹窗
        ActionChains(self.driver).move_to_element(upload_element).click().perform()
        # 点击上传文件弹出上传文件窗口
        ActionChains(self.driver).release()
        time.sleep(3)  # 为了看效果
        # 获取数据文件相对路径
        file_path = 'data_manage\csv_file\eastelecps.eastelec_data_process1000.csv'
        # 调用上传文件方法
        set_uploader(file_path, "CyberDataHubAuto\\")
        # 获取资源名称文本框元素
        date_time = datetime.datetime.now()
        date = date_time.strftime('%m%d%H%M%S')
        self.driver.find_element_by_xpath('//input[@id="resourceName"]').send_keys('Auto'+date)
        time.sleep(3)
        self.driver.find_element_by_xpath('//textarea[@id="resourceDescription"]').send_keys('自动化测试脚本测试资源简介')
        time.sleep(3)
        # js = "var q=document.getElementById('id').scrollTop=10000"
        # self.driver.execute_script(js)
        self.driver.find_element_by_xpath('//div[@class="block"]/div/div[6]/div[2]/div/span/div/button[2]').click()
        time.sleep(20)
    # def test_myresources_newbuild_file_ftp(self):
    #     '''数据发布中心-我的资源-资源新建：ftp文件上传'''
    #     # 登录后切换至数据发布中心模块
    #     self.driver.find_element_by_xpath('//a[@href="/dataset"]').click()
    #     # self.driver.find_element_by_xpath('//header[@class="app-header"]/div[1]/a[6]').click()
    #     time.sleep(2)
    #     # 转换至ifram框才可以定位里面的元素
    #     iframe = self.driver.find_element_by_xpath('//iframe[@id="dataset"]')
    #     self.driver.switch_to.frame(iframe)
    #     # 定位我的资源模块元素并点击展开我的资源菜单列表
    #     self.driver.find_element_by_xpath('//*[@id="cyber-dataset"]/div/main/ul/li[2]').click()
    #     # 定位我的资源下的资源目录并点击进入资源目录列表
    #     self.driver.find_element_by_xpath('//ul[@id="/private$Menu"]/li[1]').click()
    #     time.sleep(1)
    #     # 定位新建按钮并点击进入新建资源页
    #     self.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-two-chinese-chars"]').click()
    #     time.sleep(2)
    #
    #     # 新建资源页输入内容
    #     # 获取本地与ftp按钮元素
    #     self.driver.find_element_by_xpath('//div[@class="local-type ant-select ant-select-enabled"]').click()
    #
    #     # 获取上传按钮元素
    #     upload_element = self.driver.find_element_by_xpath(
    #         '//div[@class="block"]/div/div[2]/div[1]/div[2]/div/span/span/div/span/span/span/span')
    #     # 点击弹窗上传文件弹窗
    #     ActionChains(self.driver).move_to_element(upload_element).click().perform()
    #     # 点击上传文件弹出上传文件窗口
    #     ActionChains(self.driver).release()
    #     time.sleep(3)  # 为了看效果
    #     # 获取数据文件相对路径
    #     file_path = 'data_manage\csv_file\eastelecps.eastelec_data_process1000.csv'
    #     # 调用上传文件方法
    #     set_uploader(file_path, "CyberDataHubAuto\\")
    #     # 获取资源名称文本框元素
    #     date_time = datetime.datetime.now()
    #     date = date_time.strftime('%m%d%H%M%S')
    #     self.driver.find_element_by_xpath('//input[@id="resourceName"]').send_keys('Auto' + date)
    #     time.sleep(3)
    #     self.driver.find_element_by_xpath('//textarea[@id="resourceDescription"]').send_keys('自动化测试脚本测试资源简介')
    #     time.sleep(3)
    #     # js = "var q=document.getElementById('id').scrollTop=10000"
    #     # self.driver.execute_script(js)
    #     self.driver.find_element_by_xpath('//div[@class="block"]/div/div[6]/div[2]/div/span/div/button[2]').click()
    #     time.sleep(20)
    def test_myresources_newbuild_datamap(self):
        '''数据发布中心-我的资源-资源新建：数据地图内容发布'''
        # 登录后切换至数据发布中心模块
        self.driver.find_element_by_xpath('//a[@href="/dataset"]').click()
        # self.driver.find_element_by_xpath('//header[@class="app-header"]/div[1]/a[6]').click()
        time.sleep(2)
        # 转换至ifram框才可以定位里面的元素
        iframe = self.driver.find_element_by_xpath('//iframe[@id="dataset"]')
        self.driver.switch_to.frame(iframe)
        # 定位我的资源模块元素并点击展开我的资源菜单列表
        self.driver.find_element_by_xpath('//*[@id="cyber-dataset"]/div/main/ul/li[2]').click()
        # 定位我的资源下的资源目录并点击进入资源目录列表
        self.driver.find_element_by_xpath('//ul[@id="/private$Menu"]/li[1]').click()

        time.sleep(3)
        self.driver.find_element_by_xpath('//ul[@class="ant-pagination ant-table-pagination"]/li[3]').click()
        # # 定位新建按钮并点击进入新建资源页
        # self.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-two-chinese-chars"]').click()
        # time.sleep(2)
        # # 定位数据地图redio元素及点击
        # self.driver.find_element_by_xpath('//div[@id="sourceResourceType"]/label[2]/span[1]').click()
        # time.sleep(2)
        # # 定位请选择数据地图文本框并点击
        # self.driver.find_element_by_xpath('//*[@class= "block"]/div/div[2]/div[2]/div/span/span').click()
        # time.sleep(2)
        # # 定位数据地图来源选择，主要是三个分层：ADS、CDM、ODS分别是li[1],li[2],li[3]
        # self.driver.find_element_by_xpath('//div[@class= "ant-cascader-menus ant-cascader-menus-placement-bottomLeft"]/div/ul[1]/li[1]').click()
        # time.sleep(2)
        # # 定位某个分层下的数据库列表并点击选中某数据库
        # self.driver.find_element_by_xpath('//div[@class= "ant-cascader-menus ant-cascader-menus-placement-bottomLeft"]/div/ul[2]/li[1]').click()
        # time.sleep(2)
        # # 定位某个数据库下的表单列表并点击选中某表单
        # self.driver.find_element_by_xpath('//div[@class= "ant-cascader-menus ant-cascader-menus-placement-bottomLeft"]/div/ul[3]/li[1]').click()
        # time.sleep(1)
        # date_time = datetime.datetime.now()
        # date = date_time.strftime('%m%d%H%M%S')
        # # 定位资源名称并添加名称
        # self.driver.find_element_by_xpath('//input[@id="resourceName"]').send_keys('DataMapAuto'+date)
        # # 添加资源简介
        # self.driver.find_element_by_xpath('//textarea[@id="resourceDescription"]').send_keys('自动化测试脚本测试资源简介_数据地图')
        # # 点击下一步进入数据解析界面
        # self.driver.find_element_by_xpath('//div[@class="block"]/div/div[6]/div[2]/div/span/div/button[2]').click()
        # time.sleep(2)
        # # 点击保存按钮提交数据
        # self.driver.find_element_by_xpath('//div[@class="block"]/div/div/button[3]').click()
        # time.sleep(10)
        #定位资源列表刷新按钮刷新页面数据
        # self.driver.find_element_by_xpath('//div[@class="table-toolbar__buttons"]/button').click()

        # print(len(lis))
        # # len(lis)  # 有多少个li
        # lis[-1].click()  # 最后一个li



if __name__=='__main__':
    unittest.main()