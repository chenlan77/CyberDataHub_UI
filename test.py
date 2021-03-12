import os
def test():
        curPath = os.path.abspath(os.path.dirname(__file__))
        print("curPath:",curPath)
        rootPath = curPath[:curPath.find("pycharmWorkSpace\\") + len("CyberDataHubAuto\\")]  # 获取myProject，也就是项目的根路径
        print("rootPath:",rootPath)
if __name__=='__main__':
        test()