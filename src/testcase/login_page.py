#!/usr/bin/env python
# coding=utf-8

'''
Created on 2017年8月30日

登录页面
'''
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
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

    # 获取错误提示
    def get_toast(self):
        els = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(LoginPageLocators.toast_element))

        if self.get_element(els):#LoginPageLocators.toast_element

            self.logger.info("get toast element")
        else:
            self.logger.info("Fail")
