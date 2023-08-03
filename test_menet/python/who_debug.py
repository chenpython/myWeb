import os
import re, random

import scrapy

from ...menet.menet.spiders import base_spider
from ...menet.menet.common_tools import tools

# 当弹出过验证码后，当前ip会一直受到验证码的限制
# 滑块验证出现频率较高
# 大于 3 页就会出现图片识别验证码
# 验证码通过后，后续页数请求需要携带什么数据？
# 验证码失败后，怎么判断验证是否失败？如果重新发起请求？
# 验证码通过后切换代理后是否还有效？


class WhoClinicSpider(base_spider.CustomBaseSpider):
    name = ''
    allowed_domains = ['www.chictr.org.cn']

    custom_settings = {
        "MONGODB_COLLECTION_NAME": f'results_{name}',
        "SUBPATH": name,
        'DOWNLOAD_DELAY': 2,
        'RETRY_TIMES': 10
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

    def start_requests(self):

        for page in range(1, 6525):
            yield scrapy.Request(url=self.next_url.format(page),
                                 headers=self.headers)

        # yield scrapy.Request(url=self.next_url.format(4), headers=self.headers)

    def parse(self, response):

        if type_ := self.error_page_type(response):

            raise Exception('{} 出现 {} 页面'.format(response.url, type_))

        all_tr = response.xpath('//table[@class="table_list"]/tbody/tr')

        for tr in all_tr[1:]:

            all_td = tr.xpath("td")

            revisions_url = 'http://{}/{}'.format(
                self.allowed_domains[0], all_td[0].xpath('a/@href').get())

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
                'http://{}/{}'.format(
                    self.allowed_domains[0],
                    all_td[2].xpath('p/a/@href').get()),  # 详情页地址
                'parent_url':
                response.url
            }

            yield scrapy.Request(url=revisions_url,
                                 headers=self.headers,
                                 callback=self.parse_revisions,
                                 meta={'info': info},
                                 dont_filter=True)

        if 'page=' in response.url:

            cur_page = int(response.url.split('page=')[-1])

        else:
            cur_page = 1

            self.total_page = int(
                response.xpath('string(//div[@id="pgProj"]/span)').re(
                    '共(\d+)页')[0])

        next_page = cur_page + 1

        if next_page > self.total_page:
            return

        next_url = self.next_url.format(next_page)

        yield scrapy.Request(next_url, headers=self.headers)

        # if 'page=' not in response.url:

        #     self.total_page = int(
        #         response.xpath('string(//div[@id="pgProj"]/span)').re(
        #             '共(\d+)页')[0])

        # for next_page in range(2, self.total_page + 1):

        #     next_url = self.next_url.format(next_page)

        #     yield scrapy.Request(next_url, headers=self.headers)

    def parse_revisions(self, response):

        if type_ := self.error_page_type(response):

            raise Exception('{} 出现 {} 页面'.format(response.url, type_))

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

        if type_ := self.error_page_type(response):

            raise Exception('{} 出现 {} 页面'.format(response.url, type_))

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

    def save_response(self, response):

        dowloads_folder = '/home/feng/workspace/WebCrawling/menet/tmp'

        filename = filename = '{:06}.html'.format(random.randint(0, 1000000))

        if not os.path.exists(dowloads_folder):

            os.mkdir(dowloads_folder)

        with open(os.path.join(dowloads_folder, filename), 'wb') as f:

            f.write(response.body)

    def parse_error_handler(self, response):

        if re.search(r'请填写验证码', response.text):

            img_time = random.random()

            img_url = f'https://www.chictr.org.cn/Tools/verifyimagepage.aspx?textcolor=2&bgcolor=F4F4F4&ut=1&time={img_time}'

            verifycode = tools.captcha_instance.captcha_handler(
                img_url, self.headers)

            page = int(response.url.split('page=')[-1])

            url = f'https://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode={verifycode}&page={page}'

            return scrapy.Request(url,
                                  headers=response.request.headers,
                                  meta=response.request.meta,
                                  callback=response.request.callback)

        return response.request

    def error_page_type(self, response):

        if re.search(r"滑动验证页面", response.text):

            div = response.xpath('//div[@class="waf-nc-h5-panel"]')

            traceid = response.xpath("//div[@id='traceid']/text()").get()

            return '滑块验证'

        if re.search(r'请填写验证码', response.text):

            return '图片识别验证码'

        return True

    def table_1_handler(self, selector):

        return {
            'last_refreshed_date':
            self.extract_value(
                selector.xpath('string(tbody/tr[2]/td[2])').get()),
            'registration_status':
            self.extract_value(
                selector.xpath('string(tbody/tr[4]/td[2])').get()),
            'registration_status_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[5]/td[2])').get()),
            'public_title':
            self.extract_value(
                selector.xpath('string(tbody/tr[6]/td[2])').get()),
            'public_title_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[7]/td[2])').get()),
            'acronym':
            self.extract_value(
                selector.xpath('string(tbody/tr[8]/td[2])').get()),
            'acronym_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[9]/td[2])').get()),
            'scientific_title':
            self.extract_value(
                selector.xpath('string(tbody/tr[10]/td[2])').get()),
            'scientific_title_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[11]/td[2])').get()),
            'study_subject_id':
            self.extract_value(
                selector.xpath('string(tbody/tr[11]/td[2])').get()),
            'partner_registry_or_other_registe':
            self.extract_value(
                selector.xpath('string(tbody/tr[12]/td[2])').get())
        }

    def table_2_handler(self, selector):

        return {
            'applicant':
            self.extract_value(
                selector.xpath('string(tbody/tr[1]/td[2])').get()),
            'applicant_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[2]/td[2])').get()),
            'study_leader':
            self.extract_value(
                selector.xpath('string(tbody/tr[1]/td[4])').get()),
            'study_leader_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[2]/td[4])').get()),
            'Applicant_telephone':
            self.extract_value(
                selector.xpath('string(tbody/tr[3]/td[2])').get()),
            'study_leader_telephone':
            self.extract_value(
                selector.xpath('string(tbody/tr[3]/td[4])').get()),
            'applicant_fax':
            self.extract_value(
                selector.xpath('string(tbody/tr[4]/td[2])').get()),
            'study_leader_fax':
            self.extract_value(
                selector.xpath('string(tbody/tr[4]/td[4])').get()),
            'applicant_e-mail':
            self.extract_value(
                selector.xpath('string(tbody/tr[5]/td[2])').get()),
            'study_leader_e-mail':
            self.extract_value(
                selector.xpath('string(tbody/tr[5]/td[4])').get()),
            'applicant_website':
            self.extract_value(
                selector.xpath('string(tbody/tr[6]/td[2])').get()),
            'study_leader_website':
            self.extract_value(
                selector.xpath('string(tbody/tr[6]/td[4])').get()),
            'applicant_address':
            self.extract_value(
                selector.xpath('string(tbody/tr[7]/td[2])').get()),
            'applicant_address_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[8]/td[2])').get()),
            'study_leader_address':
            self.extract_value(
                selector.xpath('string(tbody/tr[7]/td[4])').get()),
            'study_leader_address_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[8]/td[4])').get()),
            'applicant_postcode':
            self.extract_value(
                selector.xpath('string(tbody/tr[9]/td[2])').get()),
            'study_leader_postcode':
            self.extract_value(
                selector.xpath('string(tbody/tr[9]/td[4])').get()),
            'applicant_institution':
            self.extract_value(
                selector.xpath('string(tbody/tr[10]/td[2])').get()),
            'applicant_institution_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[11]/td[2])').get()),
        }

    def table_3_handler(self, selector):

        tbody1 = selector.xpath("tbody[1]")
        tbody2 = selector.xpath("tbody[2]")

        return {
            'approved_by_ethic_committee':
            self.extract_value(tbody1.xpath('string(tr[1]/td[2])').get()),
            'approved_by_ethic_committee_en':
            self.extract_value(tbody1.xpath('string(tr[2]/td[2])').get()),
            'approved_no_of_ethic_committee':
            self.extract_value(tbody2.xpath('string(tr[1]/td[2])').get()),
            'approved_file_of_ethical_committee':
            'https://{}{}'.format(
                self.allowed_domains[0],
                self.extract_value(tbody2.xpath('tr[1]/td[4]/a/@href').get()),
            ),
            'ethic_committee_name':
            self.extract_value(tbody2.xpath('string(tr[2]/td[2])').get()),
            'ethic_committee_name_en':
            self.extract_value(tbody2.xpath('string(tr[3]/td[2])').get()),
            'ethic_committee_approved_date':
            self.extract_value(tbody2.xpath('string(tr[4]/td[2])').get()),
            'ethic_committee_contact_name':
            self.extract_value(tbody2.xpath('string(tr[5]/td[2])').get()),
            'ethic_committee_contact_name_en':
            self.extract_value(tbody2.xpath('string(tr[6]/td[2])').get()),
            'ethic_committee_contact_address':
            self.extract_value(tbody2.xpath('string(tr[7]/td[2])').get()),
            'ethic_committee_contact_address_en':
            self.extract_value(tbody2.xpath('string(tr[8]/td[2])').get()),
            'ethic_committee_contact_phone':
            self.extract_value(tbody2.xpath('string(tr[9]/td[2])').get()),
            'ethic_committee_contact_email':
            self.extract_value(tbody2.xpath('string(tr[9]/td[4])').get()),
        }

    def table_4_handler(self, selector):

        return {
            'primary_sponsor':
            self.extract_value(
                selector.xpath("string(tbody/tr[1]/td[2])").get()),
            'primary_sponsor_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[2]/td[2])").get()),
            'primary_sponsor_address':
            self.extract_value(
                selector.xpath("string(tbody/tr[3]/td[2])").get()),
            'primary_sponsor_address_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[4]/td[2])").get()),
            'secondary_sponsor': {
                'country':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[1]/td[2])").
                    get()),
                'country_en':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[2]/td[2])").
                    get()),
                'province':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[1]/td[4])").
                    get()),
                'province_en':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[2]/td[4])").
                    get()),
                'institution_hospital':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[3]/td[2])").
                    get()),
                'institution_hospital_en':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[4]/td[2])").
                    get()),
                'address':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[3]/td[4])").
                    get()),
                'address_en':
                self.extract_value(
                    selector.xpath(
                        "string(tbody/tr[5]/td[2]/table/tbody/tr[4]/td[4])").
                    get()),
            },
            'funding_source':
            self.extract_value(
                selector.xpath("string(tbody/tr[6]/td[2])").get()),
            'funding_source_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[7]/td[2])").get()),
            'target_disease':
            self.extract_value(
                selector.xpath("string(tbody/tr[8]/td[2])").get()),
            'target_disease_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[9]/td[2])").get()),
            'target_disease_code':
            self.extract_value(
                selector.xpath("string(tbody/tr[10]/td[2])").get()),
            'target_disease_code_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[11]/td[2])").get()),
            'study_type':
            self.extract_value(
                selector.xpath("string(tbody/tr[12]/td[2])").get()),
            'study_type_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[13]/td[2])").get()),
            'study_phase':
            self.extract_value(
                selector.xpath("string(tbody/tr[14]/td[2])").get()),
            'study_phase_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[15]/td[2])").get()),
            'objectives_of_study':
            self.extract_value(
                selector.xpath("string(tbody/tr[16]/td[2])").get()),
            'objectives_of_study_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[17]/td[2])").get()),
            'medicine_description':
            self.extract_value(
                selector.xpath("string(tbody/tr[18]/td[2])").get()),
            'medicine_description_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[19]/td[2])").get()),
            'study_design':
            self.extract_value(
                selector.xpath("string(tbody/tr[20]/td[2])").get()),
            'study_design_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[21]/td[2])").get()),
            'inclusion_criteria':
            self.extract_value(
                selector.xpath("string(tbody/tr[22]/td[2])").get()),
            'inclusion_criteria_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[23]/td[2])").get()),
            'exclusion_criteria':
            self.extract_value(
                selector.xpath("string(tbody/tr[24]/td[2])").get()),
            'exclusion_criteria_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[25]/td[2])").get())
        }

    def table_5_handler(self, selector):
        return {
            'study_execute_time':
            self.extract_value(selector.xpath("string(tr[1]/td[2])").get()),
            'Recruiting_time':
            self.extract_value(selector.xpath("string(tr[1]/td[4])").get())
        }

    def table_6_handler(self, selector):

        selector = selector.xpath('tbody/tr[1]/td[2]')

        result = []

        tables = selector.xpath("table")

        for tb in tables:

            result.append({
                'group':
                self.extract_value(
                    tb.xpath('string(tbody/tr[1]/td[2])').get()),
                'group_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[2]/td[2])').get()),
                'sample_size':
                self.extract_value(
                    tb.xpath('string(tbody/tr[1]/td[4])').get()),
                'intervention':
                self.extract_value(
                    tb.xpath('string(tbody/tr[3]/td[2])').get()),
                'intervention_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[4]/td[2])').get()),
                'intervention_code':
                self.extract_value(
                    tb.xpath('string(tbody/tr[3]/td[4])').get()),
            })

        return {'interventions': result}

    def table_7_handler(self, selector):

        return {
            'research_settings': {
                'country':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2])').
                    get()),
                'country_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[2]/td[2])').
                    get()),
                'province':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[1]/td[4])').
                    get()),
                'province_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4])').
                    get()),
                'city':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[1]/td[6])').
                    get()),
                'city_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[2]/td[6])').
                    get()),
                'institution_hospital':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[3]/td[2])').
                    get()),
                'institution_hospital_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2])').
                    get()),
                'institution_level':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[3]/td[4])').
                    get()),
                'institution_level_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]/table/tbody/tr[4]/td[4])').
                    get()),
            }
        }

    def table_8_handler(self, selector):

        result = []

        tables = selector.xpath("table")

        for tb in tables:

            result.append({
                'outcome':
                self.extract_value(
                    tb.xpath('string(tbody/tr[1]/td[2])').get()),
                'outcome_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[2]/td[2])').get()),
                'type':
                self.extract_value(
                    tb.xpath('string(tbody/tr[1]/td[4])').get()),
                'type_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[2]/td[4])').get()),
                'measure_time_point_of_outcome':
                self.extract_value(
                    tb.xpath('string(tbody/tr[3]/td[2])').get()),
                'measure_time_point_of_outcome_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[4]/td[2])').get()),
                'measure_method':
                self.extract_value(
                    tb.xpath('string(tbody/tr[3]/td[4])').get()),
                'measure_method_en':
                self.extract_value(
                    tb.xpath('string(tbody/tr[3]/td[4])').get()),
            })

        return {'outcomes': result}

    def table_9_handler(self, selector):

        return {
            'collecting_samples_from_participants': {
                'sample_name':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[1]/td[2])').
                    get()),
                'sample_name_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[2]/td[2])').
                    get()),
                'tissue':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[1]/td[4])').
                    get()),
                'tissue_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[2]/td[4])').
                    get()),
                'fate_of_sample':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[3]/td[2])').
                    get()),
                'fate_of_sample_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[4]/td[2])').
                    get()),
                'note':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[3]/td[4])').
                    get()),
                'note_en':
                self.extract_value(
                    selector.xpath(
                        'string(tbody/tr[1]/td[2]//table/tbody/tr[4]/td[4])').
                    get())
            }
        }

    def table_10_handler(self, selector):

        return {
            'recruiting_status':
            self.extract_value(
                selector.xpath('string(tbody/tr[1]/td[2]/p[1])').get()),
            'recruiting_status_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[1]/td[2]/p[2])').get()),
            'participant_age': {
                'min_age':
                '{} 岁'.format(
                    self.extract_value(
                        selector.xpath(
                            'string(tbody/tr[1]/td[4]/table//tr[1]/td[2])').
                        get())) if
                selector.xpath('string(tbody/tr[1]/td[4]/table//tr[1]/td[2])'
                               ).get() else '',
                'max_age':
                '{} 岁'.format(
                    self.extract_value(
                        selector.xpath(
                            'string(tbody/tr[1]/td[4]/table//tr[2]/td[2])').
                        get())) if
                selector.xpath('string(tbody/tr[1]/td[4]/table//tr[2]/td[2])'
                               ).get() else ''
            },
            'gender':
            self.extract_value(
                selector.xpath('string(tbody/tr[2]/td[2])').get()),
            'gender_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[2]/td[4])').get()),
            'randomization_procedure':
            self.extract_value(
                selector.xpath('string(tbody/tr[3]/td[2])').get()),
            'randomization_procedure_en':
            self.extract_value(
                selector.xpath('string(tbody/tr[4]/td[2])').get())
        }

    def table_11_handler(self, selector):

        tbody1 = selector.xpath("tbody[1]")
        tbody2 = selector.xpath("tbody[2]")

        return {
            'blinding':
            self.extract_value(tbody1.xpath("string(tr[1]/td[2])").get()),
            'blinding_en':
            self.extract_value(tbody1.xpath("string(tr[2]/td[2])").get()),
            'calculated_results':
            tbody2.xpath("tr[1]/td[2]").get()
        }

    def table_12_handler(self, selector):

        return {
            'ipd_sharing':
            self.extract_value(
                selector.xpath("string(tbody/tr[1]/td[2])").get()),
            'sharing_ipd_way':
            self.extract_value(
                selector.xpath("string(tbody/tr[2]/td[2])").get()),
            'sharing_ipd_way_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[3]/td[2])").get()),
            'data_collection_and_management':
            self.extract_value(
                selector.xpath("string(tbody/tr[4]/td[2])").get()),
            'data_collection_and_management_en':
            self.extract_value(
                selector.xpath("string(tbody/tr[5]/td[2])").get()),
            'data_and_safety_monitoring_committee':
            self.extract_value(
                selector.xpath("string(tbody/tr[6]/td[2])").get())
        }

    def extract_value(self, content: str):

        result = ''

        result += ''.join(content).replace('\r', '').replace('\n', '').replace(
            '\t', '').replace('\xa0', '').strip()

        return result