#!/usr/bin/env python
# coding=utf8
'''
Created on 2011-9-26
@author: lc
Description:

'''
import ConfigParser
import sys, os

src_path = os.path.abspath('..')
sys.path.append(src_path)
reload(sys)


class Config(object):
    def __init__(self, path=r'../config/config.ini'):
        configParser = ConfigParser.ConfigParser()
        configParser.read(path)

        # desired_caps数据
        self.platformName = configParser.get("desired_caps", "platformName")
        self.platformVersion = configParser.get("desired_caps", "platformVersion")
        self.deviceName = configParser.get("desired_caps", "deviceName")
        self.appPackage = configParser.get("desired_caps", "appPackage")
        self.appActivity = configParser.get("desired_caps", "appActivity")
        self.command_executor = configParser.get("desired_caps", "command_executor")

        # loginData
        self.username = configParser.get("login_data", "username")
        self.password = configParser.get("login_data", "password")

        # wait element load time
        self.waitTime = configParser.get("conf", "waitTime")

        # mysql数据库
        #         self.db_host=config.get("rzxdb","db_host")
        #         self.db_port=config.get("rzxdb","db_port")
        #         self.db_user=config.get("rzxdb","db_user")
        #         self.db_passwd=config.get("rzxdb","db_passwd")
        #         self.db_name=config.get("rzxdb","db_name")
        #         self.db_charset=config.get("rzxdb","db_charset")



        #         self.sel_host = config.get("selenium","sel_host")
        #         self.sel_port = config.get("selenium","sel_port")
        #         self.sel_browser = config.get("selenium","sel_browser")
        #         self.sel_domain = config.get("selenium","sel_domain")

        # 输入数据的json文件路径


# self.json_data_path=config.get("datapath","json_data_path")



if __name__ != "__main__":
    config_path = os.path.abspath('../config/config.ini')
    print config_path
    config = Config()
