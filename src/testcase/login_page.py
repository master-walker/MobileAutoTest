#!/usr/bin/env python
# coding=utf-8

'''
Created on 2017年8月30日

登录页面
'''
import time
from common import base_page
from config.read_config import config
from element.elements import LoginPageLocators


class LoginPage(base_page.BasePage):
    # 登录方法
    def login(self, login_data=[config.username, config.password]):
        start_time = time.time()
        self.logger.info("---------------------------------------------------------------------------")
        # 提交数据，登录
        self.submit(LoginPageLocators.loginElements, login_data)
        self.logger.info("login in  Spend {0} seconds".format(time.time() - start_time))
