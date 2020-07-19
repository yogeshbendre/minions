# Author: ybendre
# Test: recertify
# This test will replace vCenter certificates

import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mysession = requests.Session()
mysession.verify = False

class Test:

    def __init__(self):
        self.vc=os.getenv("vcenter")
        if self.vc is None:
            print("No vCenter provided, please set environment variable vcenter")
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

    def get_vc_session(self):
        myresp = None
        print(self.vc)
        print(self.username)
        print(self.mysession)
        try:
            myurl='https://' + self.vc + ":" + self.port + '/rest/com/vmware/cis/session'
            print(myurl)
            myresp = self.mysession.post(myurl,auth=(self.username, self.password))
            print(myresp.text)
            ret = json.loads(myresp.text)["value"]
            self.sessionval = ret
            print("Logged In Successfully")
            return ret
        except Exception as e:
            print("Authentication failed")
            print(myresp.text)
            self.sessionval = None
            return None

    def testSetup(self):
        self.get_vc_session()
        return True

    def testTask(self):
        myurl = "https://"+self.vc+":"+self.port+" /rest/vcenter/certificate-management/vcenter/vmca-root"
        mydata={}

        myheader = {
            "Content-Type": "application/json",
            "'vmware-api-session-id": str(self.sessionval)
        }
        print(myurl)
        myresp=self.mysession.post(myurl,data=json.dumps(mydata),headers=myheader)
        print(myresp.text)
        self.logger.info(myresp.status_code)
        self.logger.info(str(myresp.text))
        return True

    def testCleanup(self):
        pass

