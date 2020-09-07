import logging.config


# Author: ybendre
# Test: login_logout
# This test will replace vCenter certificates

import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mysession = requests.Session()
mysession.verify = False

class Test:


    def __init__(self,testlogger):
        self.logger = testlogger
        self.logger.info('Perform __init__')
        self.vc=os.getenv("vcenter")
        if self.vc is None:
            self.logger.info("No vCenter provided, please set environment variable vcenter")
            return
        self.username = os.getenv("vcuser")
        if self.username is None:
            self.username = "administrator@vsphere.local"

        self.password=os.getenv("vcpassword")
        if self.password is None:
            self.password = "Admin!23"

        self.port = os.getenv("port")
        if self.port is None:
            self.port = "443"

        self.mysession=mysession
        self.sessionval = None

        # Function to get the vCenter server session

        self.logger.info('Finished  __init__')

    def get_vc_session(self):
        self.logger.info('Perform get_vc_session')
        myresp = None
        self.logger.info(self.vc)
        self.logger.info(self.username)
        self.logger.info(self.mysession)
        try:
            myurl='https://' + self.vc + ":" + self.port + '/rest/com/vmware/cis/session'
            self.logger.info(myurl)
            myresp = self.mysession.post(myurl,auth=(self.username, self.password))
            self.logger.info(myresp.text)
            ret = json.loads(myresp.text)["value"]
            self.sessionval = ret
            self.logger.info("Logged In Successfully")
            return ret
        except Exception as e:
            self.logger.error('Failed in get_vc_session: '+str(e))
            self.logger.exception('')
            self.logger.info("Authentication failed")
            self.logger.info(myresp.text)
            self.sessionval = None
            return None

        self.logger.info('Finished  get_vc_session')

    def testSetup(self):
        self.logger.info('Perform testSetup')
        return True

        self.logger.info('Finished  testSetup')

    def testTask(self):
        self.logger.info('Perform testTask')
        self.get_vc_session()
        return True

        self.logger.info('Finished  testTask')

    def testCleanup(self):
        self.logger.info('Perform testCleanup')
        return True

