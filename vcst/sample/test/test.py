# This is a sample test.
# All the parameters are to be passed as environment variables.
# Then use them with os.getenv("<param_name>")


from vcst.ConnectAnchor import ConnectAnchor
import os

class Test:

    def __init__(self):
        pass

    def loginToVc(self):
        self.ca = ConnectAnchor(os.getenv("vcenter"), os.getenv("username"), os.getenv("password"))
        self.si = self.ca.loginToVc()

    def opDivideByX(self,x):
        try:
            abc = 1/x
        except Exception as e:
            pass

    def testSetup(self):
        self.loginToVc()

    def testTask(self):
        self.opDivideByX(0)

    def testCleanup(self):
        self.opDivideByX(1)
