import asyncio, time, re, json, random
import signal
import os
import datetime
import aiohttp

import cv2
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.errors import PageError
from lxml.html import etree

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError

from ..menet.common_tools import db, tools, proxy, const, decorator, crawlab_task
from ..menet import settings

mongo_client = db.mongo_client
mongo_collection = mongo_client['results_who_clinic']

redis_client = db.redis_client

captcha_instance = tools.captcha_instance
proxy_instance = proxy.Proxy()

default_total_page_size = 'WHO_DEFAULT_TOTAL_PAGE_SIZE'
default_total_page = int(redis_client.get(default_total_page_size).decode(
)) if redis_client.get(default_total_page_size) else 6590

exists_chrome_process_ids = 'CHROME_PROCESS_IDS'

version_key = 'WHO_VERSION_KEY'
WHO_JOB_ID = "clean_failed_queue"

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

sched = BackgroundScheduler()

crawlab_task_recorder = crawlab_task.CrawlabTaskRecorder()


class LimitError(Exception):
    pass


class ECCError(Exception):
    pass


class WHO:

    headers = headers
    url_prefix = 'https://www.chictr.org.cn'
    home_page = "https://www.chictr.org.cn/searchproj.aspx"
    allowed_domains = ['www.chictr.org.cn']

    public_content = {
        "province": "中国",
        "website_name": "中国临床试验注册中心",
        "website_domain": "http://www.chictr.org.cn/searchproj.aspx",
        "crawl_frequence": "一周一次",
        "website_location": "首页 > 检索入口 > 检索试验",
    }

    def __init__(self,
                 redis_version_key=None,
                 page_batch=None,
                 failed_detail_urls=None,
                 failed_menu_urls=None,
                 version=None,
                 cur_page=1) -> None:

        if cur_page:
            self.cur_page = cur_page
        else:
            self.cur_page = 1

        self.version_key = version_key
        self.version = version  # 继续上一个的批次
        self.redis_version_key = redis_version_key
        self.page_batch = page_batch
        self.failed_detail_urls = failed_detail_urls
        self.failed_menu_urls = failed_menu_urls
        self.ip_key = None
        self.browser = None

        self.session = aiohttp.ClientSession()

        self.pattern = re.compile(r"\n|\r|\t")

        self.next_page_url_template = 'https://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode={}&page={}'

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

        page = await self.browser.newPage()
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

        return page

    async def init_browser(self, proxy):
        # 由于需要切换不同代理，无法使用现有chrome

        # 配置参数参考:https://juejin.cn/post/6844904036634722318

        await self.close_chrome()

        # 初始化浏览器配置
        options = {
            'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            # 设置浏览器外观
            'args': [
                "--start-maximized",
                "--window-size=1920,1080",
                '--disable-infobars',
                f'--proxy-server={proxy}',
                '--no-sandbox',  # Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
            ],
            # 'dumpio':
            # True,  # 把无头浏览器进程的 stderr 核 stdout pip 到主程序，也就是设置为 True 的话，chromium console 的输出就会在主程序中被打印出来
            # 'logLevel':
            # 'ERROR'
        }
        path = settings.CHROME_PATH

        self.browser = await launch(
            headless=
            True,  # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            options=options,
            executablePath=path,
            # autoClose=False  # 解决 browser.close 出现 loop close 问题
        )

        # chrome_ids_key = '{}:{}'.format(self.redis_version_key,
        #                                 exists_chrome_process_ids)
        # mapping = {
        #     self.browser.process.pid: int(datetime.datetime.now().timestamp())
        # }
        # redis_client.zadd(chrome_ids_key, mapping=mapping)

    async def img_code(self):
        img_time = random.random()

        img_url = f'https://www.chictr.org.cn/Tools/verifyimagepage.aspx?textcolor=2&bgcolor=F4F4F4&ut=1&time={img_time}'

        verifycode = await tools.captcha_instance.captcha_handler_by_url_async(
            img_url, self.headers, self.proxy_url, self.session)

        return verifycode

    async def refresh_proxy_(self):

        self.proxy = proxy_instance.random_one_proxy()  # 自建代理池短效IP

        self.ip_key = json.dumps(self.proxy)

        self.proxies = {
            'http': 'http://{}'.format(self.proxy),
            'https': 'http://{}'.format(self.proxy),
        }

        self.proxy_url = 'http://{}'.format(self.proxy)
        await self.close_chrome()

    async def start(self, sem, method, **kwargs):
        async with sem:
            method = getattr(self, method)
            await method(**kwargs)

    async def crawl_main(self, cur_page, end_page):

        start_time = time.perf_counter()
        start_page = cur_page

        try:
            await self.refresh_proxy_()

            while cur_page < end_page:  # 多线程

                if redis_client.hexists(self.page_batch, cur_page):
                    if int(
                            redis_client.hget(
                                self.page_batch,
                                cur_page).decode()) >= 1:  # 翻页成功的页面则跳过
                        cur_page += 1
                        continue

                await asyncio.sleep(random.uniform(2, 5))  # 随机等待时间，避免网站崩溃

                if cur_page == 1:
                    cur_url = self.home_page
                elif cur_page > 3:  # 从第3页开始均需要携带验证码参数
                    try:
                        verifycode = await self.img_code()
                        if not verifycode or len(verifycode) != 5:
                            raise ECCError("图片验证码识别失败")
                        cur_url = self.next_page_url_template.format(
                            verifycode, cur_page)
                    except ECCError as e:
                        print("".format(e))
                        continue
                    except asyncio.exceptions.TimeoutError as e:
                        print("获取验证码超时，切换IP，err：{}".format(e))
                        await self.refresh_proxy_()
                        continue
                    except aiohttp.client_exceptions.ClientProxyConnectionError as e:
                        print('代理异常，刷新IP')
                        await self.refresh_proxy_()
                        continue
                    except cv2.error as e:
                        print("图片异常，重新下载，err：{}".format(e))
                        await self.refresh_proxy_()
                        continue
                    except Exception as e:
                        print("获取图片验证码失败，err：{}".format(e))
                        if 'Authorized failed' in str(e):
                            print("代理异常，切换IP")
                            await self.refresh_proxy_()

                        continue
                else:
                    cur_url = self.next_page_url_template.format('', cur_page)

                try:

                    resp = await self.session.get(cur_url,
                                                  proxy=self.proxy_url,
                                                  headers=self.headers,
                                                  timeout=15)
                    resp_content = await resp.text()

                    if re.search(r"滑动验证页面|TraceID: ", resp_content):
                        resp_content = await self.captcha(cur_url)
                        if resp_content == '':
                            raise LimitError("滑块验证失败，请切换IP")
                    if re.search(
                            r'ui-dialog ui-widget ui-widget-content ui-corner-all  ui-draggable ui-resizable',
                            resp_content):
                        raise ECCError('图片验证码校验错误，请重试')
                    if re.search(r'共检索到<b>0</b>个符合检索条件的试验', resp_content):
                        continue

                    await self.parse_page(resp_content, cur_url, cur_page)

                    if cur_page == 1:
                        total_page = int(
                            re.search(r"共(\d+)页", resp_content).group(1))
                        redis_client.set(default_total_page_size,
                                         total_page)  # 永久保留上一次的页数

                    cur_page += 1

                except (LimitError, asyncio.exceptions.TimeoutError) as e:
                    print("".format(e))
                    await self.refresh_proxy_()
                    continue

                except ECCError as e:
                    print("".format(e))
                    continue

                except RecursionError as e:
                    print("{} 出现异常，err：{}".format(cur_url, e))
                    continue
                except Exception as e:
                    print("出现未知错误：{}".format(e))
                    failed_menu_info = {
                        'version': self.version,
                        'cur_page': cur_page
                    }
                    failed_menu_value = json.dumps(failed_menu_info)
                    redis_client.lpush(self.failed_menu_urls,
                                       failed_menu_value)  # 记录失败的详情url
                    cur_page += 1
                    continue
        except Exception as e:
            print("执行批次 {} 失败，err：{}".format(self.version, e))

        await self.session.close()
        await self.close_chrome()

        end_time = time.perf_counter()
        print('{} 批次 {} 至 {} 区间采集结束，共消耗 {:.8f} 秒'.format(
            self.version, start_page, end_page, end_time - start_time))

    async def captcha(self, cur_url):
        """滑块验证码破解"""

        resp_content = ''
        retry_times = 1

        if not self.browser:  # 在需要图片验证码时创建浏览器
            await self.init_browser(self.proxy)

        while retry_times < 10:  # 尝试破解滑块5次
            await asyncio.sleep(random.uniform(0, 3))  # 随机等待时间

            try:

                page = await self.open_page(self.browser, cur_url)  # 浏览器打开滑块页面
                if await page.xpath('//div[@class="index_part2"]'):
                    resp_content = await page.content()

                else:
                    await page.waitForSelector('#nc_1__scale_text',
                                               timeout=10000)  # 等待滑块区域出现

                    await self.move_to_gap(page)  # 移动滑块
                    asyncio.sleep(3)
                    await page.waitForNavigation({
                        'timeout': 15000,
                        # 'waitUntil': ['domcontentloaded', 'waitUntil']
                    })

                    if refresh_button := await page.querySelector(
                            "#\`nc_1_refresh1\`"):  # 校验滑块是否成功
                        retry_times += 1
                        refresh_button.click()
                        continue

                    await page.waitForSelector('.index_part2',
                                               timeout=20000)  # 等待搜索区域出现
                    resp_content = await page.content()

                await page.close()
                break

            except PageError as e:
                print("打开滑块页面报错，err：{}".format(e))
                retry_times += 1
                continue

            except Exception as e:
                print("滑块解决失败，err：{}".format(e))
                await page.close()
                retry_times += 1
                continue

        return resp_content

    async def parse_page(self, html, parent_url, cur_page):

        selector_new = etree.HTML(html)

        trs = selector_new.xpath("//table[@class='table_list']/tbody//tr")

        for tr in trs[1:]:
            all_td = tr.xpath('td')

            revisions_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[0].xpath('a/@href')[0])
            detail_url = 'https://{}/{}'.format(
                self.allowed_domains[0], all_td[2].xpath('p/a/@href')[0])

            registration_number = all_td[1].xpath('string(.)').strip()
            registered_topic = all_td[2].xpath('string(.)').strip()
            study_type = all_td[3].xpath('string(.)').strip()
            registration_date = all_td[4].xpath('string(.)').strip()

            info = {
                **{
                    'data': [{
                        'registration_number': registration_number,  # 注册号
                        'registered_topic': registered_topic,  # 注册题目
                        'study_type': study_type,  # 研究类型
                        'registration_date': registration_date,  # 注册时间
                        'detail_url': detail_url,
                        'revisions_url': revisions_url,  # 历史版本地址
                    }]
                },
                **{
                    'version': self.version,
                    'crawl_time': self.version,
                    'parent_url': parent_url,
                    'source_page': cur_page,
                },
                **self.public_content
            }
            self.detail_url = detail_url

            detail_info = await self.parse_detail(detail_url, self.headers,
                                                  parent_url, cur_page)
            redis_client.hincrby(self.page_batch, cur_page, 1)

            if not detail_info:
                detail_info = {
                    'detail_url': self.detail_url,
                    'parent_info': info
                }
                detail_info_value = json.dumps(detail_info)
                redis_client.lpush(self.failed_detail_urls,
                                   detail_info_value)  # 记录失败的详情url
                continue

            detail_info = tools.format_data(detail_info, replace_str=['  '])
            info['data'][0]['detail'] = detail_info
            info['timestamp'] = int(datetime.datetime.now().timestamp())

            self.store_data(info)

    @decorator.retry_decorator_custom(20, True, sleep_random=[2, 5])
    async def parse_detail(self, cur_url, headers, parent_url, cur_page):
        try:
            if not hasattr(self, 'proxy_url') or not getattr(
                    self, 'proxy_url', None):
                await self.refresh_proxy_()

            resp = await self.session.get(cur_url,
                                          proxy=self.proxy_url,
                                          headers=headers,
                                          timeout=25)
            resp_content = await resp.text()

            if re.search(r"滑动验证页面|TraceID: ", resp_content):
                resp_content = await self.captcha(cur_url)
                if resp_content == '':
                    raise LimitError("滑块验证失败，请切换IP")

            if '非常抱歉!您查看的项目的不存在或已超过当天最大查看次数' in resp_content:
                raise LimitError(
                    "查看的项目的不存在或已超过当天最大查看次数，url：{}".format(cur_url))

            if re.search(r"<h1>404 Not Found</h1>", resp_content):
                raise Exception("{} 获取页面异常。刷新重试".format(cur_url))

            selector_new = etree.HTML(resp_content)

            content_list = selector_new.xpath(
                "//div[@class='ProjetInfo_title']") + selector_new.xpath(
                    '//div[@class="ProjetInfo_ms"]')

            encoding = resp.charset if resp.charset else "utf-8"

            content = ''.join([
                etree.tostring(cnt, encoding=encoding,
                               method='html').strip().decode(encoding)
                for cnt in content_list
            ])

            registration_number = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "Registration number")]/following-sibling::td'
                )
            ]).strip()

            date_of_last_refreshed_on = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "Date of Last Refreshed on")]/following-sibling::td'
                )
            ]).strip()

            date_of_registration = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "Date of Registration")]/following-sibling::td'
                )
            ]).strip()

            registration_status = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "注册号状态")]/following-sibling::td')
            ]).strip()

            public_title = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "注册题目：")]/following-sibling::td')
            ]).strip()

            english_acronym = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "注册题目简写")]/following-sibling::td'
                )
            ]).strip()

            scientific_title = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究课题的正式科学名称")]/following-sibling::td'
                )
            ]).strip()

            study_subject_id = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究课题代号(代码)")]/following-sibling::td'
                )
            ]).strip()

            other_register = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "在二级注册机构或其它机构的注册号")]/following-sibling::td'
                )
            ]).strip()

            applicant = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人：")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人：")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_telephone = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人电话")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader_telephone = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人电话")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_fax = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人传真")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader_fax = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人传真")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_email = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人电子邮件")]/following-sibling::td[1]'
                )
            ]).strip()

            study_email = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人电子邮件")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_website = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请单位网址(自愿提供)")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader_website = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人网址(自愿提供)")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_address = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人通讯地址")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader_address = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人通讯地址")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_postcode = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请注册联系人邮政编码")]/following-sibling::td[1]'
                )
            ]).strip()

            study_leader_postcode = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究负责人邮政编码")]/following-sibling::td[1]'
                )
            ]).strip()

            applicant_institution = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "申请人所在单位：")]/following-sibling::td[1]'
                )
            ]).strip()

            approved_by_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "是否获伦理委员会批准")]/following-sibling::td[1]'
                )
            ]).strip()

            approved_no_of_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会批件文号")]/following-sibling::td[1]'
                )
            ]).strip()

            name_of_the_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "批准本研究的伦理委员会名称")]/following-sibling::td[1]'
                )
            ]).strip()

            date_of_approved_by_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会批准日期")]/following-sibling::td[1]'
                )
            ]).strip()

            contact_name_of_the_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会联系人：")]/following-sibling::td[1]'
                )
            ]).strip()

            contact_address_of_the_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会联系地址")]/following-sibling::td[1]'
                )
            ]).strip()

            contact_phone_of_the_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会联系人电话")]/following-sibling::td[1]'
                )
            ]).strip()

            contact_email_of_the_ethic_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "伦理委员会联系人邮箱")]/following-sibling::td[1]'
                )
            ]).strip()

            primary_sponsor = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究实施负责（组长）单位：")]/following-sibling::td[1]'
                )
            ]).strip()

            primary_sponsor_address = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究实施负责（组长）单位地址")]/following-sibling::td[1]'
                )
            ]).strip()

            secondary_sponsor = self.secondary_sponsor(
                selector_new=selector_new)

            source_of_funding = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "经费或物资来源")]/following-sibling::td[1]'
                )
            ]).strip()

            target_disease = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究疾病：")]/following-sibling::td[1]'
                )
            ]).strip()

            target_disease_code = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究疾病代码")]/following-sibling::td[1]'
                )
            ]).strip()

            study_type = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究类型")]/following-sibling::td[1]'
                )
            ]).strip()

            study_phase = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究所处阶段")]/following-sibling::td[1]'
                )
            ]).strip()

            objectives_of_study = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究目的")]/following-sibling::td[1]'
                )
            ]).strip()

            description_for_medicine = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "药物成份或治疗方案详述")]/following-sibling::td[1]'
                )
            ]).strip()

            study_design = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究设计：")]/following-sibling::td[1]'
                )
            ]).strip()

            inclusion_criteria = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "纳入标准")]/following-sibling::td[1]'
                )
            ]).strip()

            exclusion_criteria = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "排除标准")]/following-sibling::td[1]'
                )
            ]).strip()

            study_execute_time = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "研究实施时间")]/following-sibling::td[1]'
                )
            ]).strip()

            recruiting_time = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "征募观察对象时间")]/following-sibling::td[1]'
                )
            ]).strip()

            interventions = self.interventions(selector_new=selector_new)

            outcomes = self.outcomes(selector_new=selector_new)

            countries_of_recruitment = self.countries_of_recruitment(
                selector_new=selector_new)

            # TODO: 解析具体内容
            collecting_sample = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "采集人体标本")]/following-sibling::td[1]'
                )
            ]).strip()

            recruiting_status = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "征募研究对象情况")]/following-sibling::td[1]/p[1]'
                )
            ]).strip()

            participant_age = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "年龄范围")]/following-sibling::td[1]'
                )
            ]).strip()
            matches = self.pattern.findall(participant_age)
            for match in matches:
                participant_age = participant_age.replace(match, '')
            participant_age.replace(
                '                                                                                                                ',
                ' ')

            gender = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "性别：")]/following-sibling::td[1]'
                )
            ]).strip()

            randomization_procedure = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "随机方法（请说明由何人用什么方法产生随机序列）")]/following-sibling::td[1]'
                )
            ]).strip()

            blinding = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "盲法")]/following-sibling::td[1]')
            ]).strip()

            ipd_sharing = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "是否共享原始数据")]/following-sibling::td[1]'
                )
            ]).strip()

            the_way_of_sharing_ipd = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "共享原始数据的方式")]/following-sibling::td[1]'
                )
            ]).strip()

            data_collection_and_management = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "数据采集和管理（说明：数据采集和管理由两部分组成，一为病例记录表(Case Record Form, CRF)，二为电子采集和管理系统(Electronic Data Capture, EDC)，如ResMan即为一种基于互联网的EDC")]/following-sibling::td[1]'
                )
            ]).strip()

            data_and_safety_monitoring_committee = ''.join([
                cnt.xpath('string(.)') for cnt in selector_new.xpath(
                    '//td[contains(string(.), "数据与安全监察委员会")]/following-sibling::td[1]'
                )
            ]).strip()

            return {
                'registration_number': registration_number,
                'date_of_last_refreshed_on': date_of_last_refreshed_on,
                'date_of_registration': date_of_registration,
                'registration_status': registration_status,
                'public_title': public_title,
                'english_acronym': english_acronym,
                'scientific_title': scientific_title,
                'study_subject_id': study_subject_id,
                'other_register': other_register,
                'applicant': applicant,
                'study_leader': study_leader,
                'applicant_telephone': applicant_telephone,
                'study_leader_telephone': study_leader_telephone,
                'applicant_fax': applicant_fax,
                'study_leader_fax': study_leader_fax,
                'applicant_email': applicant_email,
                'study_email': study_email,
                'applicant_website': applicant_website,
                'study_leader_website': study_leader_website,
                'applicant_address': applicant_address,
                'study_leader_address': study_leader_address,
                'applicant_postcode': applicant_postcode,
                'study_leader_postcode': study_leader_postcode,
                'applicant_institution': applicant_institution,
                'approved_by_ethic_committee': approved_by_ethic_committee,
                'approved_no_of_ethic_committee':
                approved_no_of_ethic_committee,
                'name_of_the_ethic_committee': name_of_the_ethic_committee,
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
                'primary_sponsor': primary_sponsor,
                'primary_sponsor_address': primary_sponsor_address,
                'secondary_sponsor': secondary_sponsor,
                'source_of_funding': source_of_funding,
                'target_disease': target_disease,
                'target_disease_code': target_disease_code,
                'study_type': study_type,
                'study_phase': study_phase,
                'objectives_of_study': objectives_of_study,
                'description_for_medicine': description_for_medicine,
                'study_design': study_design,
                'inclusion_criteria': inclusion_criteria,
                'exclusion_criteria': exclusion_criteria,
                'study_execute_time': study_execute_time,
                'recruiting_time': recruiting_time,
                'interventions': interventions,
                'outcomes': outcomes,
                'countries_of_recruitment': countries_of_recruitment,
                'collecting_sample': collecting_sample,
                'recruiting_status': recruiting_status,
                'participant_age': participant_age,
                'gender': gender,
                'randomization_procedure': randomization_procedure,
                'blinding': blinding,
                'ipd_sharing': ipd_sharing,
                'the_way_of_sharing_ipd': the_way_of_sharing_ipd,
                'data_collection_and_management':
                data_collection_and_management,
                'data_and_safety_monitoring_committee':
                data_and_safety_monitoring_committee,
                'content': content
            }

        except (aiohttp.client_exceptions.ClientHttpProxyError,
                asyncio.exceptions.TimeoutError,
                aiohttp.client_exceptions.ClientProxyConnectionError,
                LimitError) as e:
            print("{} 解析页面失败，代理无效，来源页面：{}\n失败原因：error：{}，err：{}".format(
                cur_url, parent_url, e, e.__repr__()))
            await self.refresh_proxy_()
            raise e

        except Exception as e:
            print("{} 解析页面失败，来源页面：{}\n失败原因：error：{}，err：{}".format(
                cur_url, parent_url, e, e.__repr__()))
            raise e

    def interventions(self, selector_new):

        all_trs = selector_new.xpath(
            '//td[contains(string(.), "干预措施")]/following-sibling::td[1]//tr')

        results = []

        group = len(all_trs) // 4

        groups = [i * 4 for i in range(1, group + 1)]

        for index in groups:

            results.append({
                'group':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "组别")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'sample_size':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "样本量")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'intervention':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "干预措施：")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'intervention_code':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "干预措施代码")]/following-sibling::td[1]'
                    )
                ]).strip()
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
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "指标中文名")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'type':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "指标类型")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'measure_time_point_of_outcome':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "测量时间点")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'measure_method':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "测量方法")]/following-sibling::td[1]'
                    )
                ]).strip()
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
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "国家")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'province':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "省(直辖市)")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'city':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "市(区县)")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'institution_hospital':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "单位(医院)")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'level_of_the_institution':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "单位级别")]/following-sibling::td[1]'
                    )
                ]).strip()
            })

        return results

    def secondary_sponsor(self, selector_new):

        all_trs = selector_new.xpath(
            '//td[contains(string(.), "试验主办单位(项目批准或申办者)")]/following-sibling::td[1]//tr'
        )

        results = []

        group = len(all_trs) // 4

        groups = [i * 4 for i in range(1, group + 1)]

        for index in groups:

            results.append({
                'country':
                ''.join(
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "国家")]/following-sibling::td[1]'
                    )).strip(),
                'institution_hospital':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "单位(医院)")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'province':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "省(直辖市)")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'address':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 2].xpath(
                        'td[contains(string(.), "具体地址")]/following-sibling::td[1]'
                    )
                ]).strip(),
                'city':
                ''.join([
                    cnt.xpath('string(.)') for cnt in all_trs[index - 4].xpath(
                        'td[contains(string(.), "市(区县)")]/following-sibling::td[1]'
                    )
                ]).strip()
            })

        return results

    async def retry_failed_detail(self, info_list, headers):

        for info in info_list:
            parent_info = info['parent_info']
            cur_url = info['detail_url']

            parent_url = info['parent_info']['parent_url']
            cur_page = info['parent_info'].get('cur_page')

            result = await self.parse_detail(cur_url=cur_url,
                                             headers=headers,
                                             parent_url=parent_url,
                                             cur_page=cur_page)

            if not result:
                detail_info = {
                    'detail_url': cur_url,
                    'parent_info': parent_info
                }
                detail_info_value = json.dumps(detail_info)
                redis_client.lpush(self.failed_detail_urls, detail_info_value)

            else:
                parent_info['data'][0]['detail'] = result
                parent_info['timestamp'] = int(
                    datetime.datetime.now().timestamp())

                self.store_data(parent_info)

        await self.session.close()
        await self.close_chrome()

    async def close_chrome(self):
        if self.browser:
            try:
                await self.browser.close()  # 关闭浏览器
            except Exception as e:
                pass

        self.browser = None  # 去掉无效代理绑定的浏览器

    def store_data(self, data):
        mongo_collection.insert_one(data)
        redis_client.incrby(crawlab_task_recorder.task_id, 1)


async def run(version, cur_page, pre_end_page=default_total_page):

    if not version:

        if redis_client.exists(version_key):  # 继续上一个的批次
            version = redis_client.get(version_key).decode()
        else:
            version = datetime.datetime.now().strftime(
                "%Y%m%d %H:%M:%S")  # 开启新的批次
            redis_client.set(version_key, version)

    batch_size = 10  # 控制每个协程任务翻页数
    sem = asyncio.Semaphore(3)  # 控制协程并发数

    redis_version_key = version.replace(' ', '').replace(':', '')
    page_batch = '{}:all_pages'.format(redis_version_key)
    failed_detail_urls = '{}:failed_detail_urls'.format(redis_version_key)
    failed_menu_urls = '{}:failed_menu_urls'.format(redis_version_key)

    spider = type('Spider', (), {'name': 'who_clinic', 'crawl_time': version})
    crawlab_task_recorder.spider_open(spider)

    print('开始 {} 的数据采集，页数范围：{} ~ {}'.format(page_batch, cur_page,
                                            pre_end_page))

    start_time = time.perf_counter()
    try:

        sched.add_job(background_process,
                      "interval",
                      kwargs={
                          "redis_version_key": redis_version_key,
                          'page_batch': page_batch,
                          'failed_detail_urls': failed_detail_urls,
                          'failed_menu_urls': failed_menu_urls,
                          'version': version,
                          'cur_page': cur_page
                      },
                      hours=1,
                      id=WHO_JOB_ID)
        sched.start()

        tasks = [
            asyncio.create_task(
                WHO(redis_version_key=redis_version_key,
                    page_batch=page_batch,
                    failed_detail_urls=failed_detail_urls,
                    failed_menu_urls=failed_menu_urls,
                    version=version,
                    cur_page=cur_page).start(
                        sem, 'crawl_main', **{
                            'cur_page': page,
                            'end_page': min(page + batch_size,
                                            pre_end_page + 1)
                        }))
            for page in range(cur_page, pre_end_page + 1, batch_size)
        ]
        await asyncio.gather(*tasks)

        cur_end_page = redis_client.get(default_total_page_size)
        if cur_end_page and pre_end_page < int(
                redis_client.get(default_total_page_size).decode()):  # 抓取新增页数据

            cur_end_page = int(
                redis_client.get(default_total_page_size).decode())

            await run(version=version,
                      cur_page=pre_end_page,
                      pre_end_page=cur_end_page)

        await execute_failed_menu_queue(redis_version_key=redis_version_key,
                                        page_batch=page_batch,
                                        failed_detail_urls=failed_detail_urls,
                                        failed_menu_urls=failed_menu_urls,
                                        version=version,
                                        cur_page=cur_page)
        await execute_failed_detail_queue(
            redis_version_key=redis_version_key,
            page_batch=page_batch,
            failed_detail_urls=failed_detail_urls,
            failed_menu_urls=failed_menu_urls,
            version=version,
            cur_page=cur_page)

    except Exception as e:
        print("{} 执行报错，err：{}".format(version, e))
    else:
        redis_client.delete(page_batch)
        redis_client.delete(version_key)
    finally:
        sched.remove_all_jobs()
        sched.shutdown(wait=False)

    end_time = time.perf_counter()

    print('{} 批次整体采集结束，共消耗 {:.8f} 秒'.format(version, cur_page, pre_end_page,
                                            end_time - start_time))

    crawlab_task_recorder.spider_close(spider)


async def execute_failed_menu_queue(redis_version_key=None,
                                    page_batch=None,
                                    failed_detail_urls=None,
                                    failed_menu_urls=None,
                                    version=None,
                                    cur_page=None):

    print('开始清理 {} 的失败检索队列'.format(version))

    menu_length = redis_client.llen(failed_menu_urls)
    page_info_list = [
        redis_client.lpop(failed_menu_urls) for _ in range(menu_length)
    ]
    page_info = [json.loads(info.decode()) for info in page_info_list]
    sem = asyncio.Semaphore(3)

    tasks = [
        asyncio.create_task(
            WHO(redis_version_key=redis_version_key,
                page_batch=page_batch,
                failed_detail_urls=failed_detail_urls,
                failed_menu_urls=failed_menu_urls,
                version=version,
                cur_page=cur_page).start(
                    sem, 'crawl_main', **{
                        'cur_page': int(info['cur_page']),
                        'end_page': int(info['cur_page']) + 1
                    })) for info in page_info
    ]

    await asyncio.gather(*tasks)

    print('{} 失败检索页完成'.format(version))


async def execute_failed_detail_queue(redis_version_key=None,
                                      page_batch=None,
                                      failed_detail_urls=None,
                                      failed_menu_urls=None,
                                      version=None,
                                      cur_page=None):

    print('开始清理 {} 的失败详情队列'.format(version))

    detail_length = redis_client.llen(failed_detail_urls)

    if not detail_length:
        return
    detail_length = min(const.DEFAULT_WHO_DETAIL_BATCH_SIZE, detail_length)

    detail_list = (redis_client.lpop(failed_detail_urls)
                   for _ in range(detail_length))
    detail_info = [json.loads(info.decode()) for info in detail_list]

    who_instance = WHO(redis_version_key=redis_version_key,
                       page_batch=page_batch,
                       failed_detail_urls=failed_detail_urls,
                       failed_menu_urls=failed_menu_urls,
                       version=version,
                       cur_page=cur_page)

    who_instance.retry_failed_detail(detail_info, headers)

    print('{} 失败详情页页完成'.format(version))


def background_process(**kwargs):

    # kill_chrome_process(kwargs.get('redis_version_key'), clear_all=False)

    asyncio.run(execute_failed_detail_queue(**kwargs))


def kill_chrome_process(redis_version_key, clear_all=True):
    end_score = int(datetime.datetime.now().timestamp())
    if not clear_all:
        end_score = int((datetime.datetime.now() -
                         datetime.timedelta(hours=1)).timestamp())

    chrome_ids_key = '{}:{}'.format(redis_version_key,
                                    exists_chrome_process_ids)

    pid_list = redis_client.zrangebyscore(chrome_ids_key, 1, end_score)
    pid_list_ = [int(pid.decode()) for pid in pid_list]

    for pid in pid_list_:
        print('杀死无效 Chrome 进程：{}'.format(pid))
        os.kill(pid, signal.SIGKILL)
    for pid in pid_list_:
        redis_client.zrem(chrome_ids_key, pid)


def main(version, cur_page):

    asyncio.run(run(version=version, cur_page=cur_page))
