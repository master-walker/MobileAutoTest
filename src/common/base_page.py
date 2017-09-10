#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Created on 2017年5月29日
操作页面元素的基类
'''

import os
import sys
import time
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.connectiontype import ConnectionType
from config.read_config import config

src_path = os.path.abspath('..')
sys.path.append(src_path)
reload(sys)

wait_time = float(config.waitTime)

success = "SUCCESS   "
fail = "FAIL   "


class BasePage(object):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    # 获取元素和元素信息，返回 数组
    def _get_elements(self, locators):
        logger = self.logger
        t1 = time.time()
        try:
            elements = []
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locators[:2]))
            if len(locators) == 3:
                elements_and_info = (element, locators[-1])
            elif len(locators) == 2:
                elements_and_info = (element, "")
            elements.append(elements_and_info)
            logger.info("{0} getElement {1}, Spend {2} seconds".format(success, locators[-1], time.time() - t1))
            return elements

        except (NoSuchElementException, TimeoutException):
            logger.info("{0} getElement {1}, Spend {2} seconds".format(fail, locators[-1], time.time() - t1))
            raise Exception

    # 根据locators获取一个元素，或多个元素
    def get_element_and_info(self, locators):
        logger = self.logger
        try:
            if isinstance(locators, tuple):
                elements = self._get_elements(locators)
                return elements

            elif isinstance(locators, list):
                elements = []
                for locate in locators:
                    elements.extend(self._get_elements(locate))
                return elements

        except TypeError:
            logger.debug(traceback.print_exc())
            return False

    # 仅获取元素
    def get_element(self, locator):
        if not isinstance(locator, list):
            element = (self.get_element_and_info(locator))[0]
            return element
        else:
            return False

    # 获取一组相同类型元素
    def get_group_elements(self, locate, waitTime=wait_time, num=None):
        driver = self.driver
        logger = self.logger
        t1 = time.time()
        try:
            groupElements = WebDriverWait(driver, waitTime).until(EC.presence_of_all_elements_located(locate))
            # 获取指定个数的元素
            elements = groupElements[:num]
            logger.info("{0} getElement {1}, Spend {2} seconds".format(success, groupElements[-1], time.time() - t1))
            return elements
        except TimeoutException:
            logger.info("{0} getElement {1}, Spend {2} seconds".format(fail, groupElements[0], time.time() - t1))
            return False

    # 输入数据并提交
    # 默认参数值应该是不可变的
    def submit(self, locators, datas, sleep_time=2):
        # 输入数据
        self.input(locators[:-1], datas)
        time.sleep(sleep_time)
        # 提交
        self.click(locators[-1])

    # 输入数据
    def input(self, locators, datas):
        t1 = time.time()
        logger = self.logger
        try:
            elements = self.get_element_and_info(locators)
            for index, element in enumerate(elements):
                if isinstance(datas, str) or isinstance(datas, unicode):
                    element[0].clear()
                    element[0].send_keys(datas)
                    logger.info("{0} input {1}, Spend {2} seconds".format(element[1], datas, time.time() - t1))
                elif isinstance(datas, list):
                    element[0].clear()
                    element[0].send_keys(datas[index])
                    logger.info("{0} input {1}, Spend {2} seconds".format(element[1], datas[index], time.time() - t1))
                else:
                    logger.debug("inputData传值异常")

        except IndexError:
            print traceback.print_exc()

    # 点击元素
    def click(self, locators, sleep_time=2):
        elements = self.get_element_and_info(locators)
        t1 = time.time()
        logger = self.logger
        try:
            for element in elements:
                element[0].click()
                logger.info("{0} click  Spend {1} seconds".format(element[1], time.time() - t1))
                time.sleep(sleep_time)
        except Exception:
            print traceback.print_exc()

    # 获取元素的文本值
    def get_element_text(self, locators):
        logger = self.logger
        t1 = time.time()
        try:
            text = [element[0].text for element in self.get_element_and_info(locators)]
            if len(text) is 1:
                return text[0]
                logger.info("get_element_text {0}  Spend {1} seconds".format(text[0], time.time() - t1))
            else:
                return text
                logger.info("get_element_text {0}  Spend {1} seconds".format(text[-1], time.time() - t1))
        except TypeError:
            print traceback.print_exc()

    # 检查单选框或复选框选中
    def is_selected(self, locators):
        element = self.get_element(locators)
        try:
            return element[0].is_selected()
        except Exception:
            print traceback.print_exc()

    # 检查元素是否可用
    def is_enabled(self, locators):
        element = self.get_element(locators)
        try:
            return element[0].is_enabled()
        except Exception:
            print traceback.print_exc()

    # 检查元素是否可见
    def is_displayed(self, locators):
        element = self.get_element(locators)
        try:
            return element[0].is_displayed()
        except Exception:
            print traceback.print_exc()

    # 屏幕左滑
    def swipe_to_left(self, width, height, duration=800):
        self.driver.swipe(width / 4 * 3, height / 2, width / 4, height / 2, duration)

    # 屏幕右滑
    def swipe_to_right(self, width, height, duration=800):
        self.driver.swipe(width / 4, height / 2, width / 4 * 3, height / 2, duration)

    # 屏幕下滑
    def swipe_to_down(self, width, height, duration=800):
        self.driver.swipe(width / 2, height / 4, width / 2, height / 4 * 3, duration)

    # 屏幕上滑
    def swipe_to_up(self, width, height, duration=800):
        self.driver.swipe(width / 2, height / 4 * 3, width / 2, height / 4, duration)

    # 模拟手指点击（最多五个手指），可设置按住时间长度（毫秒）
    def tap(self, positions, duration=None):
        self.driver.tap(positions, duration=duration)

    # 按住A点后快速滑动至B点
    def flick(self, start_x, start_y, end_x, end_y):
        self.driver.flick(start_x, start_y, end_x, end_y)

    # 安装应用
    def install_app(self, path):
        self.driver.install_app(path)

    # 检查应用是否安装
    def is_install_app(self, package_name):
        self.driver.is_app_installed(package_name)

    # 卸载应用
    def uninstall(self, package_name):
        self.driver.remove_app(package_name)

    # 启动应用
    def launch(self):
        self.driver.launch_app()
        self.logger.info("launch app")

    # 关闭应用
    def close_app(self):
        self.driver.close_app()
        self.logger.info("close app")

    # 重置应用
    def reset(self):
        self.driver.reset()

    # 把当前应用放到app后台
    def background(self, sleep_time):
        self.driver.background_app(sleep_time)
        self.logger.info("make app background {0} seconds".format(sleep_time))

    # 打开通知栏
    # 打开通知栏功能只有Android可用
    def open_notifications(self):
        self.driver.open_notifications()
        self.logger.info("open notification")

    # Api: 文件操作相关
    # 从设备拉出文件
    def pullFile(self, filePath):
        self.driver.pull_file(filePath)

    # 向设备推送文件
    def pushFile(self, path, data):
        self.driver.push_file(path, data.encode("base64"))

    # 截图
    def take_screen_shot(self, file_name='/%s.jpeg' % (time.strftime('%Y-%m-%d-%H-%M', time.localtime()))):
        screenshot_path = os.path.abspath('../report/screenshot')
        if os.path.exists(screenshot_path) is not True:
            os.mkdir(screenshot_path)
        file_path = screenshot_path + file_name
        self.driver.get_screenshot_as_file(file_path)
        self.logger.info("take screen shot in {0}".format(file_path))

    # Api: 屏幕、手势操作相关
    # 锁定屏幕
    def lock(self, lock_time):
        self.driver.lock(lock_time)
        self.logger.info("lock the device {0} seconds".format(lock_time))

    # 滑动屏幕
    # def swipe(self, height, width):
    #     self.driver.swipe(75, 500, 75, 0, 0.8)

    # 捏
    def pinch(self, locators):
        element = self.get_element_and_info(locators)
        self.driver.pinch(element)

    # 屏幕放大
    def zoom(self, locators):
        element = self.get_element_and_info(locators)
        self.driver.zoom(element)

    # 元素滚动
    def scroll(self, origin_ele, dest_ele):
        self.driver.scroll(origin_ele, dest_ele)

    # 键盘事件
    def keyevent(self, keyCode):
        self.driver.keyevent(keyCode)

    # 隐藏键盘,iOS使用key_name隐藏，安卓不使用参数
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        # android no parameter
        self.driver.hide_keyboard()

    # 等待指定的activity出现直到超时，interval为扫描间隔1秒
    def wait_cctivity(self, activity, timeout, interval=1):
        self.driver.wait_activity(activity, timeout)

    # 长按
    # long_press()
    # 短按
    # press()
    # 点击
    # tap()
    # 移动到
    # move_to()
    # 执行手势操作
    # perform()
    # 释放操作
    # release()
    # 等待
    # wait()

    # TouchAction:触摸操作
    # 录制小视频的时候，长按录制10s
    def touchActions(self, locator):
        element = self.getElementAndInfo(locator)
        action = TouchAction(self.driver)
        action.long_press(element, None, None, 10000).release().perform()

    # 摇晃设备
    def shake(self):
        self.driver.shake()

    # Api: 应用上下文
    # 列出所有的可用上下文
    def getContexts(self):
        return self.driver.contexts

    # 列出当前上下文
    def currentContext(self):
        return self.driver.current_context

    # 将上下 文切换到默认上
    def switchContext(self):
        self.driver.switch_to.context(None)

    # 应用的字符串
    # driver.app_strings
    # Api: Activity相关

    # 获得activity
    def get_activity(self):
        return self.driver.current_activity

    # 设置网络类型
    # Sets the network connection type. Android only.
    #     Possible values:
    #         Value (Alias)      | Data | Wifi | Airplane Mode
    #         -------------------------------------------------
    #         0 (None)           | 0    | 0    | 0
    #         1 (Airplane Mode)  | 0    | 0    | 1
    #         2 (Wifi only)      | 0    | 1    | 0
    #         4 (Data only)      | 1    | 0    | 0
    #         6 (All network on) | 1    | 1    | 0
    # These are available through the enumeration `appium.webdriver.ConnectionType`
    # 设置网络类型
    # :Args:
    #  - connectionType - a member of the enum appium.webdriver.ConnectionType
    def set_network(self, net_type):
        if (net_type == "airplane_mode"):
            self.driver.set_network_connection(ConnectionType.AIRPLANE_MODE)
        elif (net_type == "wifi_only"):
            self.driver.set_network_connection(ConnectionType.WIFI_ONLY)
        elif (net_type == "data_only"):
            self.driver.set_network_connection(ConnectionType.DATA_ONLY)
        else:
            self.driver.set_network_connection(ConnectionType.ALL_NETWORK_ON)
