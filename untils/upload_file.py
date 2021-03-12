import win32gui
import win32con,os,time
import os
def set_uploader(file_path,pro_path):
    time.sleep(2)
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find(pro_path) + len(pro_path)]
    file_fullpath =rootPath+file_path

    if (os.path.exists(file_fullpath) == False):                                       # 判断路径是否存在
        print(u"文件路径不存在")
        return False
    else:
        try:
            dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
            ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
            ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
            Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)                     # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
            button = win32gui.FindWindowEx(dialog, 0, 'Button', None)                   # 确定按钮Button
            win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, file_fullpath)       # 往输入框输入绝对地址
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)                # 按button
            print(u'上传成功')
            time.sleep(2)
        except AttributeError as e:
            raise e

# if __name__=='__main__':
#      pass