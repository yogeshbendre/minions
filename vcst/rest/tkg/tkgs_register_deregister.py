# Author: ybendre
# Test: tkgs_register_deregister
# This test will register and deregister tkgs (wcp) with TMC

import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from TMCEnable import workflow as enable_workflow
from TMCDisable import workflow as disable_workflow

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mysession = requests.Session()
mysession.verify = False

class Test:

    def __init__(self):
        self.param_valid = True
        self.vc = os.getenv("vcenter")
        if self.vc is None:
            print("No vCenter provided, please set environment variable vcenter")
            self.param_valid = False
            return
        self.username = os.getenv("vcuser")
        if self.username is None:
            self.username = "root"

        self.password=os.getenv("vcpassword")
        if self.password is None:
            self.password = "Admin!23"

        self.port = os.getenv("port")
        if self.port is None:
            self.port = "443"

        self.mysession=mysession
        self.sessionval = None

        # Function to get the vCenter server session

    def testSetup(self):
        if self.param_valid:
            return True
        else:
            print("Some parameters are not valid.")
            return False


    def testTask(self):
        return True


    def testCleanup(self):
        return True







