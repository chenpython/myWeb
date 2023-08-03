import asyncio
import random
import re
from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests


class PyppteerChromeBrowser:

    def __init__(self, proxy=None):

        self.options = {
            'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            # 设置浏览器外观
            'args': [
                "--start-maximized",
                "--window-size=1920,1080",
                '--disable-infobars',
                '--no-sandbox',  # Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
            ],
            # 'dumpio':
            # True,  # 把无头浏览器进程的 stderr 核 stdout pip 到主程序，也就是设置为 True 的话，chromium console 的输出就会在主程序中被打印出来
            # 'logLevel':
            # 'ERROR'
        }
        self.options = {}

        if proxy:
            self.options['args'].append(f'--proxy-server={proxy}')

        self.path = '/usr/bin/google-chrome-stable'

    async def __aenter__(self):
        self.browser = await launch(
            headless=False,
            # headless=
            # True,  # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            options=self.options,
            executablePath=self.path)
        self.chrome_process_id = self.browser.process.pid
        return self.browser

    async def __aexit__(self, type, value, traceback):
        try:
            await self.browser.close()
        except Exception as e:
            print("关闭浏览器失败，error：{}".format(e))


class Test:
    headers = {
        'Host': 'www.chictr.org.cn',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.chictr.org.cn/searchproj.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    cookies = {}

    def check_is_normal_page(self, resp_content):
        if '非常抱歉!您查看的项目的不存在或已超过当天最大查看次数' in resp_content:
            return False
        if 'document.cookie=name+"="+value+";expires="+expiredate.toGMTString()+' in resp_content:
            return False
        if re.search(r"<h1>404 Not Found</h1>", resp_content):
            return False

        if re.search(r'共检索到<b>0</b>个符合检索条件的试验', resp_content):
            return False

        # if any([('历史版本' in resp_content and '注册时间' in resp_content),
        #         ('注册号' in resp_content and '下载XML文档' in resp_content)]):
        #     return True
        if self.check_is_captcha_page(resp_content):
            return False

        return True

    def check_is_captcha_page(self, resp_content):
        if (re.search(r"滑动验证页面|TraceID: ", resp_content)
                or '请按住滑块，拖动到最右边' in resp_content
                or '别离开，为了更好的访问体验，请滑动滑块进行验证，通过后即可继续访问网页' in resp_content):
            return True
        return False

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

        await asyncio.sleep(2)
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

        return page

    async def main(self):
        # 启动浏览器
        # # 初始化浏览器配置
        # options = {
        #     'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
        #     'args':
        #     ["--start-maximized", "--window-size=1920,1080",
        #      '--disable-infobars']  # 设置浏览器外观
        # }

        for i in range(1, 6000):
            url = 'https://www.chictr.org.cn/searchproj.html?page={}&title=&officialname=&subjectid=&regstatus=&regno=&secondaryid=&applier=&studyleader=&createyear=&sponsor=&secsponsor=&sourceofspends=&studyailment=&studyailmentcode=&studytype=&studystage=&studydesign=&recruitmentstatus=&gender=&agreetosign=&measure=&country=&province=&city=&institution=&institutionlevel=&intercode=&ethicalcommitteesanction=&whetherpublic=&minstudyexecutetime=&maxstudyexecutetime=&btngo=btn'.format(
                i)

            resp = requests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
            )
            content = resp.text
            if self.check_is_captcha_page(content):

                async with PyppteerChromeBrowser() as browser:
                    page = await self.open_page(browser, url)
                    content = await page.content()  # 获取页面源码
                    await self.move_to_gap(page)  # 移动滑块
                    move_content = await page.content()  # 获取页面源码
                    if self.check_is_normal_page(move_content):
                        print("{} 滑块验证成功，请求完成")
                        cookies_list = await page.cookies()
                        self.cookies = {
                            item['name']: item['value']
                            for item in cookies_list
                        }
                        self.headers['Referer'] = page.url
                    else:
                        print("{} 滑块验证失败".format(url))

            elif resp.status_code == 200 and self.check_is_normal_page(
                    content):
                print('{} 请求正常'.format(url))
            else:
                print("{} 未知情况".format(url))


import aiohttp
from yarl import URL


async def perform_request(url, cookie_jar=None):
    async with aiohttp.ClientSession(cookie_jar=cookie_jar) as session:

        response = await session.get(url)

        response_cookies = session.cookie_jar.filter_cookies(response.url)

        url1 = 'https://blog.csdn.net/The_Time_Runner/article/details/89352464'
        session.cookie_jar.update_cookies(response.cookies,
                                          response_url=URL(url1))

        response1 = await session.get(url1)

        response_cookies_1 = session.cookie_jar.filter_cookies(response1.url)


async def test_cookie():
    # 执行请求并携带 cookies

    cookie_jar = aiohttp.CookieJar(unsafe=True)

    cookie_jar.update_cookies({'example_cookie': '12345'})

    response_text = await perform_request(
        'https://www.zhihu.com/question/19840137', cookie_jar=cookie_jar)


if __name__ == "__main__":
    # test = Test()
    # asyncio.get_event_loop().run_until_complete(test.main())
    asyncio.run(test_cookie())
