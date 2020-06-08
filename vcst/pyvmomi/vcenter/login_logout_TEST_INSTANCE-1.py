import logging.config


# Author: ybendre
# Test: login_logout
# This test will perform login-logout of vcenter

import json
import os
from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass

class Test:


    def __init__(self,testlogger):
        self.logger = testlogger
        self.logger.info('Perform __init__')
        self.vc=os.getenv("vcenter")
        if self.vc is None:
            self.logger.info("No vCenter provided, please set environment variable vcenter")
            return None

        self.username = os.getenv("vcuser")
        if self.username is None:
            self.username = "administrator@vsphere.local"

        self.password=os.getenv("vcpassword")
        if self.password is None:
            self.password = "Admin!23"

        self.port = os.getenv("port")
        if self.port is None:
            self.port = "443"
        self.mysession = None
        self.content = None

        # Function to get the vCenter server session

        self.logger.info('Finished  __init__')

    def login(self):
        self.logger.info('Perform login')
        try:
            si = SmartConnectNoSSL(host=self.vc, user=self.username, pwd=self.password, port=self.port)
            self.mysession = si
            return True
        except Exception as e:
            self.logger.error('Failed in login: '+str(e))
            self.logger.exception('')
            self.logger.info("Authentication failed")
            self.mysession = None
            return False

        self.logger.info('Finished  login')

    def logout(self):
        self.logger.info('Perform logout')
        try:
            Disconnect(self.mysession)
            return True
        except Exception as e:
            self.logger.error('Failed in logout: '+str(e))
            self.logger.exception('')
            self.logger.info("Logout failed")
            self.mysession = None
            return False


        self.logger.info('Finished  logout')

    def testSetup(self):
        self.logger.info('Perform testSetup')
        return True

        self.logger.info('Finished  testSetup')

    def testTask(self):
        self.logger.info('Perform testTask')
        if self.login():
            if self.logout():
                return True
            else:
                return False
        else:
            return False
        

        self.logger.info('Finished  testTask')

    def testCleanup(self):
        self.logger.info('Perform testCleanup')
        return True
