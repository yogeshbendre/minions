# This is a sample test.
# All the parameters are to be passed as environment variables.
# Then use them with os.getenv("<param_name>")


from vcst.ConnectAnchor import ConnectAnchor
import os

class Test:

    def __init__(self):
        pass

    def loginToVc(self):
        self.si = ConnectAnchor(os.getenv("vcenter"), os.getenv("username"), os.getenv("password"))

    def opDivideByX(self,x):
        try:
            abc = 1/x
        except Exception as e:
            pass

    def testSetup(self):
        #a=1/0
        self.opDivideByX(1)

    def testTask(self):
        self.loginToVc()
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)

    def testCleanup(self):
        self.opDivideByX(1)
