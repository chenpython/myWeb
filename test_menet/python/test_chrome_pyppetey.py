import asyncio
import time
from pyppeteer import launch


async def main():

    options = {
        'ignoreDefaultArgs': ['--enable-automation'],
        'args': [
            "--start-maximized",
            "--window-size=1920,1080",
            '--disable-infobars',
        ]  # 设置浏览器外观
    }

    browser = await launch(headless=True,
                           options=options,
                           executablePath='/usr/bin/google-chrome')

    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面大小
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator,'
        '{ webdriver:{ get: () => false } }) }')  # 去掉驱动检测

    await page.goto('https://www.baidu.com/')
    time.sleep(3)
    # url = 'https://bot.sannysoft.com/'
    # await page.goto(url)
    # time.sleep(3)
    # page1 = await browser.newPage()
    # url2 = 'https://web.uutool.cn/'
    # await page1.goto(url2)
    await page.screenshot({'path': '/root/crawlab_workspace/tmp/example.png'})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

print('结束....')