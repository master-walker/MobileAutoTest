#!/usr/bin/env python
# coding=utf-8

'''
Created on 2017年5月30日

页面常用的公共方法
'''
import time
from common import base_page
from config.read_config import config
from element.elements import LoginPage


class CommonPage(base_page.BasePage):
    # 登录方法
    def login(self, datas=[config.username, config.password]):
        t1 = time.time()
        logger = self.logger
        logger.info("\n---------------------------------------------------------------------------")
        # 提交数据，登录
        self.submit(LoginPage.loginElements, datas)
        logger.info("enter loginPage  Spend {0} seconds".format(time.time() - t1))


