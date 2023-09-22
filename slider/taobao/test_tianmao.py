import asyncio
import random
import re

import requests
from pyppeteer import launch
from pyppeteer.errors import PageError
from pyppeteer_stealth import stealth


def login_interface():

    url = 'https://login.taobao.com/member/login.jhtml?spm=a21n57.1.754894437.1.3af7523coKHJJR&f=top&redirectURL=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%25E7%259B%2590%25E9%2585%25B8%25E6%25B0%25A8%25E5%259F%25BA%25E8%2591%25A1%25E8%2590%2584%25E7%25B3%2596%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.jianhua.201856-taobao-item.2%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306'
    # headers = {
    #     'sec-ch-ua':
    #     '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    #     'Accept':
    #     'application/json, text/plain, */*',
    #     'Content-Type':
    #     'application/x-www-form-urlencoded',
    #     'bx-v':
    #     '2.5.1',
    #     'sec-ch-ua-mobile':
    #     '?0',
    #     'User-Agent':
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    #     'sec-ch-ua-platform':
    #     '"Windows"',
    #     'Origin':
    #     'https://login.taobao.com',
    #     'Sec-Fetch-Site':
    #     'same-origin',
    #     'Sec-Fetch-Mode':
    #     'cors',
    #     'Sec-Fetch-Dest':
    #     'empty',
    #     'Referer':
    #     'https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.754894437.1.5af92a8948fJ8r&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
    #     'Accept-Encoding':
    #     'gzip, deflate, br',
    #     'Accept-Language':
    #     'zh-CN,zh;q=0.9',
    #     'Cookie':
    #     'cna=uy1SHSHUvScCAduAjKJKXbnM; _m_h5_tk=737a51878f196f8ed793de38ab1513a8_1691049283281; _m_h5_tk_enc=53e6098783da34469579f38abdbb79ba; cookie2=105127586344b04f01ef0427bdfc91c1; t=3b3e51c3f96b6c1e5e26ec56f90b74c0; _tb_token_=753eb78971e8b; XSRF-TOKEN=37dcf81f-775b-4adf-9ff5-0ef48a9b45d9; _samesite_flag_=true; xlly_s=1; isg=BC0t-voJNUdkp9Gr4FibwXnMPMmnimFcYMvcGm8yIEQz5kmYPd67LcOw1LoA4nkU; tfstk=dCVH006ruJkCqSzlqBhC9w0tZj6tdHGSAud-2bnPQcoswDFLp82glumdP9GLI0qajDkdRyHkZzmswDFLp82gxkR-puFuCQ4bPWQIwwGQRbGPDiCxZyaINAVTlJAqAcHxUSSAMsUCE6UfOiI7fl5fUPA6EWS891HjmUXqrVXMZ0n48DzLz5zyD0zEOQd-j2XZDdJqnQOS7aFwFLME5Vmxk7Tds; l=fBMFZD0RNetpBakaBOfaPurza77TtIR8muPzaNbMi9fPO6CH5CAOW1OMy7LMCnGVEsj6r38PiVPBB4T8LyzHh6Yl3ZQ7XPQu6d8hEkcah'
    # }

    # data = {
    #     'loginId': '2427219623@qq.com',
    #     'password2':
    #     'bb8be9b1e98b5d72dd5407c6df8d65d24365ba166a39312c14fbac1c60c60842c1593cf0c893c414e12e2f9cd6d9def163353025e2b1d827b05d9f4de4f4716ddfff66b73b4cd2864763803d726c4d73f1527420fbb6f9738385b783b909355520168b9d91708dac8f15521f6d3700562282809e65737fde946d5f39ebb3f0a4',
    #     'keepLogin': 'false',
    #     'ua':
    #     '140%23pn2DWog6zzPyjQo2LxcTCtSdvwtFZhudHZ2yE45Edbkk8u2cAVT3cFhyKlYV4o7Plu8%2BWegzLtEq6Ruy05naie94ryVqlbzxhBMsLTWdzzc13XaIU6OzzPzbVXlqlbrD%2Br5wqiuYzFFy2XMvl61zzPkt0LSV%2BQ3l2gNKR3ht1bfVI284qlOokDrVg466dnkGOSvZrI7ZbI86hRd0qRd%2BopYICBGctNCXB8Me39zZVdQDFcAEt%2BiE0ivqQAc9486RacyY9W9YivdBHEEFwzO2sTAYSuewkpsoeVm1U9UWnTA1DshyA6x5OdNzudZSX3T4WG4i4gUb0zW8LYMMFD9XdkZNgNkCVxF%2BwPG1wrsvqGDZULZhpWP43P944k0PpOxyGReq9FQPaR1ZbwwTzEPp%2BXOBfg%2FneuRzPeT8Rjsozb6BGTJ9olZqGHF258uWjSVjOjg0YNOEUX9MPYOgJBGJwHH1Wnnfzig21Tbnicv6pFmISlC68RROCupwZEe7IbBVbdokliNNSuAHt4nJ2lYlCn8fMnOmPAc0CKwc7WJiK8GBJaf%2BPBXm2HK%2Fq%2B6h84X5qHfdLmUO8B%2B0IpbAAZyJ%2FCpnm3EQ%2B%2FP%2BdmB%2Ft6h28WvNjyc0JhJLONOp0UVtopYB2q%2FTTC4M%2BJ4oEHhAUV785A%2FRfKFfPjX8QdDjbA3QP%2FSz%2BMJQRyBSMsGsUTlLtsXD%2FitMul7ONd0z%2FpHzmNuELS1CNt7UzqpZNeSRfl60n6H1bKWCIG3dQtDyYc9JvaY3%2F9PuMW%2B03AMHV6dQETNEmTI4vKpEGVBoSPb5BuUCf06yXanW3rxmBT0AjVZ0aoZDTCxrBB%2F1%2FxYQBwJNAFue3VnUOwcT34sy89z7Njm6uy6d9EUTia0Jkkpud71wYuTdP1o1tTuAI5VdHiPz5CXteoe%2BgTN%2BAEo6jvzgIr5Vdx5QnaKjxbgdazqNoklRhlfFEPGxkU4cchEjGX6MjmepdownfuWajZfDeZ93kjwQDbgW8r6hFl%2BMcEjVZ9ERR22D%2BaKwjh1gSCd17HCQIYPfX2V0K2265uTudsRgH%2BC%2BkiPyEziytDHI0Y4JGN8DrTI%2F0QCnhiUqWkn9HbFosDYZIvZyK3Sz7OxgoWwoZ4CEelAxctY5',
    #     'umidGetStatusVal': '255',
    #     'screenPixel': '1847x1039',
    #     'navlanguage': 'zh-CN',
    #     'navUserAgent':
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    #     'navPlatform': 'Win32',
    #     'appName': 'taobao',
    #     'appEntrance': 'taobao_pc',
    #     '_csrf_token': 'UztBTtb4f7GHyohW7jYfk5',
    #     'umidToken': '0edb79dee16e589a59021dd9403088a717dccadd',
    #     'hsiz': '105127586344b04f01ef0427bdfc91c1',
    #     'bizParams': '',
    #     'style': 'default',
    #     'appkey': '00000000',
    #     'from': 'tbTop',
    #     'isMobile': 'false',
    #     'lang': 'zh_CN',
    #     'returnUrl': 'https://www.taobao.com/',
    #     'fromSite': '0',
    #     'umidTag': 'SERVER',
    #     'weiBoMpBridge': '',
    #     'deviceId': '',
    #     'pageTraceId': '2106cd6216910417297034426d04af',
    #     'bx-ua':
    #     '226!9Agx37T8blMvWbbv7bQiWx3u2twZOGpzS3Pj25WCmfP3Jux3VDczwmyLA6Cg/6mnxfrVQeCr94N7ZluYRHPLdXYNI042C6z3WTrBDsGBxoyBW7Ya4DnXGUjeEFZ3RifEnZbkDgTShqEwVqIyBwEs0T7Kj406xBHo1Iy2W63hK2fGgZ3E6gKWgn+1XGRprNJ7f0AFiBLaY4pJXcGNhNsjNp3oGLGGSys5LxuSBo3pD5+Vae2ygS5bEdOAs3JDQ5jzKBO8koD68XnRlwfAJ+t7cab73W9YjakgHlRGblUIDLGAHukeCJNJ/6j7SYDTRSWwzWNW0WsNQd1baMByC7JJMZ9pwSnSykgZbvoz4ER55cjchaWfR2BHnCRfMwUlF1QyJFMNZjA3+BYYmKwI0mlbd0fmQcDOz88aPGFTcqIzqj5whQfedBs2gB91vFlaneTR3BTlyKmhzO9O2/J6lA12gB9ZyVaHtNvlPfEKRDmR89BLhobhQmT3TJt/MDr+/vJHW1MxqoMvsqlo3Ualp9v20Q/q8D1n0RzfoznGyvTl4/ApD2T69h5wd7HwMhDH/vTGjTzaXuJb4tYJKqcu0DfedrSJdUwX/0DDOJic/Wi8bSx/hVwe6gvyJQeylo3JyOnrWTDkqsiu9ZtvotkzsDfJ6QYyMDr+u5ONDkDAes1MsKGnDZmn0WbpH7Zw6vvIyhTNAEoNROnMIyy52SvB/m3/+rX/wDEsEyQZ38OlRz7KlHAhLArSuSjzg8WbqU8UneNU38YtfVgbHO9ogUalp9eGrYyNIOa5ne7sgPLGGISxl0/Y3DkHpyvZXYeSJKly8yTJ38QHy2mcHO/Y7vGcd9vGg8/2yoQa8yzdwPQHh9ucT59W3U1FpXJ2gMHOwtskgV5mhnuCyUaEJcyOcso6q2b9+H9bpvOBXsv5hd0fyUuIwSX01b7Hy/sbnfX//yOfnyQ53IkvyKVnHmFo3gTeKDvGg8lDehM+sgbQ/lY7r6bhssUMjszAfBb0Wta8UXxKq1oIHVsNfkHNzWdMmLEAWFzQACB3ffQg0s7lF3Gl0A5urRX8A4q7NL2eGiEREhVeKvYvwV6McGKdYbqIv2snFr0ilh5ccYqgXXwFjbXSfhSFvWFmcftRhzTksW1uzGCb0wc60qxBz43G3q/87jZS9oa7Z5Zw9ahc8GyjiKmjyp0Pmv6s5Lifw3stPx5BQuojbo1weY0WFkxLofxZYkohmyKvoFvlbihBN4yrN5LYnES8uSBXdiPdD3436xrqxM7YAvnZLMeldWxzdI/4/gaVtARLbrcQl/yafnmHf97gbD6xMR3Vilf1db1pdm7KpOpS5yuATyzYSYaSnfrKhyEmtJ7Nx+gghYqS7fWm+sk58yz0kxhgaCWElYAmCiVz/ohcYFnUuiJ/h7HpkyZzh6xn8fhq5bK2pWYRAEzISgyaVBhaCR9CsOhmRAL/jA9K0VdOHoioAJB6rfDSJ2lzQK56bsHjhmJ1tCJaYdIv4u1dO6yswV3+Vz57S7TNZuLE8s1AeTJmS3RYSWx+lr9ACgGpMQMTmoLFbbB3nfIsBIsGsUT/FIaHuB+uiEhKqF94tolEAkglDR1fTIFgBgtculWdwoJZT2A0xIuIUPt/GuXTbb==',
    #     'bx-umidtoken': 'G9BD3F5125478ADE7CF2A58A275282E1C7696E55BDD5E3350F4'
    # }

    # response = requests.post(url, headers=headers, data=data)
    response = requests.get(url)

    print(response.status_code)
    # print(response.text)


class PyppteerChromeBrowser:

    def __init__(self, proxy=None):

        # 初始化浏览器配置
        self.options = {
            # 'ignoreDefaultArgs': ['--enable-automation'],  # 去掉检测驱动提示
            # 设置浏览器外观
            'args': [
                "--start-maximized",
                # "--window-size=1920,1080",
                # '--disable-infobars',
                # '--no-sandbox',  # Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
            ],
            # 'dumpio':
            # True,  # 把无头浏览器进程的 stderr 核 stdout pip 到主程序，也就是设置为 True 的话，chromium console 的输出就会在主程序中被打印出来
            # 'logLevel':
            # 'ERROR'
        }

        if proxy:
            self.options['args'].append(f'--proxy-server={proxy}')

        # self.path = '/usr/bin/google-chrome-stable'
        self.path = '/usr/bin/google-chrome-stable'

    async def __aenter__(self):
        self.browser = await launch(
            headless=False,  # 必须为 True，否则报错：Most likely you need to configure your SUID sandbox correctly
            options=self.options,
            executablePath=self.path)
        # self.chrome_process_id = self.browser.process.pid
        return self.browser

    async def __aexit__(self, type, value, traceback):
        try:
            await self.browser.close()
        except Exception as e:
            print("关闭浏览器失败，error：{}".format(e))

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
        # before_move_content = await page.content()

        # div = await page.querySelector('div[id="page"]'
        #                                )  # 可以拿到 “请按住滑块，拖动到最右边” 区域内容
        # div = await page.querySelector('iframe[id="baxia-dialog-content"]')
        # div_text = await page.evaluate('(element) => element.textContent', div)
        # print("Text content of the element:", div_text)
        # body = await page.querySelector("body[class='chl-reg']")
        # scripts = await page.querySelector('script')

        # result = await page.evaluate(scripts)

        # 模拟鼠标滑动
        await page.hover('#nc_1_n1z')

        await page.mouse.down()

        slider = await page.querySelector('.nc-lang-cnt')

        position = await slider.boundingBox()

        track = self.handle_distance(position['x'])

        for dis in track:
            await page.mouse.move(page.mouse._x + dis, page.mouse._y, {'delay': random.randint(500, 1000), 'steps': 3})

        await page.mouse.up()


async def iframe(page):
    iframe = await page.Jx('//iframe[id="J_Member"]')
    # page = await page.waitForSelector('iframe')

    if not iframe:
        return page

    for item in iframe:
        iframe_url = await page.evaluate('item => item.src', item)

    await page.goto(iframe_url)
    await page.waitForNavigation(waitUntil='networkidle0')
    await asyncio.sleep(2)

    return page


def login_pyppteer(url):

    async def open_taobao(url):

        pyppteer_instance = PyppteerChromeBrowser()

        for i in range(1, 21):
            async with pyppteer_instance as browser:
                page = await browser.newPage()
                await page.setUserAgent(
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/104.0.0.0 Safari/537.36')
                await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面大小
                await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                                 '{ webdriver:{ get: () => false } }) }')  # 去掉驱动检测

                await page.setJavaScriptEnabled(enabled=True)
                # 防止页面识别出脚本(反爬虫关键语句)
                await stealth(page)

                await page.goto(url, timeout=60000)

                enter_content = await page.content()
                page = await iframe(page)

                # print(enter_content)

                element = await page.querySelector('a[class="h"]')
                bounding_box = await element.boundingBox()

                if bounding_box:
                    # Calculate the coordinates of the center of the element
                    x = bounding_box['x'] + bounding_box['width'] / 2
                    y = bounding_box['y'] + bounding_box['height'] / 2

                    # Move the mouse cursor to the center of the element
                    await page.mouse.move(x, y)
                    await page.mouse.click(x, y)
                    await page.waitForNavigation(waitUntil='networkidle0', timeout=100000)

                    await asyncio.sleep(2)

                enter_content = await page.content()

                before_input_content = await page.content()

                username = await page.querySelector('input[name="fm-login-id"]')
                await username.type('2427219623@qq.com')
                # await asyncio.sleep(3)
                password = await page.querySelector('input[name="fm-login-password"]')
                await password.type("feng33314")
                # await asyncio.sleep(3)
                after_input_content = await page.content()

                await asyncio.sleep(5)

                submit = await page.querySelector("button[class='fm-button fm-submit password-login']")
                if not submit:
                    pass
                await submit.click()

                after_submit_content = await page.content()

                # logined = re.findall(r'userid=\d+&', after_submit_content)

                if '<input type="hidden" name="ua"' in after_submit_content:

                    await page.close()
                    print("完成第{}次登录".format(i))

                    continue
                
                await pyppteer_instance.move_to_gap(page)  # 移动滑块
                await asyncio.sleep(2)

            result_content = await page.content()  # 最终数据内容
            await asyncio.sleep(2)

        print('登录结束')

    asyncio.run(open_taobao(url))


if __name__ == "__main__":
    url = "https://www.taobao.com/"
    # nc_src = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.5.1"

    login_pyppteer(url)
    # login_interface()
    print("-" * 50 + "end" + "-" * 50)
