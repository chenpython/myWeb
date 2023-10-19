import asyncio
import time

from pyppeteer import launch
from pyppeteer_stealth import stealth
from selenium import webdriver


def pyppteer_browser():

    async def open_browser():
        # url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.5.1"
        url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
        options = {
            # 'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            # 设置浏览器外观
            'args': [
                "--start-maximized",
                # "--window-size=1920,1080",
                # '--disable-infobars',
                # '--no-sandbox',  # Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
            ]
        }
        browser = await launch(
            headless=False,
            # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            options=options,
            executablePath='/usr/bin/google-chrome-stable', # ubuntu
            # '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',   # MacOS
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
        
        login_page_cnt = await page.content()

        username = await page.querySelector('input[id="loginname"]')
        await username.type('jlsl123456')

        password = await page.querySelector('input[id="nloginpwd"]')
        await password.type("250Kuai4Mao1")

        after_input_content = await page.content()

        await asyncio.sleep(5)

        submit = await page.querySelector("div[class='item item-fore5']")
        if not submit:
            pass
        await submit.click()
        await page.waitForNavigation()

        after_submit_content = await page.content()
        
        await browser.close()

        time.sleep(3)


    loop = asyncio.new_event_loop()
    loop.run_until_complete(open_browser())
    print("end")



if __name__ == "__main__":

    pyppteer_browser()

