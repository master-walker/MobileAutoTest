#!/usr/bin/python
#coding=utf8
'''
Created on 2011-8-3
@author: jxh
Description:

'''
import paramiko

class remotehost():
    def __init__(self,hostname,port,username,password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        #paramiko.util.log_to_file('paramiko.log')
        self.host = paramiko.SSHClient()
        #s.load_system_host_keys()
        self.host.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host.connect(hostname=hostname,port=int(port),username=username,password=password)
    def exec_command(self,command):
        stdin,stdout,stderr=self.host.exec_command(str(command))
        return stdout.read(),stderr.read()
    def close(self):
        self.host.close()