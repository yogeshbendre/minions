# Author: ybendre
# Test: configur_wcp_tools
# This test will put some tools on wcp masters

import json
import os
import requests
import time
from vcst.rest.tkg import WCPFetcher as wf


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

        self.lihost = os.getenv("lihost")
        if self.lihost is None:
            self.lihost = "10.199.56.56"

        self.port = os.getenv("port")
        if self.port is None:
            self.port = "443"
        self.numMasters = os.getenv("numMasters")
        if self.numMasters is None:
            self.numMasters = 3
        self.numMasters = int(self.numMasters)
        self.wcpfetcher = wf(self.vc, self.username, self.password)



    def runCommandOnWCPClusters(self, cmd, sleepTime=0):
        for w in self.wcpfetcher.wcp_info:
            self.wcpfetcher.run_command_on_each_master(w, cmd, self.numMasters)
            time.sleep(sleepTime)

    def ifconfig(self):
        cmd1 = 'ifconfig'
        self.runCommandOnWCPClusters(cmd1, 0)



    def installLogInsightAgent(self):
        cmd1 = 'curl -k -X GET "https://10.199.56.1/LI/LIAgent.rpm - o /root/LIAgent.rpm"'
        cmd2 = 'SERVERHOST='+self.lihost+' rpm -i /root/LIAgent.rpm'
        cmd3 = '/etc/init.d/liagentd start'
        self.runCommandOnWCPClusters(cmd1, 2)
        self.runCommandOnWCPClusters(cmd2, 2)
        self.runCommandOnWCPClusters(cmd3, 2)

    def testSetup(self):
        if self.param_valid:
            return True
        else:
            print("Some parameters are not valid.")
            return False

    def testTask(self):
        try:
            self.installLogInsightAgent()
            return True
        except Exception as e:
            return False

    def testCleanup(self):
        return True







