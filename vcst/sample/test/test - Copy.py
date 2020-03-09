class Test:

    def __init__(self):
        print("I am fine")


    def printInfo(self):
        print("I am test class")


    def opDivideByX(self,x):
        try:
            abc = 1/x

        except Exception as e:
            dosomethingelse = True

    def testSetup(self):
        self.opDivideByX(1)



    def testCleanup(self):
        self.opDivideByX(1)

    def testTask(self):
        self.opDivideByX(0)
