# Author: ybendre
# Test: vmotion
# This test will perform vmotion of vm

import json
import os
from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass

class Test:

    def __init__(self):
        self.vc=os.getenv("vcenter")
        if self.vc is None:
            self.logger.info("No vCenter provided, please set environment variable vcenter")
            return
        self.vm = os.getenv("testvm")
        if self.vm is None:
            self.logger.info("No vm name provided, please set environment variable testvm")
            return

        self.desthost = os.getenv("testdesthost")
        if self.vm is None:
            self.logger.info("No desthost name provided, please set environment variable testdesthost")
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
        self.mysession = None
        self.content = None

        # Function to get the vCenter server session

    def get_vc_session(self):
        try:
            si = SmartConnectNoSSL(host=self.vc, user=self.username, pwd=self.password, port=self.port)
            self.mysession = si
        except Exception as e:
            print("Authentication failed")
            self.mysession = None
            return None

    def wait_for_task(self, task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                self.logger.info("Task completed successfully")
                return task.info.result

            if task.info.state == 'error':
                self.logger.error("there was an error")
                task_done = True

    def get_obj(self, vimtype, name):
        """
        Return an object by name, if name is None the
        first found object is returned
        """
        obj = None
        container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break

        return obj

    def vmotion_vm(self, vm_name, dest_host):
        self.logger.info("Search VM to be vmotioned "+vm_name)
        vm = self.get_obj([vim.VirtualMachine], vm_name)
        self.logger.info("VM Found")
        self.logger.info("Search dest host "+dest_host)
        destination_host = self.get_obj([vim.HostSystem], dest_host)
        self.logger.info("Dest host found")
        resource_pool = vm.resourcePool

        migrate_priority = vim.VirtualMachine.MovePriority.defaultPriority

        msg = "Migrating %s to destination host %s" % (vm_name, dest_host)
        self.logger.info(msg)

        # Live Migration :: Change host only
        task = vm.Migrate(pool=resource_pool, host=destination_host, priority=migrate_priority)
        self.wait_for_task(task)

    def testSetup(self):
        self.get_vc_session()
        self.content = self.mysession.RetrieveContent()


    def testTask(self):
        self.vmotion_vm(self.vm, self.desthost)
        return True

    def testCleanup(self):
        pass

