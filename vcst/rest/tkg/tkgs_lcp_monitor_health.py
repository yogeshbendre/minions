# Author: ybendre
# Test: tkgs_register_deregister
# This test will register and deregister tkgs (wcp) with TMC

import json
import os
import time
from vcst.rest.tkg.TMCHandler import TMC

class Test:

    def __init__(self):
        self.param_valid = True
        self.tmc_url = os.getenv("tmc_url")
        if self.tmc_url is None:
            print("No tmc_url provided, please set environment variable tmc_url")
            self.param_valid = False
            return
        self.api_token = os.getenv("api_token")
        if self.api_token is None:
            print("No api_token provided, please set environment variable api_token")
            self.param_valid = False
            return
        self.org_id = os.getenv("org_id")
        if self.org_id is None:
            print("No org_id provided, please set environment variable org_id")
            self.param_valid = False
            return
        self.lcp_name = os.getenv("lcp_name")
        if self.lcp_name is None:
            print("No lcp_name provided, please set environment variable lcp_name")
            self.param_valid = False
            return
        self.tmc = TMC(self.tmc_url, self.api_token, self.org_id)

    def isLCPHealthy(self):
        myresp = self.tmc.get_local_control_plane(self.lcp_name)
        print(myresp)
        isHealthy = True
        try:
            lcp_info = myresp.json()
            if ("healthy" in lcp_info["localcontrolplane"]["status"]["health"].lower()):
                print("LCP: " + self.lcp_name + " seems to be healthy.")
                isHealthy = True
            else:
                print("LCP: " + self.lcp_name + " seems to be unhealthy.")
                isHealthy = False

        except Exception as e:
            print("Health check for " + self.lcp_name + " failed with " + str(e))
            isHealthy = False
        return isHealthy


def testSetup(self):
        if self.param_valid:
            return True
        else:
            print("Some parameters are not valid.")
            return False


    def testTask(self):
        success = True
        try:
            success = self.isLCPHealthy()
            return success
        except Exception as e:
            return False

    def testCleanup(self):
        return True







