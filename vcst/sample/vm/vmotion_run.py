import logging.config


# This is a sample test.
# All the parameters are to be passed as environment variables.
# Then use them with os.getenv("<param_name>")


from vcst.ConnectAnchor import ConnectAnchor
from vcst.helper import Helper
import os

class Test:


    def __init__(self):
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('vcst.sample.vm.vmotion')
        self.logger.info('Perform __init__')
        self.vcenter = os.getenv("vcenter")
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.vm_name = os.getenv("vm_name")
        self.src_host = os.getenv("src_host")
        self.dest_host = os.getenv("dest_host")
        self.src_host = os.getenv("src_datastore")
        self.dest_datastore = os.getenv("dest_datastore")
        self.ca = ConnectAnchor(self.vcenter, self.username, self.password)
        self.si = self.ca.loginToVc()
        self.content = self.si.Retrieve_Content()
        self.helper = Helper(self.ca)





        self.logger.info('Finished  __init__')

    def findVM(self):
        self.logger.info('Perform findVM')
        vm=None
        try:
            vm = self.helper.getVM(self.content, self.vm_name)
        except Exception as e:
            self.logger.error('Failed in findVM: '+str(e))
            vm = None
        return vm

        self.logger.info('Finished  findVM')

    def getSpec(self,vm,backwards = False):
        self.logger.info('Perform getSpec')
        spec = None
        try:
            if backwards:
                spec = self.helper.buildVmotionSpec(vm, self.src_host, self.src_datastore)
            else:
                spec = self.helper.buildVmotionSpec(vm, self.dest_host, self.dest_datastore)
        except Exception as e:
            self.logger.error('Failed in getSpec: '+str(e))
            spec = None
        return spec

        self.logger.info('Finished  getSpec')

    def relocateVM(self, vm, spec):
        self.logger.info('Perform relocateVM')
        task = None
        try:
            task = vm.RelocateVM_Task(spec)
        except Exception as e:
            self.logger.error('Failed in relocateVM: '+str(e))
            task = None
        return task

        self.logger.info('Finished  relocateVM')

    def testSetup(self):
        self.logger.info('Perform testSetup')
        self.loginToVc()

        self.logger.info('Finished  testSetup')

    def testTask(self):
        self.logger.info('Perform testTask')
        vm = self.findVM()
        spec = self.getSpec(vm)
        task = self.relocateVM(vm, spec)
        task_success = self.helper.monitorTask(task)
        assert (task_success), "Forward vMotion has failed."
        # Back to src
        vm = self.findVM()
        spec = self.getSpec(vm, backwards=True)
        task = self.relocateVM(vm, spec)
        task_success = self.helper.monitorTask(task)
        assert (task_success), "Backward vMotion has failed."

        return task_success



        self.logger.info('Finished  testTask')

    def testCleanup(self):
        self.logger.info('Perform testCleanup')
        self.dest_datastore = self.src_datastore
        self.dest_host = self.src_host
        vm = self.findVM()
        spec = self.getSpec()
        task = self.relocateVM(vm, spec)
        task_success = self.helper.monitorTask(task)
        return task_success

        pass
