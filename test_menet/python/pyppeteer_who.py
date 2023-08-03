import asyncio, time, re, json, random
from math import ceil
from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests
from lxml.html import etree

from ..common_tools import db, tools, proxy

mongo_client = db.mongo_client
mongo_collection = mongo_client['results_who_clinic']

redis_client = db.redis_client

captcha_instance = tools.captcha_instance
proxy_instance = proxy.Proxy()


class LimitError(Exception):
    pass


class ECCError(Exception):
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

    async def move_to_gap(self, page):
        # slider是要移动的滑块,tracks是要传入的移动轨迹

        # 模拟鼠标滑动
        await page.hover('#nc_1_n1z')

        await page.mouse.down()

        slider = await page.querySelector('.nc-lang-cnt')

        position = await slider.boundingBox()

        track = self.handle_distance(position['x'])

        for dis in track:
            await page.mouse.move(page.mouse._x + dis, page.mouse._y, {
                'delay': random.randint(500, 1000),
                'steps': 3
            })

        await page.mouse.up()

    async def open_page(self, browser, url):

        page = await browser.newPage()
        # 设置页面参数
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/104.0.0.0 Safari/537.36')
        await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面大小
        await page.evaluateOnNewDocument(
            '() =>{ Object.defineProperties(navigator,'
            '{ webdriver:{ get: () => false } }) }')  # 去掉驱动检测

        await page.setJavaScriptEnabled(enabled=True)
        # 防止页面识别出脚本(反爬虫关键语句)
        await stealth(page)

        await page.goto(url)

        # html = await page.content()

        # if re.search(r"滑动验证页面", html):
        #     self.move_to_gap()

        # page.xpath('//a[@id="moreOption"]')

        return page

    def get_cur_page(self, url):

        match = re.search(r'&page=(\d*)', url)

        if match:

            cur_page = int(match.group(1))

        else:
            cur_page = 1

        return cur_page

    async def init_browser(self, proxy):

        # 初始化浏览器配置
        options = {
            'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            'args': [
                "--start-maximized", "--window-size=1920,1080",
                '--disable-infobars', f'--proxy-server={proxy}'
            ]  # 设置浏览器外观
        }

        browser = await launch(headless=False,
                               options=options,
                               executablePath='/usr/bin/google-chrome-stable')

        return browser

    def img_code(self):
        img_time = random.random()

        img_url = f'https://www.chictr.org.cn/Tools/verifyimagepage.aspx?textcolor=2&bgcolor=F4F4F4&ut=1&time={img_time}'

        verifycode = tools.captcha_instance.captcha_handler_by_url(
            img_url, self.headers)

        return verifycode

    def refresh_proxy(self):

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
        self.proxy = proxy_instance.get_one_ip(payload)  # 网站根据 IP 控制数据

        self.ip_key = json.dumps(payload)

    def crawl_main(self, cur_page):

        self.refresh_proxy()

        proxies = {
            'http': 'http://{}'.format(self.proxy),
            'https': 'http://{}'.format(self.proxy),
        }

        next_page_url_template = 'https://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode={}&page={}'

        while True:
            if cur_page == 1:
                cur_url = self.home_page
            elif cur_page > 3:  # 从第3页开始均需要携带验证码参数
                try:
                    verifycode = self.img_code()
                    if not verifycode or len(verifycode) != 5:
                        raise ECCError("图片验证码识别失败")
                    cur_url = next_page_url_template.format(
                        verifycode, cur_page)
                except ECCError as e:
                    print("".format(e))
                    continue
                except Exception as e:
                    print("获取验证码失败，err：{}".format(e))
                    continue
            else:
                cur_url = next_page_url_template.format('', cur_page)

            try:

                resp = requests.get(cur_url, headers=self.headers)
                resp_content = resp.text

                if re.search(r"滑动验证页面|TraceID: ", resp_content):
                    print('{} 出现滑块'.format(cur_url))
                    resp_content = self.captcha(cur_url)
                    if resp_content == '':
                        raise LimitError("滑块验证失败，请切换IP")
                elif re.search(
                        r'ui-dialog ui-widget ui-widget-content ui-corner-all  ui-draggable ui-resizable',
                        resp_content):
                    print('图片验证码验证失败，url：{}'.format(cur_url))
                    raise ECCError('图片验证码校验错误，请重试')
                elif cur_page == self.total_page:
                    print('抓取结束')
                    return
                else:
                    print('{} 页面正常，开始解析页面'.format(cur_url))
                    self.parse_page(resp_content, cur_url, proxies)
                    cur_page += 1

            except LimitError as e:
                print("".format(e))
                redis_client.delete(self.ip_key)  # 删除旧的IP
                self.refresh_proxy()
                proxies = {
                    'http': 'http://{}'.format(self.proxy),
                    'https': 'http://{}'.format(self.proxy),
                }
                continue

            except ECCError as e:
                print("".format(e))
                continue

            except Exception as e:
                print("出现未知错误：{}".format(e))
                return

    def captcha(self, cur_url):

        proxy = self.proxy

        async def handler():

            retry_times = 1
            resp_content = ''

            try:
                browser = await self.init_browser(proxy)

                while retry_times < 10:  # 尝试破解滑块5次
                    print('{} 第 {} 次解决滑块验证码'.format(cur_url, retry_times))

                    page = await self.open_page(browser, cur_url)  # 浏览器打开滑块页面
                    await page.waitForSelector('#nc_1__scale_text',
                                               timeout=60000)  # 等待滑块区域出现

                    await self.move_to_gap(page)  # 移动滑块

                    asyncio.sleep(3)

                    if refresh_button := await page.querySelector(
                            "#\`nc_1_refresh1\`"):  # 校验滑块是否成功
                        retry_times += 1
                        refresh_button.click()
                        print('{} 滑块校验失败，刷新重试'.format(page.url))
                        continue

                    await page.waitForSelector('.index_part2')
                    resp_content = await page.content()
                    break

            except Exception as e:
                print("滑块解决失败，err：{}".format(e))

            finally:
                await browser.close()
                print('关闭浏览器，返回页面数据')
                return resp_content

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(handler())
        return result

    async def crawl(self, url):

        browser = await self.init_browser()

        page = await self.open_page(browser, url)

        # button = await page.xpath('//a[contains(text(), "下一页")]')

        # await button.click()

        # html = await page.content()

        while True:

            try:

                pre_url = page.url
                html = await page.content()

                cur_page = self.get_cur_page(page)

                page.url_key = '{}:{}'.format(self.version, cur_page)

                print('开始翻页流程，url：{}'.format(page.url))

                if self.failure_page:

                    if ceil(cur_page / 10) == ceil(self.failure_page /
                                                   10):  # 在同一页数栏
                        print(
                            '失败页数与当前页在同一栏，无需页数栏翻页，cur_page：{}，failure_page：{}'.
                            format(cur_page, self.failure_page))

                        next_page_elem = browser.find_elements(
                            'xpath', '//a[@onclick="serchPage({})"]'.format(
                                self.failure_page))
                        self.failure_page = None

                    elif ceil(cur_page / 10) < ceil(
                            self.failure_page / 10):  # 需要对页数栏进行翻页
                        print('失败页数大于11，需页数栏翻页，cur_page：{}，failure_page：{}'.
                              format(cur_page, self.failure_page))

                        if cur_page % 10 == 0:  # 页数栏进行翻页操作
                            next_page_elem = browser.find_elements(
                                'xpath', '//a[contains(text(), "下一页")]')
                            print(
                                '当前页数为页数栏最后一页，需要点击翻页，cur_page：{}，failure_page：{}'
                                .format(cur_page, self.failure_page))

                        else:  # 点击当前页数栏最后一页
                            next_page_elem = browser.find_elements(
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

                    next_page_elem = await page.xpath(
                        '//a[contains(text(), "下一页")]')

                if not next_page_elem:

                    if re.search(r"滑动验证页面", html):
                        print('{} 出现滑块'.format(page.url))

                        retry_times = 1

                        while retry_times < 5:

                            print('{} 第 {} 次解决滑块验证码'.format(
                                page.url, retry_times))

                            await self.move_to_gap(page)

                            if refresh_button := await page.querySelector(
                                    "#\`nc_1_refresh1\`"):

                                print('{} 滑块校验失败'.format(page.url))

                                retry_times += 1

                                # TODO: 优化，未通过则循环刷新通过

                                refresh_button.click()

                            else:
                                next_page_elem = await page.xpath(
                                    '//a[contains(text(), "下一页")]')
                                break

                        else:
                            print("{} 滑块验证失败 {} 次，停止尝试，退出程序".format(
                                page.url, retry_times))
                            # 滑块失败，切换IP，重新抓取
                            browser = await self.init_browser()
                            page = await self.open_page(browser, pre_url)
                            continue

                    elif await page.querySelector("#ui-dialog-title-1"):
                        print('图片验证码验证失败，url：{}'.format(page.url))

                        if (redis_client.hget(self.url_batch, page.url_key)
                            ) and int((redis_client.hget(
                                self.url_batch, page.url_key).decode()) > 50):
                            print('{} 失败次数大于30次，切换IP重新抓取'.format(page.url))

                            browser = await self.init_browser()
                            page = await self.open_page(browser, pre_url)
                            continue

                        match = re.search(r'&page=(\d*)', page.url).group(1)
                        self.failure_page = int(match)

                        page = await self.open_page(browser,
                                                    self.home_page)  # 返回首页
                        redis_client.hincrby(self.url_batch, page.url_key,
                                             1)  # 记录不同页数验证码出错次数

                        continue

                    elif cur_page == self.total_page:
                        print('已抓取完最后一页，结束')
                        redis_client.delete(self.url_batch)
                        break

                    else:
                        print('当前未找到下一页元素，重新尝试，cur_page：{}，failure_page：{}'.
                              format(cur_page, self.failure_page))

                        for i in range(1, 4):  # 下一页模块未加载出来
                            print("第 {} 次重新获取下一页，url：{}".format(i, page.url))

                            next_page_elem = await page.xpath(
                                '//a[contains(text(), "下一页")]')
                            time.sleep(1)

                            if next_page_elem:
                                continue

                        if not next_page_elem:
                            print('出现未知情况，url：{}'.format(page.url))
                            break

                elem = next_page_elem[0]
                await page.evaluate(
                    '_ => {window.scrollBy(0, window.innerHeight);}')  # 翻到底部
                time.sleep(1)

                print('当前打开地址：{}'.format(pre_url))

                if not self.check_old_url(page):  # 不保存重复数据
                    # 多线程访问详情
                    print('{} 解析页面，保存数据'.format(page.url))

                    await self.extract_value(html, page.url)

                    redis_client.hset(self.url_batch, page.url_key, 0)

                print('{} 点击翻页'.format(page.url))

                await elem.click()
                await page.waitForNavigation(
                    {'timeout': 0}
                )  # 避免 Execution context was destroyed, most likely because of a navigation.
                page.setDefaultNavigationTimeout(300000)

                time.sleep(3)

                pages = await browser.pages()
                page = pages[-1]

                if await page.xpath(
                        '//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all  ui-draggable ui-resizable"]'
                ):
                    print('{} 出现图片验证码'.format(page.url))

                    await self.verify_img_code()

            # except selenium.common.exceptions.NoSuchElementException as e:
            #     print("页面异常，错误：{}，处理前地址：{}，处理后地址：{}".format(
            #         e, pre_url, page.url))
            #     browser.get(pre_url)
            #     time.sleep(1)

            except LimitError as e:
                print('访问 {} 达到最大限制次数，切换IP，所属页数：{}，error：{}'.format(
                    self.detail_url, page.url, e))
                browser = await self.init_browser()
                page = await self.open_page(browser, pre_url)

            # except selenium.common.exceptions.WebDriverException as e:
            #     print('代理：{}异常，当前地址：{}，切换IP，error：{}'.format(
            #         self.cur_proxy, page.url, e))
            #     self.laod_webdriver()

            except Exception as e:
                print("页面出现未知问题，错误：{}，处理前地址：{}，当前地址：{}".format(
                    e, pre_url, page.url))
                break

        # print('{} 不是目标代理'.format(proxy))

        # redis_client.delete(ip_key)

        time.sleep(2)

        await browser.close()

    def start(self):

        # loop = asyncio.get_event_loop()

        # loop.run_until_complete(asyncio.wait([self.crawl(self.home_page)]))
        self.crawl_main(12)

    async def verify_img_code(self, page):
        verify_code_area = await page.querySelector('#imgVerify')
        verify_code_img = await verify_code_area.screenshot(
        )  # 由于验证码图片动态改变，因此需要截图

        verify_code = captcha_instance.captcha_handler_by_content(
            verify_code_img)

        await page.type('.txtVerifyCode', verify_code)  # 输入验证码

        time.sleep(1)

        submit = await page.querySelector('#btnSaveProRes')
        await submit.click()

        time.sleep(3)

    async def extract_value(self, html, parent_url):

        print('开始解析检索页数据，url：{}'.format(parent_url))

        selector_new = etree.HTML(html)

        trs = selector_new.xpath("//table[@class='table_list']/tbody//tr")

        for tr in trs[1:]:

            all_td = tr.xpath('td')

            revisions_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[0].xpath('a/@href')[0])

            detail_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[2].xpath('p/a/@href')[0])

            registration_number = all_td[1].xpath('string(.)')
            registered_topic = all_td[2].xpath('string(.)')
            study_type = all_td[3].xpath('string(.)')
            registration_date = all_td[4].xpath('string(.)')

            info = {
                'registration_number': registration_number,  # 注册号
                'registered_topic': registered_topic,  # 注册题目
                'study_type': study_type,  # 研究类型
                'registration_date': registration_date,  # 注册时间
                'detail_url': detail_url,
                'parent_url': parent_url,
                'revisions_url': revisions_url  # 历史版本地址
            }

            self.detail_url = detail_url

            detail_info = self.parse_detail(detail_url, self.headers,
                                            parent_url)

            info['detail'] = detail_info
            info['version'] = self.version

            # print('{} 抓取到的数据：\n{}'.format(parent_url, info))
            mongo_collection.insert_one(info)

    def parse_page(self, html, parent_url, proxies):
        print('开始解析检索页数据，url：{}'.format(parent_url))

        selector_new = etree.HTML(html)

        trs = selector_new.xpath("//table[@class='table_list']/tbody//tr")

        for tr in trs[1:]:

            all_td = tr.xpath('td')

            revisions_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[0].xpath('a/@href')[0])

            detail_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[2].xpath('p/a/@href')[0])

            registration_number = all_td[1].xpath('string(.)')
            registered_topic = all_td[2].xpath('string(.)')
            study_type = all_td[3].xpath('string(.)')
            registration_date = all_td[4].xpath('string(.)')

            info = {
                'registration_number': registration_number,  # 注册号
                'registered_topic': registered_topic,  # 注册题目
                'study_type': study_type,  # 研究类型
                'registration_date': registration_date,  # 注册时间
                'detail_url': detail_url,
                'parent_url': parent_url,
                'revisions_url': revisions_url  # 历史版本地址
            }

            self.detail_url = detail_url

            detail_info = self.parse_detail(detail_url, self.headers,
                                            parent_url, proxies)

            info['detail'] = detail_info
            info['version'] = self.version

            # print('{} 抓取到的数据：\n{}'.format(parent_url, info))
            mongo_collection.insert_one(info)

    def parse_detail(self, cur_url, headers, parent_url, proxies):
        print('开始解析详情页数据，detail_url: {}，url：{}'.format(cur_url, parent_url))
        try:

            resp = requests.get(cur_url, headers=headers, proxies=proxies)
            resp_content = resp.text

            if re.search(r"滑动验证页面|TraceID: ", resp_content):
                print('{} 出现滑块'.format(cur_url))
                resp_content = self.captcha(cur_url)
                if resp_content == '':
                    raise LimitError("滑块验证失败，请切换IP")

            if '非常抱歉!您查看的项目的不存在或已超过当天最大查看次数' in resp_content:
                print('{} 已经超过最大尝试次数'.format(cur_url))
                return {}

            selector_new = etree.HTML(resp_content)

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

        except requests.exceptions.ConnectTimeout as e:
            raise LimitError("解析详情页出现错误：{}，请切换IP".format(e))

        except Exception as e:

            print("解析页面失败\nerror：{}\nresp.text：{}".format(e, resp_content))

            return {}

    def check_old_url(self, page):

        if redis_client.hexists(self.url_batch, page.url_key):  # 多线程问题
            return True

        return False

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


# async def main():

#     options = {
#         'ignoreDefaultArgs': ['--enable-automation'],
#         'args': [
#             "--start-maximized",
#             "--window-size=1920,1080",
#             '--disable-infobars',
#         ]  # 设置浏览器外观
#     }

#     browser = await launch(headless=False,
#                            options=options,
#                            executablePath='/usr/bin/google-chrome-stable')

#     page = await browser.newPage()
#     await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面大小
#     await page.evaluateOnNewDocument(
#         '() =>{ Object.defineProperties(navigator,'
#         '{ webdriver:{ get: () => false } }) }')  # 去掉驱动检测

#     await page.goto('https://www.baidu.com/')
#     time.sleep(3)
#     url = 'https://bot.sannysoft.com/'
#     await page.goto(url)
#     time.sleep(3)
#     # page1 = await browser.newPage()
#     # url2 = 'https://web.uutool.cn/'
#     # await page1.goto(url2)
#     await page.screenshot({'path': 'example.png'})
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())

# print('结束....')