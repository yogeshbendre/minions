from IntelligentProcessor import IntelligentProcessor as IP

class minion:

    testfilepath = None
    newtestfilepath = None
    testobj = None
    mysuffix = '_run'

    def __init__(self,testfilepath):
        self.testfilepath = testfilepath
        self.newtestfilepath = testfilepath + self.mysuffix

    def preprocessTestFile(self):

        #mycontent = None
        srcFile = self.testfilepath.replace('.','/')+'.py'
        destFile = self.newtestfilepath.replace('.', '/') + '.py'
        #with open(srcFile,'r') as fp:
        #   mycontent = fp.read()

        #with open(destFile, 'w') as fp:
        #    fp.write(mycontent)
        myprocessor = IP(srcFile,destFile)
        myprocessor.processContents()
        print('Processed: '+self.testfilepath)

    def initializeTestObj(self):
        mod = __import__(self.newtestfilepath, fromlist=['Test'])
        myclass = getattr(mod, 'Test')
        self.testobj = myclass()

    def testMe(self):
        self.testobj.printInfo()
        try:
            self.testobj.testSetup()

        except Exception as e:
            print("Test Setup Failed: "+str(e))
            return

        try:
            self.testobj.testTask()
        except Exception as e:
            print("Test Failed: "+str(e))

        try:
            self.testobj.testCleanup()
        except Exception as e:
            print("Test Cleanup Failed: "+str(e))


