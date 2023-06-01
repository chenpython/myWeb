import scrapy
from lxml import etree

from . import base_spider


class AmazonSellers(base_spider.CustomBaseSpider):

    name = 'amazon_sellers'
    custom_settings = base_spider.CustomBaseSpider.custom_settings.copy()
    custom_settings.update({
        "MONGODB_COLLECTION_NAME": f'results_{name}',
        "SUBPATH": name
    })

    allowed_domains = ['www.amazon.sg']

    public_content = {
        "province": "美国",
        "crawl_frequence": "一周一次",
        "website_name": "亚马逊",
    }

    headers = {
        'Host': 'www.amazon.sg',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'device-memory': '8',
        'sec-ch-device-memory': '8',
        'dpr': '1.0399999618530273',
        'sec-ch-dpr': '1.0399999618530273',
        'viewport-width': '1847',
        'sec-ch-viewport-width': '1847',
        'rtt': '350',
        'downlink': '1.35',
        'ect': '3g',
        'sec-ch-ua':
        '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Service-Worker-Navigation-Preload': 'true',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    cookies = {
        'session-id':
        '358-6440405-3020822',
        'i18n-prefs':
        'SGD',
        'ubid-acbsg':
        '357-4656707-7810308',
        's_cc':
        'true',
        's_vnum':
        '2117433079550%26vn%3D1',
        's_sq':
        '%5B%5BB%5D%5D',
        's_ppv':
        '67',
        's_nr':
        '1685433088507-New',
        's_dslv':
        '1685433088510',
        'lc-acbsg':
        'en_SG',
        'x-acbsg':
        '"R2Xvl85kdhj@Yqhio3?6FNpqjU6ctOpONN?ABcgYnzYb6PAxKlP60tNwelx?Hfb2"',
        'at-acbsg':
        'Atza|IwEBIK8qxO73teC3kGKMrapx8WhJoSkPgSxmQMwkvDLHAiM56RQc9F9w_9mrvpYcZD1EwCxw5q_fcV7mNO6hhPVj_b1iiW5ZpGMIdGB5KYPwmhRoMZvnTWWB9WljGfoSgUcpMm6hZIIPZrTxEIt-ArwBdO4qJZg0LfjgBWObPljcsGLfX2TuS7MifqkaPLP6Ytf4-JB8z68moHinlv-DzyOnLa-Ic1G-jGDzDztkiaQW1nl3FA',
        'sess-at-acbsg':
        '"ExJD9RteBXRGRlrsHV5bLLKBDN+akIvJXpGs0SQkDeY="',
        'sst-acbsg':
        'Sst1|PQE1Ul55_d_agEfzhHRYTGgaCR9xMEiSnLjX3O59XSOf142-5-v-HjE-8bNSJ7ZhaUC_2Vu-UXjgWR9TV19RTJtN2v7BE2adofvvtpG2kTpyCEQBzlO6mtWUeiaMfomSJJBFylYJj1nEmNyVH9LTowBr_IDkjl9y5kX0IX-JTQeGB-Qzu4hmQLkSPjZFulcQV5lURZkBTVVbJzWD6rDe4JQlpQ4lbQyurL87p1ZpSBhaaTHoMDO3Av2XDw-eoKzkCUKtAg_7GqnV53OnYEAHX458yiQXANVOg-coXrNsV-odobo',
        'session-id-time':
        '2082787201l',
        'session-token':
        'ozwnRvHxiMPcetcQspujI+yfrYs/VqFWKVBI+iRNOxLTnDZX1/AeXhjKU9I43pE5MzIvwSPWgjmJzd2AflzEBDn7n6d/T93HBMpiQFlAThccZZBlmmxau61oJv7l49ftuNOPqiz8Gix1uO51RIYY4pL5wjVyiETwCCpUuGoPU6In0jQO832t3ODzOpXmBTPFJoZaY/o+b51tFwUDZYX73oGl/fTFjxjZHMski9n8JjuQM5OeDehE2Q==',
        'csm-hit':
        'tb:6MGHQPTDKG35CVRQ797K+s-MDQCKGP9ENZE8MA2QC6G|1685436535012&t:1685436535012&adb:adblk_no'
    }

    def start_requests(self):

        yield scrapy.Request(
            'https://www.amazon.sg/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2',
            headers=self.headers,
            cookies=self.cookies)

    def parse(self, response, **kwargs):

        selector = etree.HTML(response.text)

        a_links = selector.xpath('//div[@role="group"]//a')

        for a in a_links:
            menu_url = 'https://www.amazon.sg{}'.format(a.get('href'))
            yield scrapy.Request(menu_url,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse_sub_menu)

    def parse_sub_menu(self, response, **kwargs):
        info = response.meta.get('info', {})
        p_type_list = info.get('所属分类', [])
        if not p_type_list:
            info['所属分类'] = p_type_list
        selector = etree.HTML(response.text)
        p_type = selector.xpath(
            '//span[@class="_p13n-zg-nav-tree-all_style_zg-selected__1SfhQ"]'
        )[0].text
        p_type_list.append(p_type)

        a_links = selector.xpath('//div[@role="group"]//a')
        for a in a_links:
            menu_url = 'https://www.amazon.sg{}'.format(a.get('href'))
            yield scrapy.Request(menu_url,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse_sub_menu,
                                 meta={'info': {
                                     '所属分类': p_type_list
                                 }})

        goods = selector.xpath('//div[@id="gridItemRoot"]')
        for goods_ in goods:
            selector_new = etree.HTML(
                etree.tostring(goods_, encoding=response.encoding).decode(
                    response.encoding))
            goods_name = selector_new.xpath(
                '//a[@class="a-link-normal"]/span/div')[0].text
            graders_num = 0
            graders_num_match = selector_new.xpath(
                '//span[@class="a-size-small"]')
            if graders_num_match:
                graders_num = int(graders_num_match[0].text.replace(',', ''))
            info.update({
                '商品名': goods_name,
                '评分人数': graders_num,
                #  '商品地址': response.url
            })
            yield {**self.public_content, **{'data': [info]}}
