from math import ceil
import os
import re, random
import time

import scrapy
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse

from . import base_spider
from ..common_tools import tools

captcha_instance = tools.captcha_instance


class WhoClinicSpider(base_spider.CustomBasePyppeteerSpider):
    name = 'who_clinic'
    allowed_domains = ['www.chictr.org.cn']

    custom_settings = {
        "MONGODB_COLLECTION_NAME": f'results_{name}',
        "SUBPATH": name,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 50,
        'TOTAL_PAGE': 6569,
        'HOME_PAGE': 'http://www.chictr.org.cn/searchproj.aspx'
    }

    public_content = {
        "province": "中国",
        "website_name": "中国临床试验注册中心",
        "website_domain": "http://www.chictr.org.cn/searchproj.aspx",
        "crawl_frequence": "一周一次",
        "website_location": "首页 > 检索入口 > 检索试验",
    }

    start_url = 'http://www.chictr.org.cn/searchproj.aspx'

    next_url = 'http://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode=&page={}'

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

    err_types = {
        'slider': '滑块验证',
        'image_code': '图片识别验证码',
        'image_code_failure': '图片验证码失败',
        'unkonwn': '其他错误'
    }

    total_page = 6500

    def start_requests(self):

        yield scrapy.Request(
            url=self.start_url,
            headers=self.headers,
            meta={'usedSelenium': True},
        )

    def parse(self, response):

        all_tr = response.xpath('//table[@class="table_list"]/tbody/tr')

        if not all_tr:
            raise Exception("Invalid page, url: {}".format(response.url))

        for tr in all_tr[1:]:

            all_td = tr.xpath("td")

            revisions_url = 'http://{}/{}'.format(
                self.allowed_domains[0], all_td[0].xpath('a/@href').get())

            detail_url = 'http://{}/{}'.format(
                self.allowed_domains[0],
                all_td[2].xpath('p/a/@href').get())  # 详情页地址

            info = {
                'registration_number':
                base_spider.extract_value([all_td[1].xpath('string(.)').get()
                                           ]),  # 注册号
                'registered_topic':
                all_td[2].xpath('string(.)').get(),  # 注册题目
                # 'study_type':
                # base_spider.extract_value([all_td[3].xpath('string(.)').get()
                #                            ]),  # 研究类型
                'registration_date':
                base_spider.extract_value([all_td[4].xpath('string(.)').get()
                                           ]),  # 注册时间
                'detail_url':
                detail_url,
                'parent_url':
                response.url
            }

            yield scrapy.Request(url=detail_url,
                                 headers=self.headers,
                                 callback=self.parse_detail,
                                 meta={'info': info},
                                 dont_filter=True)

        if 'page=' in response.url:

            cur_page = int(response.url.split('page=')[-1])

        else:
            cur_page = 1

            self.total_page = int(
                response.xpath('string(//div[@id="pgProj"]/span)').re(
                    '共(\d+)页')[0])

        meta = response.meta
        failure_page = meta.get('failure_page')

        if failure_page:

            if ceil(cur_page / 10) == ceil(failure_page / 10):  # 在同一页数栏
                print(
                    '失败页数与当前页在同一栏，无需页数栏翻页，cur_page：{}，failure_page：{}'.format(
                        cur_page, failure_page))

                next_page_elem = self.driver.find_elements(
                    'xpath',
                    '//a[@onclick="serchPage({})"]'.format(failure_page))
                meta['failure_page'] = None

            elif ceil(cur_page / 10) < ceil(failure_page / 10):  # 需要对页数栏进行翻页
                print('失败页数大于11，需页数栏翻页，cur_page：{}，failure_page：{}'.format(
                    cur_page, failure_page))

                if cur_page % 10 == 0:  # 页数栏进行翻页操作
                    next_page_elem = self.driver.find_elements(
                        'xpath', '//a[contains(text(), "下一页")]')
                    print('当前页数为页数栏最后一页，需要点击翻页，cur_page：{}，failure_page：{}'.
                          format(cur_page, failure_page))

                else:  # 点击当前页数栏最后一页
                    next_page_elem = self.driver.find_elements(
                        'xpath', '//a[@onclick="serchPage({})"]'.format(
                            ceil(cur_page / 10) * 10))
                    print('当前页数不是页数栏最后一页，需要点击翻页，cur_page：{}，failure_page：{}'.
                          format(cur_page, failure_page))

            else:
                raise Exception('出现不合理情况，failure_page：{}，cur_page：{}'.format(
                    failure_page, cur_page))

        else:
            print('没有失败页，继续后续步骤，cur_page：{}，failure_page：{}'.format(
                cur_page, failure_page))
            next_page_elem = self.driver.find_elements(
                'xpath', '//a[contains(text(), "下一页")]')

        if not next_page_elem:

            if re.search(r"滑动验证页面", self.driver.page_source):
                print('{} 出现滑块'.format(self.driver.current_url))
                return

            elif self.driver.find_elements("id", "ui-dialog-title-1"):
                print('验证码验证失败，url：{}'.format(self.driver.current_url))

                match = re.search(r'&page=(\d*)',
                                  self.driver.current_url).group(1)
                failure_page = int(match)

                meta['usedSelenium'] = True
                meta['failure_page'] = failure_page

                yield scrapy.Request(self.start_url,
                                     headers=response.request.headers,
                                     meta=meta)

            elif cur_page == self.total_page:
                print('已抓取完最后一页，结束')
                return

            else:
                raise Exception('出现未知情况')

        else:

            yield HtmlResponse(url=response.url,
                               body=self.driver.page_source,
                               request=response.request,
                               encoding='utf-8',
                               status=200)

            next_page_elem = next_page_elem[0]
            # 正常数据显示的网页

            next_page_elem.click()

            time.sleep(3)

            if self.driver.find_elements(
                    'xpath',
                    '//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all  ui-draggable ui-resizable"]'
            ):
                self.verify_img_code()

                yield HtmlResponse(url=self.driver.current_url,
                                   body=self.driver.page_source,
                                   request=response.request,
                                   encoding='utf-8',
                                   status=200)
                # verify_code_img = self.driver.find_element(
                #     "id", "imgVerify").screenshot_as_png  # 由于验证码图片动态改变，因此需要截图

                # verify_code = captcha_instance.captcha_handler_by_content(
                #     verify_code_img)

                # url = self.get_next_page(self.driver.current_url, verify_code)

                # yield scrapy.Request(url,
                #                      headers=response.request.headers,
                #                      meta={'usedSelenium': True})

            # next_page = cur_page + 1

            # if next_page > self.total_page:
            #     return

            # if next_page > 10:
            #     return

            # next_url = self.next_url.format(next_page)

            # yield scrapy.Request(next_url,
            #                      headers=self.headers,
            #                      meta={'usedSelenium': True})

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

    def get_cur_page(self):

        match = re.search(r'&page=(\d*)', self.driver.current_url)

        if match:

            cur_page = int(match.group(1))

        else:
            cur_page = 1

        return cur_page

    def get_next_page(self, current_url, code):

        match, page = re.search(r'verifycode=(.*)&page=(\d+)',
                                current_url).groups()

        url = current_url.replace(match, code).replace(page, page + 1)

        return url

    def parse_revisions(self, response):

        all_tr = response.xpath('//table[@class="table_list"]/tbody/tr')

        revisions = []

        for tr in all_tr[1:]:

            all_td = tr.xpath("td")

            operation = all_td[3].xpath('p/a/@onclick').get().split(
                ',')[0].split("'")[1]

            revisions.append({
                'version':
                base_spider.extract_value([all_td[0].xpath('string(.)').get()
                                           ]),
                'registration_id':
                base_spider.extract_value([all_td[1].xpath('string(.)').get()
                                           ]),
                'updated_date':
                base_spider.extract_value([all_td[2].xpath('string(.)').get()
                                           ]),
                'operation_url':
                'http://{}/{}'.format(self.allowed_domains[0], operation)
            })

        info = response.meta['info']

        info['revisions'] = revisions

        yield scrapy.Request(url=info['detail_url'],
                             headers=self.headers,
                             callback=self.parse_detail,
                             meta={"info": info})

    def parse_detail(self, response):

        title = base_spider.extract_value(
            [response.xpath('//div[@class="ProjetInfo_title"]/text()').get()])

        info = response.meta['info']

        yield {
            **self.public_content,
            **{
                'data': [{
                    **info,
                    **{
                        'title': title
                    }
                }]
            }
        }

    def amend_filename(self, filename):

        for i in {'<', '>', '/', '\\', '|', ':', '"', '*', '?', ' '}:

            filename = filename.replace(i, '')

        return filename

    def slider_page(self, response, page):
        return response.request

    def image_code_page(self, response, page):

        img_time = random.random()

        img_url = f'https://www.chictr.org.cn/Tools/verifyimagepage.aspx?textcolor=2&bgcolor=F4F4F4&ut=1&time={img_time}'

        verifycode = tools.captcha_instance.captcha_handler(
            img_url, self.headers)

        url = f'https://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode={verifycode}&page={page}'

        return scrapy.Request(url,
                              headers=response.request.headers,
                              meta=response.request.meta,
                              callback=response.request.callback)

    def image_code_failure_page(self, response, page):

        url = self.next_url.format(page)

        headers = response.request.headers

        headers['referer'] = self.next_url.format(page - 1)

        return scrapy.Request(url,
                              headers=headers,
                              meta=response.request.meta,
                              callback=response.request.callback)

    def error_page_type(self, response):

        if re.search(r"滑动验证页面", response.text):

            div = response.xpath('//div[@class="waf-nc-h5-panel"]')

            traceid = response.xpath("//div[@id='traceid']/text()").get()

            return 'slider'

        if response.xpath('//div[@class="dlgVerifyCode"]/@style').get(
        ) != 'display: none;':

            return 'image_code'

        if re.search(r'请填写正确的验证码', response.text):

            return 'image_code'

        return 'unkonwn'
