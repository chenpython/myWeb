import asyncio
from pyppeteer import launch
from pyppeteer.errors import PageError
from pyppeteer_stealth import stealth

from selenium import webdriver
import time


def pyppteer_browser():

    async def open_browser():
        url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.5.1"
        options = {
            'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            # 设置浏览器外观
            'args': [
                "--start-maximized",
                "--window-size=1920,1080",
                # '--disable-infobars',
                # '--no-sandbox',  # Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
            ]
        }
        browser = await launch(
            headless=False,
            # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            # options=options,
            executablePath=
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            # 通过 chrome 地址栏输入 chrome://version/ 路径获取 chrome://version/ 确定执行路径
            autoClose=False)

        page = await browser.newPage()
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

        await browser.close()

        print("end")

    asyncio.get_event_loop().run_until_complete(open_browser())


def selenium_browser():
    url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.5.1"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="chromedriver",
                              chrome_options=options)
    driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get(url)
    time.sleep(5)
    driver.quit()
    print("Done")


if __name__ == "__main__":

    pyppteer_browser()
    # selenium_browser()