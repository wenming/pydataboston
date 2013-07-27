import os
import pprint
import time
import datetime
import threading

from azure import *
from azure.servicemanagement import *

import configSample as config

class CreateVM:
    lock = threading.Lock()

    def __init__(self, service_name = config.service_name, deployment_name = config.deployment_name, role_name = config.role_name, affinity_group = config.affinity_group):
        self.subscription_id = config.subscription_id
        self.pem_path = config.pem_path
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.location = config.location
        self.media_name = config.media_name
        self.media_link_base = config.media_link_base
        self.computer_name = config.computer_name
        self.username = config.username
        self.password = config.password
        self.endpoint = config.endpoint
        self.role_size = config.role_size
        self.affinity_group = affinity_group
        self.endpoint_list = config.endpoint_list
        self.SERVICE_CERT_THUMBPRINT = config.SERVICE_CERT_THUMBPRINT
        self.SERVICE_CERT_DATA = config.SERVICE_CERT_DATA
        self.SERVICE_CERT_FORMAT = config.SERVICE_CERT_FORMAT
        self.SERVICE_CERT_PASSWORD = config.SERVICE_CERT_PASSWORD

        self.sms = ServiceManagementService(self.subscription_id, self.pem_path)
        # configure
        self.linux_config = LinuxConfigurationSet(self.computer_name, self.username, self.password, False)
        self.pk = PublicKey(self.SERVICE_CERT_THUMBPRINT, u'/home/%s/.ssh/authorized_keys' %(self.username))
        self.pair = KeyPair(self.SERVICE_CERT_THUMBPRINT, u'/home/%s/.ssh/id_rsa' %(self.username))
        self.linux_config.ssh.public_keys.public_keys.append(self.pk)
        self.linux_config.ssh.key_pairs.key_pairs.append(self.pair)
        self.os_hd = OSVirtualHardDisk(self.media_name, self.media_link_base + self.role_name + str(datetime.now()))
        # network
        self.network = ConfigurationSet()
        self.network.configuration_set_type = 'NetworkConfiguration'
        for endpoint in self.endpoint_list:
            self.network.input_endpoints.input_endpoints.append(ConfigurationSetInputEndpoint(endpoint[0], endpoint[1], endpoint[2], endpoint[3]))

    def createVM(self):
        self.create_host_service()
        self.create_virtual_machine()
        # start role 
        self.sms.start_role(self.service_name, self.deployment_name, self.role_name)
        self._wait_for_role_instance_status(self.service_name, self.deployment_name, self.role_name, 'ReadyRole')

    def create_host_service(self):
        if CreateVM.lock.acquire():
            try:
                if not self._hosted_service_exists(self.service_name):
                    if self.affinity_group:
                        self.sms.create_hosted_service(service_name = self.service_name, label = self.service_name, affinity_group = self.affinity_group)
                    else:
                        self.sms.create_hosted_service(service_name = self.service_name, label = self.service_name, location = self.location)
                    self._create_service_certificate(self.service_name, self.SERVICE_CERT_DATA, self.SERVICE_CERT_FORMAT, self.SERVICE_CERT_PASSWORD)
                else:
                    print "Host service has existed"
            except Exception as e:
                print e
            finally:
                CreateVM.lock.release()

    def create_virtual_machine(self):
        if CreateVM.lock.acquire():
            try:
                result = self.sms.create_virtual_machine_deployment(
                        service_name = self.service_name,
                        deployment_name = self.deployment_name,
                        deployment_slot = 'production',
                        label = self.role_name,
                        role_name = self.role_name,
                        system_config = self.linux_config,
                        os_virtual_hard_disk = self.os_hd,
                        network_config = self.network,
                        role_size = self.role_size)

                print result.request_id
                self._wait_for_async(result.request_id)
                self._wait_for_deployment_status(self.service_name, self.deployment_name, 'Running')
            finally:
                CreateVM.lock.release()

    # delete
    def deleteVM(self): 
        try:
            self.sms.delete_deployment(self.service_name, self.deployment_name)
        except Exception as e:
            print e
        while self._deployment_exists(self.service_name, self.deployment_name):
            print "Try delete deployment ..."
        print 'delete_deployment'

        try:
            result = self.sms.delete_role(self.service_name, self.deployment_name, self.role_name)
            self._wait_for_async(result.request_id)
        except Exception as e:
            print e
        print 'delete_role'

        if CreateVM.lock.acquire():
            while self._hosted_service_exists(self.service_name):
                try:
                    self.sms.delete_hosted_service(self.service_name)
                    break
                except Exception as e:
                    print e
                    time.sleep(5)
            CreateVM.lock.release()
        while self._hosted_service_exists(self.service_name):
            print "Try delete hosted_service ..."
        print 'delete_hosted_service'


    # Helper function
    def printFile(self, path):
        f  = file(path)
        s = ""
        l = []
        while True:
            line = f.readline()
            if not line:
                break
            l.append(line)
            s = ''.join(l)
        print s

    def _wait_for_async(self, request_id):
        result = self.sms.get_operation_status(request_id)
        while result.status == 'InProgress':
            print result.status + "\t" + self.role_name
            time.sleep(2)
            result = self.sms.get_operation_status(request_id)
        print result.status + "\t" + self.role_name

    def _wait_for_deployment_status(self, service_name, deployment_name, status):
        props = self.sms.get_deployment_by_name(service_name, deployment_name)
        print props.status
        while props.status != status:
            print props.status
            time.sleep(5)
            props = self.sms.get_deployment_by_name(service_name, deployment_name)
        print "Succeed in %s" %status

    def _get_role_instance_status(self, deployment, role_instance_name):
        for role_instance in deployment.role_instance_list:
            if role_instance.instance_name == role_instance_name:
                return role_instance.instance_status
        return None

    def _wait_for_role_instance_status(self, service_name, deployment_name, role_instance_name, status):
        props = self.sms.get_deployment_by_name(service_name, deployment_name)
        while True:
            p = self._get_role_instance_status(props, role_instance_name)
            if p == status:
                break
            print p + "\t" + role_instance_name
            time.sleep(5)
            props = self.sms.get_deployment_by_name(service_name, deployment_name)

    def _deployment_exists(self, service_name, deployment_name):
            try:
                props = self.sms.get_deployment_by_name(service_name, deployment_name)
                return props is not None
            except:
                return False


    def _hosted_service_exists(self, name):
        try:
            props = self.sms.get_hosted_service_properties(name)
            return props is not None
        except:
            return False

    def _create_service_certificate(self, service_name, data, format, password):
        result = self.sms.add_service_certificate(service_name, data, format, password)
        self._wait_for_async(result.request_id)

if __name__ == "__main__":
    createVMInstance = CreateVM()
    if sys.argv[1] == "create":
        createVMInstance.createVM()
    elif sys.argv[1] == "delete":
        createVMInstance.deleteVM()
    else:
        print "Error input"
