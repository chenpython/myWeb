import asyncio
import random

from pyppeteer import launch
from pyppeteer_stealth import stealth

from .. import settings
from ..common_tools import log


class PyppteerChromeBrowser:

    def __init__(self, proxy=None):

        # 初始化浏览器配置
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

        if proxy:
            self.options['args'].append(f'--proxy-server={proxy}')

        self.path = settings.CHROME_PATH

    async def __aenter__(self):
        self.browser = await launch(
            headless=False,  # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            options=self.options,
            executablePath=self.path)
        return self.browser

    async def __aexit__(self, type, value, traceback):
        try:
            await self.browser.close()
        except Exception as e:
            log.error("关闭浏览器失败，error：{}".format(e))

    @staticmethod
    async def open_page(browser, url):

        page = await browser.newPage()
        # 设置页面参数
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/104.0.0.0 Safari/537.36')
        await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面大小
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')  # 去掉驱动检测

        await page.setJavaScriptEnabled(enabled=True)
        # 防止页面识别出脚本(反爬虫关键语句)
        await stealth(page)

        await page.goto(url)

        return page

    @staticmethod
    def handle_distance(distance):
        """将直线距离转为缓慢的轨迹"""

        slow_distance = []
        while sum(slow_distance) <= distance:
            slow_distance.append(random.uniform(-2, 30))

        if sum(slow_distance) != distance:
            slow_distance.append(distance - sum(slow_distance))
        return slow_distance

    @staticmethod
    async def move_to_gap(page):

        # 模拟鼠标滑动
        await page.hover('#nc_1_n1z')

        await page.mouse.down()

        slider = await page.querySelector('.nc-lang-cnt')

        position = await slider.boundingBox()

        track = PyppteerChromeBrowser.handle_distance(position['x'])

        for dis in track:
            await page.mouse.move(page.mouse._x + dis, page.mouse._y, {'delay': random.randint(500, 1000), 'steps': 3})

        await page.mouse.up()


async def run():

    async with PyppteerChromeBrowser() as browser:

        page = await PyppteerChromeBrowser.open_page(
            browser, 'https://www.szlcsc.com/ipLimited.html?front=https%3A%2F%2Fwww.szlcsc.com%2F')

        await PyppteerChromeBrowser.move_to_gap(page)
        asyncio.sleep(3)


def main():
    asyncio.run(run())
