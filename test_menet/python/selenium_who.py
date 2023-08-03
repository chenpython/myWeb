# import os, sys

# o_path = os.getcwd()  # 得到当前根目录
# sys.path.append(o_path)
# from menet.menet import common_tools

# 记录每个地址认证错误次数，超过 20 个地址失败大于 20 次，则视为网站出现故障（验证码无论如何无法通过，曾出现），并统计验证码成功率
# 页面出现滑块验证码时切换 IP

import time, os, random, re
from math import ceil

import requests

import selenium

from lxml.html import etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from ..common_tools import db, tools, proxy

mongo_client = db.mongo_client
mongo_collection = mongo_client['results_who_clinic']

redis_client = db.redis_client

captcha_instance = tools.captcha_instance
proxy_instance = proxy.Proxy()

from os import path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image


class LimitError(Exception):
    pass


class WHO:

    headers = {
        'Host': 'www.chictr.org.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.chictr.org.cn/searchproj.aspx',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }

    url_prefix = 'https://www.chictr.org.cn'

    home_page = "https://www.chictr.org.cn/searchproj.aspx"

    allowed_domains = ['www.chictr.org.cn']

    failure_page = None

    total_page = 6567

    def __init__(self, version) -> None:

        self.version = version

        self.laod_webdriver()

        self.url_batch = '{}:all_urls'.format(self.version)

        self.failed_detail_urls = '{}:failed_detail_urls'.format(self.version)

    @staticmethod
    def handle_distance(distance):
        """将直线距离转为缓慢的轨迹"""
        import random
        slow_distance = []
        while sum(slow_distance) <= distance:
            slow_distance.append(random.uniform(-2, 30))

        if sum(slow_distance) != distance:
            slow_distance.append(distance - sum(slow_distance))
        return slow_distance

    def move_to_gap(self):  # slider是要移动的滑块,tracks是要传入的移动轨迹

        wait = WebDriverWait(self.driver, 10)
        button = wait.until(EC.presence_of_element_located(
            (By.ID, 'nc_1_n1z')))

        button = self.driver.find_element('id', 'nc_1_n1z')

        print('滑块按钮的高度：{}，宽度：{}'.format(button.size['height'],
                                        button.size['width']))

        slider = self.driver.find_element('xpath',
                                          '//span[@class="nc-lang-cnt"]')

        print('滑块区域的高度：{}，宽度：{}'.format(slider.size['height'],
                                        slider.size['width']))

        ActionChains(self.driver).move_to_element(button).perform()

        time.sleep(0.5)

        tracks = self.handle_distance(slider.location['x'])

        ActionChains(self.driver).click_and_hold(button).perform()

        time.sleep(0.5)

        for track in tracks:
            ActionChains(self.driver,
                         duration=1).move_by_offset(xoffset=track,
                                                    yoffset=0).perform()

        time.sleep(2)

        # ActionChains(self.driver, duration=1000).drag_and_drop_by_offset(
        #     button, slider.size['width'],
        #     slider.size['height']).perform()  #  速度均匀，易被识别

    def laod_webdriver(self, need_proxy=True):

        chrome_options = webdriver.ChromeOptions()

        if need_proxy:

            payload = {
                'num': 1,  #  获取数量
                'type': 2,  # 数据格式（1TXT 2JSON 3html）
                'city': 0,  # 城市
                'yys': 0,  # 运营商(100026:联通 100017:电信)
                'port': 1,  # IP协议（1:HTTP 2:SOCK5 11:HTTPS ）
                'time': 2,  # 稳定时长：30 - 180 分钟
                'ts': 1,  # 是否显示IP过期时间（1显示 2不显示）
                'ys': 0,  #  是否显示IP运营商（1显示 0不显示）
                'cs': 1,  # 是否显示位置信息（1显示 0不显示）
                'lb': 1,  # 分隔符(1:\r\n 2:/br 3:\r 4:\n 5:\t 6 :自定义)
                'sb': 0,  # 自定义分隔符
                'pb': 45,  # 端口位数（4：4位；5：5位）
                'mr': 1,  # 去重选择（1、自动去重；2、单日去重；3、不去重）
                'regions': '',  # 全国混发地区
                'pro': ''  # 代表省份
            }

            # 极光长效ip
            self.cur_proxy = proxy_instance.get_one_ip(payload)  # 网站根据 IP 控制数据
            # 自建代理池
            # self.cur_proxy = proxy_instance.random_one_proxy()  # 网站根据 IP 控制数据

            chrome_options.add_argument('--proxy-server=http://{}'.format(
                self.cur_proxy))  # 添加代理
        else:
            self.cur_proxy = ''

        chrome_options.add_experimental_option(
            'excludeSwitches',
            ['enable-automation'])  # 开启开发者模式，避免被识别出为selenium
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
        chrome_options.add_argument('user-agent=' + ua)
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')  # 绕过浏览器指纹

        chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常

        chrome_options.add_argument(
            '--no-sandbox')  #解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000')  #指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  #谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  #隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

        # chrome_options.add_experimental_option("debuggerAddress",
        #                                        "127.0.0.1:9222")  # 绕过浏览器指纹检测，测试失败

        # chrome_options.add_argument(
        #     '--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # url = 'https://bot.sannysoft.com/'  # 检测浏览器是否为驱动地址，测试失败

        # self.driver = webdriver.Chrome(
        #     executable_path="/root/crawlab_workspace/chromedriver",
        #     chrome_options=chrome_options)

        # 隐藏浏览器指纹
        with open('./js/stealth.min.js') as f:
            js = f.read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                                    {"source": js})

        self.driver.maximize_window()

    def main(self):
        self.driver.get("https://www.chictr.org.cn/searchproj.aspx")

        while True:
            try:

                pre_url = self.driver.current_url

                # self.driver.implicitly_wait(10)

                cur_page = self.get_cur_page()

                self.driver.url_key = '{}:{}'.format(self.version, cur_page)

                print('开始翻页流程，url：{}'.format(self.driver.current_url))

                if self.failure_page:

                    if ceil(cur_page / 10) == ceil(self.failure_page /
                                                   10):  # 在同一页数栏
                        print(
                            '失败页数与当前页在同一栏，无需页数栏翻页，cur_page：{}，failure_page：{}'.
                            format(cur_page, self.failure_page))

                        next_page_elem = self.driver.find_elements(
                            'xpath', '//a[@onclick="serchPage({})"]'.format(
                                self.failure_page))
                        self.failure_page = None

                    elif ceil(cur_page / 10) < ceil(
                            self.failure_page / 10):  # 需要对页数栏进行翻页
                        print('失败页数大于11，需页数栏翻页，cur_page：{}，failure_page：{}'.
                              format(cur_page, self.failure_page))

                        if cur_page % 10 == 0:  # 页数栏进行翻页操作
                            next_page_elem = self.driver.find_elements(
                                'xpath', '//a[contains(text(), "下一页")]')
                            print(
                                '当前页数为页数栏最后一页，需要点击翻页，cur_page：{}，failure_page：{}'
                                .format(cur_page, failure_page))

                        else:  # 点击当前页数栏最后一页
                            next_page_elem = self.driver.find_elements(
                                'xpath',
                                '//a[@onclick="serchPage({})"]'.format(
                                    ceil(cur_page / 10) * 10))
                            print(
                                '当前页数不是页数栏最后一页，需要点击翻页，cur_page：{}，failure_page：{}'
                                .format(cur_page, self.failure_page))

                    else:
                        print('出现不合理情况，failure_page：{}，cur_page：{}'.format(
                            self.failure_page, cur_page))
                        break

                else:
                    print('没有失败页，继续后续步骤，cur_page：{}，failure_page：{}'.format(
                        cur_page, self.failure_page))
                    next_page_elem = self.driver.find_elements(
                        'xpath', '//a[contains(text(), "下一页")]')

                if not next_page_elem:

                    if re.search(r"滑动验证页面", self.driver.page_source):
                        print('{} 出现滑块'.format(self.driver.current_url))

                        retry_times = 1

                        while retry_times < 5:

                            print('{} 第 {} 次解决滑块验证码'.format(
                                self.driver.current_url, retry_times))

                            try:

                                self.move_to_gap()

                            except selenium.common.exceptions.NoSuchElementException as e:

                                time.sleep(3)
                                continue

                            if refresh_button := self.driver.find_element(
                                    'id', '`nc_1_refresh1`'):

                                print('{} 滑块校验失败'.format(
                                    self.driver.current_url))

                                retry_times += 1

                                # TODO: 优化，未通过则循环刷新通过

                                refresh_button.click()

                            else:
                                next_page_elem = self.driver.find_elements(
                                    'xpath', '//a[contains(text(), "下一页")]')
                                break

                        else:
                            print("{} 滑块验证失败 {} 次，停止尝试，退出程序".format(
                                self.driver.current_url, retry_times))
                            break

                    elif self.driver.find_elements("id", "ui-dialog-title-1"):
                        print('验证码验证失败，url：{}'.format(self.driver.current_url))

                        match = re.search(r'&page=(\d*)',
                                          self.driver.current_url).group(1)

                        self.failure_page = int(match)

                        self.driver.get(self.home_page)  # 返回首页

                        redis_client.hincrby(self.url_batch,
                                             self.driver.url_key,
                                             1)  # 记录不同页数验证码出错次数

                        if redis_client.hget(
                                self.url_batch, self.driver.url_key) and int(
                                    redis_client.hget(
                                        self.url_batch,
                                        self.driver.url_key).decode()) > 50:
                            print('{} 失败次数大于30次，切换IP重新抓取'.format(
                                self.driver.current_url))
                            self.laod_webdriver()

                        continue

                    elif cur_page == self.total_page:
                        print('已抓取完最后一页，结束')
                        redis_client.delete(self.url_batch)
                        break

                    else:
                        print('当前未找到下一页元素，重新尝试，cur_page：{}，failure_page：{}'.
                              format(cur_page, self.failure_page))

                        for i in range(1, 4):  # 下一页模块未加载出来
                            print("第 {} 次重新获取下一页，url：{}".format(
                                i, self.driver.current_url))

                            next_page_elem = self.driver.find_elements(
                                'xpath', '//a[contains(text(), "下一页")]')

                            time.sleep(1)

                            if next_page_elem:
                                continue

                        if not next_page_elem:
                            print('出现未知情况，url：{}'.format(
                                self.driver.current_url))
                            break

                elem = next_page_elem[0]
                elem.location_once_scrolled_into_view  # 翻到页数栏
                time.sleep(1)

                print('当前打开地址：{}'.format(pre_url))

                if not self.check_old_url():  # 不保存重复数据
                    # 多线程访问详情
                    print('{} 解析页面，保存数据'.format(self.driver.current_url))

                    self.extract_value()

                    redis_client.hset(self.url_batch, self.driver.url_key, 0)

                print('{} 点击翻页'.format(self.driver.current_url))

                elem.click()

                time.sleep(3)

                if self.driver.find_elements(
                        'xpath',
                        '//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all  ui-draggable ui-resizable"]'
                ):
                    print('{} 出现图片验证码'.format(self.driver.current_url))

                    self.verify_img_code()

            except selenium.common.exceptions.NoSuchElementException as e:
                print("页面异常，错误：{}，处理前地址：{}，处理后地址：{}".format(
                    e, pre_url, self.driver.current_url))
                self.driver.get(pre_url)
                time.sleep(1)

            except LimitError as e:
                print('访问 {} 达到最大限制次数，切换IP，所属页数：{}，error：{}'.format(
                    self.detail_url, self.driver.current_url, e))
                self.laod_webdriver()
                self.driver.refresh()

            except selenium.common.exceptions.WebDriverException as e:
                print('代理：{}异常，当前地址：{}，切换IP，error：{}'.format(
                    self.cur_proxy, self.driver.current_url, e))
                self.laod_webdriver()

            except Exception as e:
                print("页面出现未知问题，错误：{}，处理前地址：{}，当前地址：{}".format(
                    e, pre_url, self.driver.current_url))
                break

        self.driver.close()

    def verify_img_code(self):
        verify_code_img = self.driver.find_element(
            "id", "imgVerify").screenshot_as_png  # 由于验证码图片动态改变，因此需要截图

        verify_code = captcha_instance.captcha_handler_by_content(
            verify_code_img)

        input_zone = self.driver.find_element('name', 'txtVerifyCode')
        input_zone.send_keys(verify_code)
        time.sleep(1)

        submit = self.driver.find_element('id', 'btnSaveProRes')
        submit.click()

        time.sleep(3)

    def extract_value(self):
        print('开始解析检索页数据，url：{}'.format(self.driver.current_url))

        trs = self.driver.find_elements(
            "xpath", "//table[@class='table_list']/tbody//tr")

        for tr in trs[1:]:

            all_td = tr.find_elements("xpath", 'td')

            revisions_url = all_td[0].find_element('xpath',
                                                   'a').get_attribute('href')

            detail_url = all_td[2].find_element('xpath', 'p/a').get_attribute(
                'href')  # 详情页地址

            info = {
                'registration_number': all_td[1].text,  # 注册号
                'registered_topic': all_td[2].text,  # 注册题目
                'study_type': all_td[3].text,  # 研究类型
                'registration_date': all_td[4].text,  # 注册时间
                'detail_url': detail_url,
                'parent_url': self.driver.current_url,
                'revisions_url': revisions_url  # 历史版本地址
            }

            self.detail_url = detail_url

            # detail_info = self.parse_detail(detail_url, self.headers)

            # info['detail'] = detail_info
            info['version'] = self.version

            print('{} 抓取到的数据：\n{}'.format(self.driver.current_url, info))
            mongo_collection.insert_one(info)

    def parse_detail(self, url, headers):
        print('开始解析详情页数据，detail_url: {}，url：{}'.format(
            url, self.driver.current_url))
        while True:

            # proxies = {
            #     'http': 'http://{}'.format(self.cur_proxy),
            #     'https': 'http://{}'.format(self.cur_proxy),
            # }

            proxies = {
                'http': 'http://{}'.format(proxy_instance.random_one_proxy()),
                'https': 'http://{}'.format(proxy_instance.random_one_proxy()),
            }

            try:

                resp = requests.get(url, headers=headers, proxies=proxies)

                if '非常抱歉!您查看的项目的不存在或已超过当天最大查看次数' in resp.text:

                    if redis_client.hget(self.failed_detail_urls, url) and int(
                            redis_client.hget(self.failed_detail_urls,
                                              url).decode()) > 5:

                        print('{} 已经超过最大尝试次数'.format(url))
                        return {}

                    redis_client.hincrby(self.failed_detail_urls, url, 1)

                else:

                    break
                # raise LimitError('非常抱歉!您查看的项目的不存在或已超过当天最大查看次数')
            except Exception as e:
                redis_client.hincrby(self.failed_detail_urls, url, 1)
                print("解析页面请求失败\nerror：{}".format(e))
                return {}

        try:

            selector_new = etree.HTML(resp.text)

            registration_number = selector_new.xpath(
                '//td[contains(string(.), "Registration number")]/following-sibling::td'
            )[0].xpath('string(.)')

            date_of_last_refreshed_on = selector_new.xpath(
                '//td[contains(string(.), "Date of Last Refreshed on")]/following-sibling::td'
            )[0].xpath('string(.)')

            date_of_registration = selector_new.xpath(
                '//td[contains(string(.), "Date of Registration")]/following-sibling::td'
            )[0].xpath('string(.)')

            registration_status = selector_new.xpath(
                '//td[contains(string(.), "注册号状态")]/following-sibling::td'
            )[0].xpath('string(.)')

            public_title = selector_new.xpath(
                '//td[contains(string(.), "注册题目")]/following-sibling::td'
            )[0].xpath('string(.)')

            english_acronym = selector_new.xpath(
                '//td[contains(string(.), "注册题目简写")]/following-sibling::td'
            )[0].xpath('string(.)')

            scientific_title = selector_new.xpath(
                '//td[contains(string(.), "研究课题的正式科学名称")]/following-sibling::td'
            )[0].xpath('string(.)')

            study_subject_id = selector_new.xpath(
                '//td[contains(string(.), "研究课题代号(代码)")]/following-sibling::td'
            )[0].xpath('string(.)')

            other_register = selector_new.xpath(
                '//td[contains(string(.), "在二级注册机构或其它机构的注册号")]/following-sibling::td'
            )[0].xpath('string(.)')

            applicant = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader = selector_new.xpath(
                '//td[contains(string(.), "研究负责人")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_telephone = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人电话")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader_telephone = selector_new.xpath(
                '//td[contains(string(.), "研究负责人电话")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_fax = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人传真")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader_fax = selector_new.xpath(
                '//td[contains(string(.), "研究负责人传真")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_email = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人电子邮件")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_email = selector_new.xpath(
                '//td[contains(string(.), "研究负责人电子邮件")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_website = selector_new.xpath(
                '//td[contains(string(.), "申请单位网址(自愿提供)")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader_website = selector_new.xpath(
                '//td[contains(string(.), "研究负责人网址(自愿提供)")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_address = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人通讯地址")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader_address = selector_new.xpath(
                '//td[contains(string(.), "研究负责人通讯地址")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            applicant_postcode = selector_new.xpath(
                '//td[contains(string(.), "申请注册联系人邮政编码")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_leader_postcode = selector_new.xpath(
                '//td[contains(string(.), "研究负责人邮政编码")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            approved_by_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "是否获伦理委员会批准")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            approved_no_of_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会批件文号")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            name_of_the_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "批准本研究的伦理委员会名称")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            date_of_approved_by_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会批准日期")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            contact_name_of_the_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会联系人")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            contact_address_of_the_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会联系地址")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            contact_phone_of_the_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会联系人电话")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            contact_email_of_the_ethic_committee = selector_new.xpath(
                '//td[contains(string(.), "伦理委员会联系人邮箱")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            primary_sponsor = selector_new.xpath(
                '//td[contains(string(.), "研究实施负责（组长）单位")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            primary_sponsor_address = selector_new.xpath(
                '//td[contains(string(.), "研究实施负责（组长）单位地址")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            secondary_sponsor = {
                'country':
                selector_new.xpath(
                    '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//td[contains(string(.), "国家")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'institution_hospital':
                selector_new.xpath(
                    '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//td[contains(string(.), "单位(医院)")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'province':
                selector_new.xpath(
                    '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//td[contains(string(.), "省(直辖市)")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'address':
                selector_new.xpath(
                    '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//td[contains(string(.), "具体地址")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'city':
                selector_new.xpath(
                    '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//td[contains(string(.), "市(区县)")]/following-sibling::td[1]'
                )[0].xpath('string(.)')
            }

            source_of_funding = selector_new.xpath(
                '//td[contains(string(.), "经费或物资来源")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            target_disease = selector_new.xpath(
                '//td[contains(string(.), "研究疾病")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            target_disease_code = selector_new.xpath(
                '//td[contains(string(.), "研究疾病代码")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_type = selector_new.xpath(
                '//td[contains(string(.), "研究类型")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_phase = selector_new.xpath(
                '//td[contains(string(.), "研究所处阶段")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            objectives_of_study = selector_new.xpath(
                '//td[contains(string(.), "研究目的")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            description_for_medicine = selector_new.xpath(
                '//td[contains(string(.), "药物成份或治疗方案详述")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_design = selector_new.xpath(
                '//td[contains(string(.), "研究设计")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            inclusion_criteria = selector_new.xpath(
                '//td[contains(string(.), "纳入标准")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            exclusion_criteria = selector_new.xpath(
                '//td[contains(string(.), "排除标准")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            study_execute_time = selector_new.xpath(
                '//td[contains(string(.), "研究实施时间")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            recruiting_time = selector_new.xpath(
                '//td[contains(string(.), "征募观察对象时间")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            interventions = self.interventions(selector_new=selector_new)

            outcomes = self.outcomes(selector_new=selector_new)

            countries_of_recruitment = self.countries_of_recruitment(
                selector_new=selector_new)

            collecting_sample = selector_new.xpath(
                '//td[contains(string(.), "采集人体标本")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            recruiting_status = selector_new.xpath(
                '//td[contains(string(.), "征募研究对象情况")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            participant_age = {
                'min_age':
                selector_new.xpath(
                    '//td[contains(string(.), "年龄范围")]/following-sibling::td[1]//td[contains(string(.), "最小")]/following-sibling::td'
                )[0].xpath('string(.)'),
                'max_age':
                selector_new.xpath(
                    '//td[contains(string(.), "年龄范围")]/following-sibling::td[1]//td[contains(string(.), "最大")]/following-sibling::td'
                )[0].xpath('string(.)')
            }

            gender = selector_new.xpath(
                '//td[contains(string(.), "性别")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            randomization_procedure = selector_new.xpath(
                '//td[contains(string(.), "随机方法（请说明由何人用什么方法产生随机序列）")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            blinding = selector_new.xpath(
                '//td[contains(string(.), "盲法")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            ipd_sharing = selector_new.xpath(
                '//td[contains(string(.), "是否共享原始数据")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            the_way_of_sharing_ipd = selector_new.xpath(
                '//td[contains(string(.), "共享原始数据的方式")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            data_collection_and_management = selector_new.xpath(
                '//td[contains(string(.), "数据采集和管理（说明：数据采集和管理由两部分组成，一为病例记录表(Case Record Form, CRF)，二为电子采集和管理系统(Electronic Data Capture, EDC)，如ResMan即为一种基于互联网的EDC")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            data_and_safety_monitoring_committee = selector_new.xpath(
                '//td[contains(string(.), "数据与安全监察委员会")]/following-sibling::td[1]'
            )[0].xpath('string(.)')

            return {
                'registration_number':
                registration_number,
                'date_of_last_refreshed_on':
                date_of_last_refreshed_on,
                'date_of_registration':
                date_of_registration,
                'registration_status':
                registration_status,
                'public_title':
                public_title,
                'english_acronym':
                english_acronym,
                'scientific_title':
                scientific_title,
                'study_subject_id':
                study_subject_id,
                'other_register':
                other_register,
                'applicant':
                applicant,
                'study_leader':
                study_leader,
                'applicant_telephone':
                applicant_telephone,
                'study_leader_telephone':
                study_leader_telephone,
                'applicant_fax':
                applicant_fax,
                'study_leader_fax':
                study_leader_fax,
                'applicant_email':
                applicant_email,
                'study_email':
                study_email,
                'applicant_website':
                applicant_website,
                'study_leader_website':
                study_leader_website,
                'applicant_address':
                applicant_address,
                'study_leader_address':
                study_leader_address,
                'applicant_postcode':
                applicant_postcode,
                'study_leader_postcode':
                study_leader_postcode,
                'approved_by_ethic_committee':
                approved_by_ethic_committee,
                'approved_no_of_ethic_committee':
                approved_no_of_ethic_committee,
                'name_of_the_ethic_committee':
                name_of_the_ethic_committee,
                'date_of_approved_by_ethic_committee':
                date_of_approved_by_ethic_committee,
                'contact_name_of_the_ethic_committee':
                contact_name_of_the_ethic_committee,
                'contact_address_of_the_ethic_committee':
                contact_address_of_the_ethic_committee,
                'contact_phone_of_the_ethic_committee':
                contact_phone_of_the_ethic_committee,
                'contact_email_of_the_ethic_committee':
                contact_email_of_the_ethic_committee,
                'primary_sponsor':
                primary_sponsor,
                'primary_sponsor_address':
                primary_sponsor_address,
                'secondary_sponsor':
                secondary_sponsor,
                'source_of_funding':
                source_of_funding,
                'target_disease':
                target_disease,
                'target_disease_code':
                target_disease_code,
                'study_type':
                study_type,
                'study_phase':
                study_phase,
                'objectives_of_study':
                objectives_of_study,
                'description_for_medicine':
                description_for_medicine,
                'study_design':
                study_design,
                'inclusion_criteria':
                inclusion_criteria,
                'exclusion_criteria':
                exclusion_criteria,
                'study_execute_time':
                study_execute_time,
                'recruiting_time':
                recruiting_time,
                'interventions':
                interventions,
                'outcomes':
                outcomes,
                'countries_of_recruitment':
                countries_of_recruitment,
                'collecting_sample':
                collecting_sample,
                'recruiting_status':
                recruiting_status,
                'participant_age':
                participant_age,
                'gender':
                gender,
                'randomization_procedure':
                randomization_procedure,
                'blinding':
                blinding,
                'ipd_sharing':
                ipd_sharing,
                'the_way_of_sharing_ipd':
                the_way_of_sharing_ipd,
                'data_collection_and_management':
                data_collection_and_management,
                'data_and_safety_monitoring_committee':
                data_and_safety_monitoring_committee
            }

        except Exception as e:
            redis_client.hincrby(self.failed_detail_urls, url, 1)

            print("解析页面失败\nerror：{}\nresp.text：{}".format(e, resp.text))

            return {}

    def check_old_url(self):

        if redis_client.hexists(self.url_batch, self.driver.url_key):  # 多线程问题
            return True

        return False

    def get_cur_page(self):

        match = re.search(r'&page=(\d*)', self.driver.current_url)

        if match:

            cur_page = int(match.group(1))

        else:
            cur_page = 1

        return cur_page

    def interventions(self, selector_new):

        all_trs = selector_new.xpath(
            '//td[contains(string(.), "干预措施")]/following-sibling::td[1]//tr')

        results = []

        group = len(all_trs) // 4

        groups = [i * 4 for i in range(1, group + 1)]

        for index in groups:

            results.append({
                'group':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "组别")]/following-sibling::td[1]')
                [0].xpath('string(.)'),
                'sample_size':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "样本量")]/following-sibling::td[1]')
                [0].xpath('string(.)'),
                'intervention':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "干预措施")]/following-sibling::td[1]')
                [0].xpath('string(.)'),
                'intervention_code':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "干预措施代码")]/following-sibling::td[1]'
                )[0].xpath('string(.)')
            })

        return results

    def outcomes(self, selector_new):

        all_trs = selector_new.xpath(
            '//td[contains(string(.), "测量指标")]/following-sibling::td[1]//tr')

        results = []

        group = len(all_trs) // 4

        groups = [i * 4 for i in range(1, group + 1)]

        for index in groups:

            results.append({
                'outcome':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "指标中文名")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'type':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "指标类型")]/following-sibling::td[1]')
                [0].xpath('string(.)'),
                'measure_time_point_of_outcome':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "测量时间点")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'measure_method':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "测量方法")]/following-sibling::td[1]')
                [0].xpath('string(.)')
            })

        return results

    def countries_of_recruitment(self, selector_new):
        all_trs = selector_new.xpath(
            '//td[contains(string(.), "研究实施地点")]/following-sibling::td[1]//tr')

        results = []

        group = len(all_trs) // 4

        groups = [i * 4 for i in range(1, group + 1)]

        for index in groups:

            results.append({
                'country':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "国家")]/following-sibling::td[1]')
                [0].xpath('string(.)'),
                'province':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "省(直辖市)")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'city':
                all_trs[index - 4].xpath(
                    'td[contains(string(.), "市(区县)")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'institution_hospital':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "单位(医院)")]/following-sibling::td[1]'
                )[0].xpath('string(.)'),
                'level_of_the_institution':
                all_trs[index - 2].xpath(
                    'td[contains(string(.), "单位级别")]/following-sibling::td[1]')
                [0].xpath('string(.)')
            })

        return results
