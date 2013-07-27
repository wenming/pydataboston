import os
import pprint
import time
import datetime
import workerpool

from azure import *
from azure.servicemanagement import *
from creatVM import *

import configSample as config

class CreateVMJob(workerpool.Job):
    def __init__(self, service_name, deployment_name, role_name):
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.createVM_instance = CreateVM(service_name = self.service_name, deployment_name = self.deployment_name, role_name = self.role_name)
    
    def run(self):
        self.createVM_instance.createVM()

class DeleteVMJob(workerpool.Job):
    def __init__(self, service_name, deployment_name, role_name):
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.createVM_instance = CreateVM(service_name = self.service_name, deployment_name = self.deployment_name, role_name = self.role_name)
    
    def run(self):
        self.createVM_instance.deleteVM()

class MultiVM:
    def __init__(self):
        self.base_service_name = config.service_name
        self.base_deployment_name = config.deployment_name
        self.base_role_name = config.role_name
        self.workerpool_size = config.workerpool_size
        self.num_vm = config.num_vm

    def create_multi_vm(self):
        pool = workerpool.WorkerPool(size = self.workerpool_size)
        for num in range(self.num_vm):
            service_name = self.base_role_name + str(num)
            deployment_name = self.base_deployment_name + str(num)
            role_name = self.base_role_name + str(num)
            job = CreateVMJob(service_name, deployment_name, role_name)
            pool.put(job)
        pool.shutdown()
        pool.wait()

    def delete_multi_vm(self):
        pool = workerpool.WorkerPool(size = self.workerpool_size)
        for num in range(self.num_vm):
            service_name = self.base_role_name + str(num)
            deployment_name = self.base_deployment_name + str(num)
            role_name = self.base_role_name + str(num)
            job = DeleteVMJob(service_name, deployment_name, role_name)
            pool.put(job)
        pool.shutdown()
        pool.wait()

if __name__ == "__main__":
    create_multi_vm_instance = MultiVM()
    if sys.argv[1] == "create":
        create_multi_vm_instance.create_multi_vm()
    elif sys.argv[1] == "delete":
        create_multi_vm_instance.delete_multi_vm()
    else:
        print "Error input"
