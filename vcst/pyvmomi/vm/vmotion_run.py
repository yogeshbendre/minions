import logging.config


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


    def __init__(self,testlogger):
        self.logger = testlogger
        self.logger.info('Perform __init__')
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

        self.logger.info('Finished  __init__')

    def get_vc_session(self):
        self.logger.info('Perform get_vc_session')
        try:
            si = SmartConnectNoSSL(host=self.vc, user=self.username, pwd=self.password, port=self.port)
            self.mysession = si
        except Exception as e:
            self.logger.error('Failed in get_vc_session: '+str(e))
            self.logger.exception('')
            print("Authentication failed")
            self.mysession = None
            return None

        self.logger.info('Finished  get_vc_session')

    def wait_for_task(self, task):
        self.logger.info('Perform wait_for_task')
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                self.logger.info("Task completed successfully")
                return task.info.result

            if task.info.state == 'error':
                self.logger.error("there was an error")
                task_done = True

        self.logger.info('Finished  wait_for_task')

    def get_obj(self, vimtype, name):
        self.logger.info('Perform get_obj')
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

        self.logger.info('Finished  get_obj')

    def vmotion_vm(self, vm_name, dest_host):
        self.logger.info('Perform vmotion_vm')
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

        self.logger.info('Finished  vmotion_vm')

    def testSetup(self):
        self.logger.info('Perform testSetup')
        self.get_vc_session()
        self.content = self.mysession.RetrieveContent()


        self.logger.info('Finished  testSetup')

    def testTask(self):
        self.logger.info('Perform testTask')
        self.vmotion_vm(self.vm, self.desthost)
        return True

        self.logger.info('Finished  testTask')

    def testCleanup(self):
        self.logger.info('Perform testCleanup')
        pass

