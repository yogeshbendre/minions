# Author: ybendre
# Test: tkgs_register_deregister
# This test will register and deregister tkgs (wcp) with TMC

import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from vcst.rest.tkg.TMCEnable import workflow as enable_workflow
from vcst.rest.tkg.TMCDisable import workflow as disable_workflow

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mysession = requests.Session()
mysession.verify = False
#Params: vc, username, password, tmc_url, api_token, org_id, lcp_prefix, monitor_time_in_min, yaml_action, force_delete
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
        self.lcp_prefix = os.getenv("lcp_prefix")
        if self.lcp_prefix is None:
            print("No lcp_prefix provided, please set environment variable lcp_prefix")
            self.param_valid = False
            return
        self.monitor_time_in_min = os.getenv("monitor_time_in_min")
        if self.monitor_time_in_min is None:
            self.monitor_time_in_min = 5
        self.monitor_time_in_min = int(self.monitor_time_in_min)

        self.yaml_action = os.getenv("yaml_action")
        if self.yaml_action is None:
            self.yaml_action = "apply"

        self.force = True
        force_delete = os.getenv("force_delete")
        if force_delete is None:
            force_delete = "true"
        if "false" in force_delete.lower():
            self.force = False


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
        success = False
        try:
            success = enable_workflow(self.vc, self.username, self.password, self.tmc_url, self.api_token, self.org_id, self.lcp_prefix, self.monitor_time_in_min, self.yaml_action)
            if success:
                success = disable_workflow(self.vc, self.username, self.password, self.tmc_url, self.api_token, self.org_id, self.lcp_prefix, self.monitor_time_in_min, self.yaml_action, self.force)
            return success
        except Exception as e:
            return False


        return True


    def testCleanup(self):
        return True







