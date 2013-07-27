import paramiko
import configSample as config

class InstallSW:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.commandList()

    def run(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, 22, self.username, self.password)
        self.exec_command_list_switch(self.command_list)
        self.ssh.close()

    def commandList(self):
        self.command_list = [
                "sudo -S apt-get update",
                "sudo -S apt-get -y install git",
                "git clone https://github.com/ipython/ipython.git",
                "cd ipython\n echo %s | sudo -S python setup.py install" %self.password,
                "sudo -S apt-get -y install python-setuptools",
                "sudo -S easy_install tornado",
                "sudo -S apt-get -y install python-zmq",
                "sudo -S easy_install Jinja2",
                "sudo -S apt-get -y install python-matplotlib python-numpy python-scipy",
                "pkill -f ipcontroller",
                "pkill -f ipython"
                ]

    def exec_command_list_switch(self, command_list):
        for command in command_list:
            if command.startswith("sudo -S"):
                self.exec_command_sudo(command)
            else:
                self.exec_command(command)

    def exec_command_list(self, command_list, func):
        for command in command_list:
            func(command)

    def exec_command_sudo(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(("echo %s | " + command) %self.password)
            str_return = stdout.readlines()
            print "OK..........\t" + self.hostname + "\t" + command
            return str_return
        except Exception as e:
            print e

    def exec_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            str_return = stdout.readlines()
            print "OK..........\t" + self.hostname + "\t" + command
            return str_return
        except Exception as e:
            print e

    def exec_multi_command(self, command, next_command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            stdin.write(next_command)
            stdin.flush()
        except Exception as e:
            print e
