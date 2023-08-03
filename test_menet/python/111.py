# -*- coding: utf-8 -*-
# @Time    : 2022-08-18 21:39
# @Author  : Kevin_Wang
# @File    : henan.py

import asyncio
import aiohttp
import re
import random
import time
import settings
import requests
from lxml import etree
from pyppeteer import launch
from redis import StrictRedis
from img2xy import img2xy
from logger import Logger
from pipeline import Pipeline
from scheduler import Scheduler


class Henan:

    def __init__(self):
        self.logger = Logger()
        self.client = StrictRedis()
        self.pipe = Pipeline()
        self.sch = Scheduler()

    def on_close(self):
        self.client.close()
        self.pipe.on_close()
        self.sch.on_close()

    def get_proxies(self):
        if settings.PACK:
            url = f'http://d.jghttp.alicloudecs.com/getip?num={settings.PROXY_NUM}&type=2&pro=0&city=0&yys=0&port=11&' \
                  f'pack={settings.PACK}&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        else:
            url = f'http://d.jghttp.alicloudecs.com/getip?num={settings.PROXY_NUM}&type=2&pro=0&city=0&yys=0&port=11&time' \
                  f'=4&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

        resp = requests.get(url).json()
        if not resp['code']:
            print('代理请求成功')
            # logger.info(f'共拿到{len(resp["data"])}个代理')
            for ip_info in resp['data']:
                ip = ip_info['ip']
                port = ip_info['port']
                ip_add = ip + ':' + str(port)
                self.client.sadd(settings.PROXY_KEY, ip_add)
        else:
            print(f'代理请求失败:{resp["code"]}:{resp["msg"]}')
            if resp['code'] == 121:
                # 代理两秒内只能请求一次
                time.sleep(2)
                print('套餐用完，更换为按次提取')
                settings.PACK = None
                self.get_proxies()
            elif resp['code'] == 111:
                print('代理拿得太频繁，稍等一会儿')
                time.sleep(2)
                # self.pack = None
                self.get_proxies()
            elif resp['code'] == 113:
                print(resp['msg'])
                exit()
            else:
                time.sleep(1)
                print(resp['code'], resp['msg'])
                # print('222', dir(crawler))
                print('代理获取失败')
                exit()

    async def init_browser(self, proxy=None):
        # 初始化浏览器配置
        args = [
            "--start-maximized",
            "--window-size=1920,1080",
            '--disable-infobars',
        ]
        if proxy:
            args.append(f'--proxy-server={proxy}')
        browser = await launch(headless=True, args=args)

        return browser

    @staticmethod
    def slide_track(distance):
        """滑动轨迹"""
        track = []
        v = 0
        t = 1
        cur = 0
        mid = distance * 3 / 5
        while cur < distance:
            if cur < mid:
                a = 0.4
            else:
                # 滑动过半开始减速
                a = -0.5
            v0 = v
            s = v0 * t + 0.5 * a * (t**2)
            cur += s
            track.append(s)
            v = v0 + a * t

        return track

    @staticmethod
    def slide_distance(gap_x):

        init_x, rate = 50, 0.5059523809523809

        # 滑动距离计算
        distance = gap_x * rate - init_x + 12

        return distance

    @staticmethod
    async def get_captcha_img(url, proxy=None):
        """请求验证码图片"""
        headers = {
            'Accept':
            'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 't.captcha.qq.com',
            'Pragma': 'no-cache',
            'Referer': 'https://t.captcha.qq.com/template/drag_ele.html',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        if proxy:
            proxy = 'http://' + proxy

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url=url, proxy=proxy,
                                       timeout=10) as resp:
                    img = await resp.content.read()
                    return img
        except Exception as e:
            print(f'get captcha img <{url}> wrong:', e)
            return

    async def school_score(self, browser, req):
        # url = 'http://www.haeea.cn/adc/pzyxpxtdx2022w.shtml'

        page = await browser.newPage()
        # 设置页面参数
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/104.0.0.0 Safari/537.36')
        await page.setViewport({'width': 1920, 'height': 1080})
        await page.evaluateOnNewDocument(
            '() =>{ Object.defineProperties(navigator,'
            '{ webdriver:{ get: () => false } }) }')
        try:
            await page.goto(req['url'])
            frame = page.frames[1]

            await frame.type('#querytxt', req['school_code'])
            # await frame.waitFor(100)
            await frame.click('#TencentCaptcha')

            # 等待加载新的iframe
            await frame.waitFor('#tcaptcha_iframe_dy', timeout=15000)
            captcha_frame = page.frames[-1]
            await captcha_frame.waitForXPath('//div[@class="tc-fg-item"]',
                                             timeout=15000)
            html = await captcha_frame.content()
            # 提取验证码图片链接，
            img_urls = re.findall(
                r'background-image: url\(&quot;(.*?)&quot;\)', html, re.S)
            bg_url = 'https://t.captcha.qq.com'
            fg_url = ''
            for img_url in img_urls:
                if 'img_index=0' in img_url:
                    fg_url = 'https://t.captcha.qq.com' + img_url.replace(
                        'amp;', '').replace('**', '')
                else:
                    bg_url += img_url.replace('amp;', '').replace('**', '')
            bg = await self.get_captcha_img(bg_url, req['proxy'])
            fg = await self.get_captcha_img(fg_url, req['proxy'])

            if bg and fg:
                # 识别缺口位置
                gap_pos = img2xy(bg, fg)
                # 计算需要滑动的距离
                slide_dis = self.slide_distance(gap_pos[0])
                # 生成滑动轨迹
                track = self.slide_track(slide_dis)

                # 模拟鼠标滑动
                await captcha_frame.hover('.tc-slider-normal')
                await page.mouse.down()
                # await page.waitFor(100)
                for dis in track:
                    await page.mouse.move(page.mouse._x + dis, page.mouse._y, {
                        'delay': random.randint(1000, 2000),
                        'step': 3
                    })
                # await page.waitFor(100)
                await page.mouse.up()
                # await page.waitFor(10)
                # 滑动后等待页面加载
                try:
                    await frame.waitForFunction(
                        'document.querySelector("#TencentCaptcha").innerText == "验证成功"',
                        timeout=15000)

                    await frame.click('#QueryBtn')
                    # 点击查询按钮后等待数据返回
                    await frame.waitFor('#tabInfo', timeout=15000)

                    frame_content = await frame.content()
                    # print(frame_content)
                    # 解析返回的数据
                    info = self.parse_info_table(frame_content)
                    await page.close()
                    if info:
                        # 给每条记录加上批次
                        for i in range(len(info)):
                            info[i] = [req['batch_text']] + info[i]

                        # 回收代理
                        if req['proxy']:
                            self.client.sadd(settings.PROXY_KEY, req['proxy'])
                        self.pipe.process_items(info)
                        self.logger.info(
                            f'get {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}]'
                        )
                    else:
                        self.logger.info(
                            f'get {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] response none'
                        )
                        self.retry(req)

                except Exception as e:
                    self.logger.error(
                        f'get {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] captcha verify failed: {e}'
                    )
                    if isinstance(e, TimeoutError) and req['proxy']:
                        self.client.sadd(settings.PROXY_KEY, req['proxy'])
                    self.retry(req)
                    await page.close()
            else:
                self.logger.error(
                    f'get {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] captcha img failed'
                )
                self.retry(req)
                await page.close()
        except Exception as e:
            self.logger.error(
                f'get {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] wrong: {e}'
            )
            if isinstance(e, TimeoutError) and req['proxy']:
                self.client.sadd(settings.PROXY_KEY, req['proxy'])
            self.retry(req)
            await page.close()

    def retry(self, req):
        req['retry_times'] = req.get('retry_times', 0) + 1
        if req['retry_times'] < settings.MAX_RETRY_TIMES:
            self.logger.info(
                f'retrying {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] {req["retry_times"]} times'
            )
            self.sch.enqueue(req)
        else:
            self.logger.info(
                f'give up retrying {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}]'
            )

    @staticmethod
    def parse_info_table(html_text):
        if '未查询到相关信息' in html_text:
            return []
        html = etree.HTML(html_text)
        trs = html.xpath('//table[@id="tabInfo"]/tbody/tr')
        fsx_xx = []
        for tr in trs[2:]:
            tds = tr.xpath('td')
            item = []
            for td in tds:
                td_text = td.xpath('text()')
                td_text = td_text[0] if td_text else ''
                item.append(td_text)
            fsx_xx.append(item)

        return fsx_xx

    async def run(self, req):

        # 一个浏览器开多个页面
        # browser = await self.init_browser()
        url = settings.batch_url.get(f'{req["batch_text"]}_{req["wenli"]}', '')
        if not url:
            self.logger.error(
                f'cant find url key: {req["batch_text"]}_{req["wenli"]}')

        if url:
            proxy = None
            if settings.USE_PROXY:
                if not self.client.exists(settings.PROXY_KEY):
                    self.get_proxies()
                proxy = self.client.spop(settings.PROXY_KEY).decode()
                self.logger.info(f'using proxy: {proxy}')
            # 多个浏览器开多个页面
            browser = await self.init_browser(proxy)
            try:
                await self.school_score(
                    browser, {
                        'url': url,
                        'school_code': req['school_code'],
                        'batch_text': req["batch_text"],
                        'wenli': req["wenli"],
                        'proxy': proxy
                    })
            except Exception as e:
                self.logger.error(
                    f'run {req["batch_text"]}[{req["wenli"]}][{req["school_code"]}] error: {e}'
                )
                self.retry(req)
            finally:
                await browser.close()

    def get_school_codes(self, batch, wenli):
        sql = f"select distinct wenli, batch_text, school_code from ga_zy_specialplan where province_id = 16 " \
              f"and stat = 1 and years = 2022 and batch_text in ('{batch}') and wenli in ({wenli})"

        try:
            self.pipe.cursor.execute(sql)
            school_codes = self.pipe.cursor.fetchall()

            return school_codes
        except Exception as e:
            self.logger.error(f'query specialplan error: {e} -> sql: {sql}')

    def main(self, batch, wenli):
        self.logger.info('spider start')
        loop = asyncio.get_event_loop()
        if not self.sch.has_req():
            batch_text = "','".join(batch)
            wenli_text = ','.join([str(w) for w in wenli])
            req_info = self.get_school_codes(batch_text, wenli_text)
            for item in req_info:
                self.sch.enqueue(item)

        while self.sch.has_req():
            try:
                reqs = []
                for _ in range(settings.REQUEST_NUM):
                    if self.sch.has_req():
                        req = self.sch.next_req()
                        reqs.append(asyncio.ensure_future(self.run(req)))

                loop.run_until_complete(asyncio.wait(reqs))
                time.sleep(1)
            except Exception as e:
                self.logger.error(f'main run error: {e}')

        self.on_close()
        self.logger.info('spider close')


if __name__ == '__main__':
    henan = Henan()
    henan.main(['本科一批', '本科二批'], [1, 2])