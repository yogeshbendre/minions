# This is a sample test.
# All the parameters are to be passed as environment variables.
# Then use them with os.getenv("<param_name>")


from vcst.ConnectAnchor import ConnectAnchor
from vcst.helper import Helper
import os

class Test:

    def __init__(self):
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





    def findVM(self):
        vm=None
        try:
            vm = self.helper.getVM(self.content, self.vm_name)
        except Exception as e:
            vm = None
        return vm

    def getSpec(self,vm,backwards = False):
        spec = None
        try:
            if backwards:
                spec = self.helper.buildVmotionSpec(vm, self.src_host, self.src_datastore)
            else:
                spec = self.helper.buildVmotionSpec(vm, self.dest_host, self.dest_datastore)
        except Exception as e:
            spec = None
        return spec

    def relocateVM(self, vm, spec):
        task = None
        try:
            task = vm.RelocateVM_Task(spec)
        except Exception as e:
            task = None
        return task

    def testSetup(self):
        self.loginToVc()

    def testTask(self):
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



    def testCleanup(self):
        self.dest_datastore = self.src_datastore
        self.dest_host = self.src_host
        vm = self.findVM()
        spec = self.getSpec()
        task = self.relocateVM(vm, spec)
        task_success = self.helper.monitorTask(task)
        return task_success

        pass
