import sys
import creatVM as createVM
import ssh as ssh_deploy
import createMultiVM as MultiVM
import installMultiSoftware as installMultiSoftware

if __name__ == "__main__":
    create_multi_vm_instance = MultiVM.MultiVM()
    install_multi_SW_instance = installMultiSoftware.MultiInstallSW()
    sshdeploy = ssh_deploy.SSHDeploy()
    if sys.argv[1] == "create":
        create_multi_vm_instance.create_multi_vm()
    elif sys.argv[1] == "delete":
        create_multi_vm_instance.delete_multi_vm()
    elif sys.argv[1] == "deploy":
        install_multi_SW_instance.install_multi_sw()
        sshdeploy.deploy_ipython_cluster()
    elif sys.argv[1] == "start":
        create_multi_vm_instance.create_multi_vm()
        install_multi_SW_instance.install_multi_sw()
        sshdeploy.deploy_ipython_cluster()
    else:
        print "Error input"

#if __name__ == "__main__":
#    if sys.argv[1] == "create":
#        createVM_instance = createVM.CreateVM()
#        createVM_instance.createVM()
#    elif sys.argv[1] == "delete":
#        createVM_instance = createVM.CreateVM()
#        createVM_instance.deleteVM()
#    elif sys.argv[1] == "ssh":
#        ssh_deploy_instance = ssh_deploy.SSHDeploy()
#        ssh_deploy_instance.deploy_ipython()
#    elif sys.argv[1] == "start":
#        createVM_instance = createVM.CreateVM()
#        ssh_deploy_instance = ssh_deploy.SSHDeploy()
#        createVM_instance.createVM()
#        ssh_deploy_instance.deploy_ipython()
#    else:
#        print "Error input"
