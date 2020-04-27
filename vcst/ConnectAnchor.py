from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import logging.config

class ConnectAnchor:

    vcenter = None
    username = None
    password = None
    service_instance = None


    def __init__(self,vcenter,username,password):
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('vcst.ConnectAnchor')
        self.vcenter = vcenter
        self.logger.info(self.vcenter)
        self.username = username
        self.logger.info(self.username)
        self.password = password
        self.logger.info(self.password)

    def getContent(self):
        return self.service_instance.Retrieve_Content()

    def loginToVc(self):
        self.logger.info("Perform Login to vCenter")
        try:
            si = SmartConnectNoSSL(
                host=self.vcenter,
                user=self.username,
                pwd=self.password)
                # port=args.port)
            self.service_instance = si
            self.logger.info("Login Successful")
            return si
        except Exception as e:
            self.logger.error("Login to vCenter failed "+str(e))
            return None