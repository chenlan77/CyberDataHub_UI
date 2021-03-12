import unittest

class  MyTest(unittest.TestCase):
   def test_login(self):
       print("OK")

if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(Test_Login('test_login'))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
     unittest.main()