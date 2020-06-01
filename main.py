from IntelligentProcessor import IntelligentProcessor as IP
import os
import logging.config


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class minion:

    testfilepath = None
    newtestfilepath = None
    testobj = None
    mysuffix = '_run'

    def __init__(self,testfilepath,preprocess=False):
        self.testfilepath = testfilepath
        self.newtestfilepath = testfilepath + self.mysuffix
        logging.config.fileConfig('logging.conf', False)
        self.logger = logging.getLogger('minion')
        #self.logger = setup_logger('minion', 'minion.log')
        self.clientlogger = setup_logger(testfilepath, 'test.log')
        if preprocess:
            self.preprocessTestFile()
        else:
            self.newtestfilepath = testfilepath

    def preprocessTestFile(self):
        srcFile = self.testfilepath.replace('.','/')+'.py'
        destFile = self.newtestfilepath.replace('.', '/') + '.py'
        myprocessor = IP(srcFile,destFile)
        myprocessor.processContents()
        self.logger.info('Processed: '+self.testfilepath)

    def initializeTestObj(self):
        mod = __import__(self.newtestfilepath, fromlist=['Test'])
        myclass = getattr(mod, 'Test')
        self.testobj = myclass(self.clientlogger)
        if self.testobj is None:
            self.logger.error("Failed to create test object")
            exit(1)

    def testMe(self, iterations, retryCnt):
        self.logger.info("Trigger test for iterations: "+str(iterations)+" with retryCnt: "+str(retryCnt))
        passed = 0
        failed = 0
        retry = 0
        try:
            self.testobj.testSetup()
            self.logger.info("Test Setup Passed")
        except Exception as e:
            self.logger.error("Test Setup Failed: "+str(e))
            return

        for it in range(0, iterations):
            try:
                testSuccess = self.testobj.testTask()
                assert (testSuccess), "Test Failed"
                passed=passed + 1
                self.logger.info("Test Passed Iteration "+str(it+1)+" Out of "+str(iterations)+" Pass Rate: "+str(round(100*passed/iterations))+"%")
            except Exception as e:
                self.logger.info("Test Failed Iteration "+str(it+1)+" Out of "+str(iterations)+" Pass Rate: "+str(round(100*passed/iterations))+"%")
                failed = failed+1
                retry = retry + 1
                if retry > retryCnt:
                    break
                continue
        try:
            self.testobj.testCleanup()
        except Exception as e:
            self.logger.warning("Test Cleanup Failed: "+str(e))

        pp = round(100*passed/iterations)
        self.logger.info("Test Result: Total: "+str(iterations)+" Pass: "+str(passed)+" Failed: "+str(failed)+" Pass Percentage: "+str(pp)+"%")

