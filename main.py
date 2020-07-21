from IntelligentProcessor import IntelligentProcessor as IP
import os
import logging.config
import time

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
    mysuffix = '_TEST'

    def __init__(self,testfilepath, preprocess=False, instance_name="1"):
        self.testfilepath = testfilepath
        if os.getenv("instance_name") is not None:
            instance_name=os.getenv("instance_name")

        self.target = os.getenv("testtarget")
        if self.target is None:
            self.target = "Generic"

        self.gap = os.getenv("testgapsec")
        if self.gap is None:
            self.gap = '60'
        self.gap = int(self.gap)

        self.retryCnt = os.getenv("retry_count")
        if self.retryCnt is None:
            self.retryCnt = '0'
        self.retryCnt = int(self.retryCnt)

        self.testnamestring = self.target + " " +self.testfilepath + " " + instance_name
        self.mysuffix = self.mysuffix + "_INSTANCE-" + instance_name
        self.instance_name = instance_name
        self.newtestfilepath = testfilepath + self.mysuffix

        logging.config.fileConfig('logging.conf', False)
        self.logger = logging.getLogger(self.testnamestring+ ' minion')
        #self.logger = setup_logger('minion', 'minion.log')
        self.clientlogger = setup_logger(self.testnamestring+' '+self.newtestfilepath, 'test.log')
        if preprocess:
            self.preprocessTestFile()
        else:
            self.newtestfilepath = testfilepath

    def preprocessTestFile(self):
        srcFile = self.testfilepath.replace('.','/')+'.py'
        destFile = self.newtestfilepath.replace('.', '/') + '.py'
        myprocessor = IP(srcFile, destFile, self.instance_name)
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
        total = 0
        try:
            testSetupSuccess = False
            if os.getenv("testsetup") == "False":
                self.logger.info("Received command to not run setup. Skipping setup.")
                testSetupSuccess = True
            else:
                self.logger.info("Performing test setup now.")
                testSetupSuccess = self.testobj.testSetup()
                if (testSetupSuccess is None) or (not testSetupSuccess):
                    self.logger.error("Test Setup Failed")
                    if testSetupSuccess is None:
                        self.logger.info("Test setup method did not return anything. Make sure to return True (success) or False (Failure) from test setup method.")
                    exit(1)
                self.logger.info("Test Setup Passed")
        except Exception as e:
            self.logger.error("Test Setup Failed: "+str(e))
            return

        for it in range(1, (iterations+1)):
            total = total + 1
            self.logger.info("Starting iteration #", total)
            try:
                testSuccess = self.testobj.testTask()
                assert (testSuccess), "Test Failed"
                passed=passed + 1
                self.logger.info("Test Passed Iteration #"+str(it)+" Out of "+str(it)+" Current Pass Rate: "+str(round(100*passed/total))+"%")
                retry = 0
            except Exception as e:
                failed = failed + 1
                self.logger.info("Test Failed Iteration #"+str(it)+" Out of "+str(it)+" Current Pass Rate: "+str(round(100*passed/total))+"%")
                retry = retry + 1
                #continue

            pp = round(100 * passed / total)
            self.logger.info("Current Test Result: Run: " + str(total) + " out of : " + str(iterations) + " Pass: " + str(passed) + " Failed: " + str(failed) + " Pass Percentage: " + str(pp) + "%")
            self.logger.info("Completed iteration #", total)
            if retry > self.retryCnt:
                break

            if os.getenv("teststop")=="True":
                self.logger.info("Received Stop Signal, stopping the test now.")
                break
            self.logger.info("Sleeping for testgapsec sec. : " + str(self.gap))
            time.sleep(self.gap)
        try:
            self.testobj.testCleanup()
        except Exception as e:
            self.logger.warning("Test Cleanup Failed: "+str(e))

        pp = round(100*passed/total)
        self.logger.info("Final Test Result: Run: " + str(total) + " out of : " + str(iterations) + " Pass: " + str(passed) + " Failed: " + str(failed) + " Pass Percentage: " + str(pp) + "%")

