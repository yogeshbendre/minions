import logging.config


# This is a sample test.
# All the parameters are to be passed as environment variables.
# Then use them with os.getenv("<param_name>")


from vcst.ConnectAnchor import ConnectAnchor
import os

class Test:


    def __init__(self):
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('vcst.sample.test.test')
        self.logger.info('Perform __init__')
        pass

        self.logger.info('Finished  __init__')

    def loginToVc(self):
        self.logger.info('Perform loginToVc')
        self.si = ConnectAnchor(os.getenv("vcenter"), os.getenv("username"), os.getenv("password"))

        self.logger.info('Finished  loginToVc')

    def opDivideByX(self,x):
        self.logger.info('Perform opDivideByX')
        try:
            abc = 1/x
        except Exception as e:
            self.logger.error('Failed in opDivideByX: '+str(e))
            pass

        self.logger.info('Finished  opDivideByX')

    def testSetup(self):
        self.logger.info('Perform testSetup')
        #a=1/0
        self.opDivideByX(1)

        self.logger.info('Finished  testSetup')

    def testTask(self):
        self.logger.info('Perform testTask')
        self.loginToVc()
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)
        self.opDivideByX(0)

        self.logger.info('Finished  testTask')

    def testCleanup(self):
        self.logger.info('Perform testCleanup')
        self.opDivideByX(1)
