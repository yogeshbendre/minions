from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

class ConnectAnchor:

    vcenter = None
    username = None
    password = None
    service_instance = None


    def __init__(self,vcenter,username,password):
        self.vcenter = vcenter
        self.username = username
        self.password = password

    def loginToVc(self):
        si = SmartConnectNoSSL(
            host=self.vcenter,
            user=self.username,
            pwd=self.password)
        # port=args.port)
        self.service_instance = si
        return si