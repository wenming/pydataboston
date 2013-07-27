import workerpool
from installSoftware import * 

class installSWJob(workerpool.Job):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.installSW_instance = InstallSW(self.hostname, self.username, self.password)

    def run(self):
        self.installSW_instance.run()

class MultiInstallSW:
    def __init__(self):
        self.base_role_name = config.role_name
        self.username = config.username
        self.password = config.password
        self.workerpool_size = config.workerpool_size
        self.num_vm = config.num_vm

    def install_multi_sw(self):
        pool = workerpool.WorkerPool(size = self.workerpool_size)
        for num in range(self.num_vm):
            self.hostname = self.base_role_name + str(num) + ".cloudapp.net"
            job = InstallSW(self.hostname, self.username, self.password)
            pool.put(job)
        pool.shutdown()
        pool.wait()

if __name__ == "__main__":
    install_multi_SW_instance = MultiInstallSW()
    install_multi_SW_instance.install_multi_sw()
