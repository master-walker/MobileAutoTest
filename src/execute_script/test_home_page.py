#!/usr/bin/env python
# coding=utf-8
'''
Created on 2017年5月23日

@author: Master SkyWalker

启动模拟器，打开terminal
输入：
adb connect 127.0.0.1:62001
查看adb连接设备
adb devices

启动appium（关联模拟器）
adb
appium -a 127.0.0.1 -p 4723 -U 127.0.0.1:62001 --no-reset
'''

import unittest
from testcase import home_page, login_page
from common import my_test


class TestHomePage(my_test.MyTest):
    def testCase(self):
        driver = self.driver
        logger = self.logger
        home_pg = home_page.HomePage(driver, logger)
        login_pg = login_page.LoginPage(driver, logger)

        # 登录
        login_pg.login()
        # 滑动
        home_pg.swipe_test()
        # 发帖
        home_pg.posted()
        # 测试方法
        home_pg.test_all()


if __name__ == "__main__":
    unittest.main()
