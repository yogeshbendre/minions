# Author: ybendre, jijumonv, jparappurath
# Test: tmc_handler
# This is WCP Helper Class

import paramiko
import sys
import time
import json


class WCPFetcher:

    def __init__(self, vc, username = "root", password = "Admin!23"):
        self.vc = vc
        self.username = username
        self.password = password
        self.wcp_info = None
        self.get_wcp_info()



    def run_command_on_wcp(self, wcp_id, cmd):
        print("Running Command: ")
        print(cmd)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.wcp_info[wcp_id]["IP"], username="root", password=self.wcp_info[wcp_id]["PWD"])
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        time.sleep(1)
        try:
            myout = stdout.readlines()
            for l in myout:
                print(l)
            return myout
        except Exception as e:
            print("Something went wrong: "+str(e))
            return None

    def run_command_on_each_master(self, wcp_id, cmd, numMasters=3):
        print("No. of masters: "+str(numMasters))
        base_ip = self.wcp_info[wcp_id]["IP"]
        lastField = int(base_ip.split(".")[-1])
        for i in range(lastField+1, lastField+4):
            myip = base_ip.replace(str(lastField), str(i))
            print("Master IP: "+str(myip))
            print("Running Command: ")
            print(cmd)
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=myip, username="root", password=self.wcp_info[wcp_id]["PWD"])
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            time.sleep(1)
            try:
                myout = stdout.readlines()
                for l in myout:
                    print(l)
                #return myout
            except Exception as e:
                print("Something went wrong: "+str(e))
                #return None

        print("Completed")


    def get_wcp_info(self):
        ssh_client =paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.vc, username=self.username, password=self.password)
        stdin, stdout, stderr = ssh_client.exec_command('curl -k -X GET "https://10.199.56.1/LI/decrypt_json.py" -o /root/decrypt_json.py')
        time.sleep(1)
        stdin, stdout, stderr = ssh_client.exec_command("python3 /root/decrypt_json.py")
        time.sleep(1)
        ssh_client.close()
        try:
            myout = stdout.readlines()
            myout = myout[0].replace("\n", "").replace("'","\"")
            myout = json.loads(myout)
            print(myout)
            self.wcp_info = myout
            return myout
        except Exception as e:
            print("Something wrong")
            return None
