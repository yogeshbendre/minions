class Test:

    def __init__(self):
        pass

    def printInfo(self):
        pass

    def opDivideByX(self,x):
        try:
            abc = 1/x
        except Exception as e:
            dosomethingelse = True

    def testSetup(self):
        a=1/0
        self.opDivideByX(1)

    def testTask(self):
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)

    def testCleanup(self):
        self.opDivideByX(1)
