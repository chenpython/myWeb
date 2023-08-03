import re
import string
import scrapy

from ...menet.menet.spiders import base_spider

from ...menet.menet.common_tools import const


class HunanPharmaceuticalServiceNetworkSpider(base_spider.CustomBaseSpider):

    name = 'hunan_pharmaceutical_service_network_debug'

    allowed_domains = ['www.hnysfww.com']
    start_url = 'https://www.hnysfww.com/article_cat.php?id=61'

    custom_settings = {
        'MONGODB_COLLECTION_NAME': f'results_{name}',
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.5
    }

    headers = {
        "Host": "www.hnysfww.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "sec-ch-ua":
        '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.hnysfww.com/article_cat.php?id=61",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }

    public_content = {
        "province": "湖南省",
        "website_name": "湖南药事服务网",
        "website_domain": "https://www.hnysfww.com/article_cat.php?id=61",
        "crawl_frequence": "一周一次",
        "website_location": "首页 > 药讯中心 > 指南•规范•共识",
    }

    total_page = 10

    exclude_urls = {
        'https://www.hnysfww.com/article.php?id=679',
        'https://www.hnysfww.com/article.php?id=874',
        'https://www.hnysfww.com/article.php?id=875'
    }

    def start_requests(self):
        start_urls = [
            'https://www.hnysfww.com/article.php?id=2654',
            'https://www.hnysfww.com/article.php?id=2627',
            'https://www.hnysfww.com/article.php?id=2094',
            'https://www.hnysfww.com/article.php?id=1822',
            'https://www.hnysfww.com/article.php?id=1765',
            'https://www.hnysfww.com/article.php?id=1743',
            'https://www.hnysfww.com/article.php?id=1725',
            'https://www.hnysfww.com/article.php?id=1652',
            'https://www.hnysfww.com/article.php?id=874',
            'https://www.hnysfww.com/article.php?id=875',
            'https://www.hnysfww.com/article.php?id=818',
            'https://www.hnysfww.com/article.php?id=679',
            'https://www.hnysfww.com/article.php?id=256'
        ]

        return [
            scrapy.Request(url=url,
                           headers=self.headers,
                           meta={'page_info': url},
                           callback=self.parse_detail) for url in start_urls
        ]

    def parse(self, response):

        self.headers['Referer'] = response.url

        news = response.xpath('//ul[@class="newsbox"]/li/a/@href')

        self.logger.info('{} 获取 {} 个公告'.format(response.url, len(news)))

        for news_ in news:

            detail_url = 'https://{}/{}'.format(self.allowed_domains[0],
                                                news_.get())

            if detail_url not in {
                    'https://www.hnysfww.com/article.php?id=2654',
                    'https://www.hnysfww.com/article.php?id=2627',
                    'https://www.hnysfww.com/article.php?id=2094',
                    'https://www.hnysfww.com/article.php?id=1822',
                    'https://www.hnysfww.com/article.php?id=1765',
                    'https://www.hnysfww.com/article.php?id=1743',
                    'https://www.hnysfww.com/article.php?id=1725',
                    'https://www.hnysfww.com/article.php?id=1652',
                    'https://www.hnysfww.com/article.php?id=874',
                    'https://www.hnysfww.com/article.php?id=875',
                    'https://www.hnysfww.com/article.php?id=818',
                    'https://www.hnysfww.com/article.php?id=679',
                    'https://www.hnysfww.com/article.php?id=256'
            }:
                continue
            yield scrapy.Request(url=detail_url,
                                 headers=self.headers,
                                 meta={'page_info': response.url},
                                 callback=self.parse_detail,
                                 dont_filter=True)

        if 'page=' not in response.url:

            next_page = 2

            self.total_page = int(
                response.xpath('//a[contains(text(), "最末页")]/@href').get().
                split('page=')[-1])

        else:

            cur_page = response.url.split('page=')[-1]

            next_page = int(cur_page) + 1

        if next_page > self.total_page:
            return

        next_url = '{}&page={}'.format(self.start_url, next_page)

        self.logger.info('下一页地址：{}'.format(next_url))

        yield scrapy.Request(url=next_url,
                             headers=self.headers,
                             dont_filter=True)

    def parse_detail(self, response):

        self.logger.info('{} 进入详情页'.format(response.url))

        title = response.xpath("//div[@class='nrbox_title']/text()").get()

        attachments = []

        if response.url not in self.exclude_urls:

            self.file_handler(response, '//div[@class="conbox"]//a', title,
                              'https://{}'.format(self.allowed_domains[0]),
                              'tmp', attachments)

            if attachments:
                attachments = self.remove_duplicates(attachments)

        self.logger.info("{} 总共有 {} 个附件".format(response.url,
                                                len(attachments)))

        parent_page = response.meta['page_info']

        yield {
            **self.public_content,
            **{
                'data': [{
                    'title': title,
                    "attachments": attachments,
                    "url": response.url,
                    'parent_page': parent_page
                }]
            }
        }

    def remove_duplicates(self, files_map):

        new_files_map = []

        exists_url = set()

        for item in files_map:

            if item['file_url'] in exists_url:
                continue

            exists_url.add(item["file_url"])

            new_files_map.append(item)

        return new_files_map

    def check_a_link(self, href):

        if not super().check_a_link(href):
            return False

        if href.split('.')[
                -1] not in const.VALID_FILE_SUFFIX + const.VALID_IMAGE_SUFFIX:
            return False

        return True

    def filename_hook(self,
                      file_name_xpath,
                      file_selector,
                      href,
                      index,
                      response=None):

        filename = file_name_xpath + '（{}）.'.format(index +
                                                    1) + href.split('.')[-1]

        filename = base_spider.format_filename(filename)

        return filename

    def file_handler(self, response: scrapy.http.response.html.HtmlResponse,
                     file_link_xpath: string, file_name_xpath: string,
                     website_domain: string, folder_name: string,
                     files_map: list):

        files = response.xpath(file_link_xpath)

        for index, file_ in enumerate(files):

            href = file_.attrib.get('href')

            if not self.check_a_link(href):
                continue

            filename = self.filename_hook(file_name_xpath=file_name_xpath,
                                          file_selector=file_,
                                          href=href,
                                          index=index,
                                          response=response)

            if not filename:
                continue

            file_url = self.file_url_hook(href,
                                          website_domain,
                                          response=response)

            files_map.append({
                'filename': filename,
                "file_url": file_url,
                "ori_url": href
            })