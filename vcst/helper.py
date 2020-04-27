
from vcst.ConnectAnchor import ConnectAnchor
import atexit
from pyVmomi import vim, vmodl
import logging.config
import time

class Helper:

    def __init__(self,ca):
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('vcst.helper.Helper')
        self.ca = ca

    def getDatastore(self, obj_name, disp=False):
        return self.getObject(obj_name, [vim.Datastore], disp)

    def getVM(self, obj_name, disp=False):
        return self.getObject(obj_name, [vim.VirtualMachine], disp)

    def getHost(self, obj_name, disp=False):
        return self.getObject(obj_name, [vim.HostSystem], disp)

    def getObject(self,obj_name,vimtype,disp=False):
        """
         Internal method to create objects of various vCenter related classes
         :param content:
         :param vimtype:
         :param name:
         :return: Object
         """
        self.logger.info("Performing getObj")
        self.logger.info("Searching object: "+str(obj_name))
        obj = None
        content  = self.ca.getContent()
        container = content.viewManager.CreateContainerView(content.rootFolder,vimtype,True)
        for c in container.view:
            if disp:
                self.logger.info("c.name:" + str(c.name))
            if c.name == obj_name:
                obj = c
                break
        self.logger.info("Finished getObject")
        return obj

    def collect_template_disks(self,vm):
        """
            Internal method to collect template disks
            :param vm: VM object
            :return: list of template disks
        """
        template_disks = []
        for device in vm.config.hardware.device:
            if type(device).__name__ == "vim.vm.device.VirtualDisk":
                datastore = device.backing.datastore
                print("device.deviceInfo.summary:" + device.deviceInfo.summary)
                print("datastore.summary.type:" + datastore.summary.type)
                if hasattr(device.backing, 'fileName'):
                    disk_desc = str(device.backing.fileName)
                    print("Disc Discription -- {}".format(disk_desc))
                    drive = disk_desc.split("]")[0].replace("[", "")
                    print("drive:" + drive)
                    print("device.backing.fileName:" + device.backing.fileName)
                    template_disks.append(device)
        return template_disks

    def construct_locator(self, template_disks, datastore_dest_id):
        """
            Internal method to construct locator for the disks
            :param template_disks: list of template_disks
            :param datastore_dest_id: ID of destination datastore
            :return: locator
        """
        ds_disk = []
        for index, wdisk in enumerate(template_disks):
            print("relocate index:" + str(index))
            print("disk:" + str(wdisk))
            disk_desc = str(wdisk.backing.fileName)
            drive = disk_desc.split("]")[0].replace("[", "")
            print("drive:" + drive)
            print("wdisk.backing.fileName:" + wdisk.backing.fileName)
            locator = vim.vm.RelocateSpec.DiskLocator()
            locator.diskBackingInfo = wdisk.backing
            locator.diskId = int(wdisk.key)
            locator.datastore = datastore_dest_id
            ds_disk.append(locator)
        return ds_disk

    def buildVmotionSpec(self,vm,dest_host,dest_datastore):
        spec = vim.VirtualMachineRelocateSpec()
        destination_host = self.getHost(dest_host)
        destination_ds = self.getDatastore(dest_datastore)
        spec.host = destination_host
        spec.pool = destination_host.parent.resourcePool
        spec.datastore = destination_ds
        template_disks = self.collect_template_disks(vm)
        spec.disk = self.construct_locator(template_disks,destination_ds)
        return spec

    def monitorTask(self, task):
        task_success = False
        try:
            while True:
                self.logger.info("Task Status: "+str(task.info.state))
                if task.info.state != vim.TaskInfo.State.running:
                    break
                time.sleep(5)
            task_success = True
        except Exception as e:
            task_success = False
        return task_success










