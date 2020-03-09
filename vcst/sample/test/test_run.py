
class Test:


    def __init__(self):
        print('Perform __init__')
        pass

        print('Finished  __init__')

    def printInfo(self):
        print('Perform printInfo')
        pass

        print('Finished  printInfo')

    def opDivideByX(self,x):
        print('Perform opDivideByX')
        try:
            abc = 1/x
        except Exception as e:
            print('Failed in opDivideByX: '+str(e))
            dosomethingelse = True

        print('Finished  opDivideByX')

    def testSetup(self):
        print('Perform testSetup')
        a=1/0
        self.opDivideByX(1)

        print('Finished  testSetup')

    def testTask(self):
        print('Perform testTask')
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)

        print('Finished  testTask')

    def testCleanup(self):
        print('Perform testCleanup')
        self.opDivideByX(1)
