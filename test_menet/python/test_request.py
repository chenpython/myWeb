import requests, re, json, urllib
import collections
from urllib.parse import urlencode
from fontTools.ttLib import TTFont  # fonttools-4.39.3

import pandas as pd


def tmp_code():
    pass
    # for url in {
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413406G1020_1_07',
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413406G1020_1_07',
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413404D1025_2_14',
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413404G1021_1_18',
    # 'https://www.drugfuture.com/pmda/drugview/670666_2413407G1025_1_02',
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413404D1025_2_14',
    # 'https://www.drugfuture.com/pmda/drugview/380079_2413404G1021_1_18',
    # 'https://www.drugfuture.com/pmda/drugview/670666_2413407G1025_1_02',
    # 'https://www.drugfuture.com/pmda/drugview/530191_4291463A1020_1_02',
    # '',
    # }:

    #     yield scrapy.Request(url,
    #                          headers=self.headers,
    #                          meta={
    #                              'info': {
    #                                  'manufacturers_and_distributors': '',
    #                                  'common_name': '',
    #                                  'sales_name': ''
    #                              }
    #                          },
    #                          callback=self.parse_detail)


def _get(url, headers, cookies):

    resp = requests.get(
        url,
        headers=headers,
        cookies=cookies,
    )

    return resp


def _post(url, headers, cookies, data):
    resp = requests.post(url, headers=headers, cookies=cookies, data=data)

    return resp


def read_html(path):

    with open(path, "r") as f:
        html = f.read()

    return html


def save_file(content):
    with open('test/html/tmp_result.html', 'wb') as f:
        f.write(content)


def save_into_excel(data: list):

    pd.DataFrame(data).to_excel(
        '/home/feng/workspace/WebCrawling/menet/test_menet/html/tmp_test_result.xlsx'
    )


def diff_file(content):
    """比较新疆资源网的耗材数据，当前拿下来的页数和目标页数的差异，将未抓取的页数写入到excel文件中保存
    """
    content_list = content.split('\n')
    content_list_set = set(content_list)

    pre_ = 0
    page_list = []
    for i in range(0, 54860 + 10, 10):
        page_list.append('{}:{}:{}'.format('20230428 00:00:25', pre_,
                                           min(i, 54860)))
        pre_ = i
    page_list_set = set(page_list)

    diff_eles = page_list_set.difference(content_list_set)

    diff_eles_ = [i for i in diff_eles]
    save_into_excel(diff_eles_)


def diff_japan_otc_batch(content):

    import datetime
    start_date_str = '20141002'
    end_date_str = '20230331'
    date_range = [('19000101', '20141001')]
    pre_date = start_date = datetime.datetime.strptime(start_date_str,
                                                       '%Y%m%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d').date()
    days = (end_date - start_date).days
    for _ in range(days):
        end_date_ = pre_date + datetime.timedelta(days=1)
        date_range.append((
            pre_date.strftime("%Y%m%d"),
            end_date_.strftime("%Y%m%d"),
        ))
        pre_date = end_date_
    print('date_range length: ', len(date_range))

    page_batch_list = ['{}:{}'.format(item[0], item[1]) for item in date_range]

    content_list = content.split('\n')
    content_list_set = set(content_list)

    page_list_set = set(page_batch_list)

    diff_eles = page_list_set.difference(content_list_set)
    diff_eles_ = [i for i in diff_eles]
    save_into_excel(diff_eles_)


def test_request():

    url = "https://www.nstl.gov.cn/api/service/nstl/web/execute?target=nstl4.search4&function=storage/website/url&url=www.nstl.gov.cn"
    headers = {
        'Host': 'www.nstl.gov.cn',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Origin': 'https://www.nstl.gov.cn',
        'Referer': 'https://www.nstl.gov.cn/resources_search.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    resp = _get(url, headers, None)

    print(resp.status_code)

    data_url = 'https://www.nstl.gov.cn/api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl'
    data_headers = {
        'Content-Type':
        'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':
        'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With':
        'XMLHttpRequest',
        'Referer':
        'https://www.nstl.gov.cn/resources_search.html',
        'Origin':
        'https://www.nstl.gov.cn',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    data = {
        'query':
        '{"c":10,"st":"0","f":[],"p":"","q":[],"op":"AND","s":["crti:desc"],"t":["JournalPaper","ProceedingsPaper","DegreePaper"]}',
        'webDisplayId': '11',
        'sl': '1',
        'searchWordId': '',
        'searchId': '',
        'facetRelation': '[]',
        'pageSize': '10',
        'pageNumber': '1'
    }  # 首页

    resp_cookie = [
        value[-1].get('/') for value in resp.cookies._cookies.items()
    ]
    resp_cookie[0].update(resp_cookie[1])
    req_cookies = resp_cookie[0]
    req_cookies = {key: value.value for key, value in req_cookies.items()}
    req_cookies['nstl_rsp'] = ''
    resp1 = _post(data_url, data_headers, req_cookies, data)

    print(resp1.status_code)


from lxml.html import etree


def test_parse_page(content):

    info = {}
    selector_new = etree.HTML(content)
    all_trs = selector_new.xpath('//table[@class="searchTable"]//tr')

    for tr in all_trs[1:]:

        all_tds = tr.xpath('td')
        info = {
            'seq': all_tds[0].xpath('string(.)'),
            'register_number': all_tds[1].xpath('string(.)'),
            'test_condition': all_tds[2].xpath('string(.)'),
            'drug_name': all_tds[3].xpath('string(.)'),
            'indications': all_tds[4].xpath('string(.)'),
            'experimental_popular_topic': all_tds[5].xpath('string(.)'),
            'cur_page': 1
        }
        detail_args = {
            'id': all_tds[1].xpath('a/@id')[0],
            'ckm_index': all_tds[1].xpath('a/@name')[0]
        }


def patent_data_handler(selector):
    colunms_map = {
        0: 'Product_No',
        1: 'Patent_No',
        2: 'Patent_Expiration',
        3: 'Drug_Substance',
        4: 'Drug_Product',
        5: 'Patent_Use_Code',
        6: 'Delist_Requested',
        7: 'Submission_Date'
    }
    result = parse_table_colums(selector=selector, colunms_map=colunms_map)
    return result


def exclusivity_data_handler(selector):
    colunms_map = {
        0: 'Product_No',
        1: 'Exclusivity_Code',
        2: 'Exclusivity_Expiration'
    }
    result = parse_table_colums(selector=selector, colunms_map=colunms_map)
    return result


def parse_table_colums(selector, colunms_map):
    result = []

    all_trs = selector.xpath('//tr')
    for tr in all_trs[1:]:
        all_tds = tr.xpath('td')
        if len(all_tds) == 1:
            continue
        row = {}
        for col_index in range(0, len(all_tds)):
            key = colunms_map.get(col_index)
            row[key] = all_tds[col_index].xpath("string(.)")

        result.append(row)
    return result


def match_rule():
    import pandas as pd

    path = '/home/feng/workspace/WebCrawling/menet/tmp/有效成分'
    result_path = '/home/feng/workspace/WebCrawling/menet/tmp/结果.xlsx'

    result_list = []

    with open(path, 'r') as f:
        rows = f.readlines()

    for row in rows:

        format_1 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+[（]{0,1}[0-9\u0800-\u9fa5-A-Z\x20\u3000]*[）]{0,1})[\x20]*／[\x20]*[(]*([\w\x20]+[（\(]{0,1}[\w\x20]*)[）\)]{0,1}[)]*?[\s\S]*)"

        matchs = re.findall(format_1, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_2 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+（[0-9\u0800-\u9fa5-A-Z\x20\u3000]+）)（([-\w\x20]+（[-\w\x20]+)））?[\s\S]*)"

        matchs = re.findall(format_2, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_3 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+[（\(][0-9\u0800-\u9fa5-A-Z\x20\u3000]+[）\)])([-\w\x20]+[(（][-\w\x20]+)[）)]?[\s\S]*)"

        matchs = re.findall(format_3, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_4 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+[（\(]{0,1}[0-9\u0800-\u9fa5-A-Z\x20\u3000]+)[）\)]{0,1}\[([-\w\x20]+[(（][-\w\x20]+)[）)]?[\s\S]*)"

        matchs = re.findall(format_4, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_5 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+)[\[〔]([\w\x20]+)[〕\]]?[\s\S]*)"

        matchs = re.findall(format_5, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_6 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+)[\(（]([-\w\x20]+)[\)）]?[\s\S]*)"

        matchs = re.findall(format_6, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_7 = r"([0-9\u0800-\u9fa5-A-Z\x20\u3000]+)[\x20、,]([-\w\x20]+?[\s\S]*)"

        matchs = re.findall(format_7, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

        if not row:
            continue

        format_8 = r"(([0-9\u0800-\u9fa5-A-Z\x20\u3000]+[^a-zA-Z])([A-Za-z][-\w\x20]+|[\s\S]*$))"

        matchs = re.findall(format_8, row)
        for match in matchs:
            if match and match[0] == row:
                result_list.append([match[0], match[1], match[2]])
                row = row.replace(match[0], '')

    df = pd.DataFrame(
        result_list,
        columns=['common_name_info', 'common_name_japan', 'common_name_en'])
    df.to_excel(result_path, index=False)


import re
from datetime import datetime


def test_format_publish_time(content):
    date_strings = content.split('\n')

    for date_string in date_strings:
        print('初始 date_string：', date_string)
        formatted_date = format_rules(date_string)
        if not formatted_date:
            continue

        print('格式化后 date_string：', formatted_date)


def format_rules(date_str):

    # 1、将中文替换
    update_date_str = date_str.replace("年", "-").replace("月",
                                                         "-").replace("日", "")
    # 2、将分隔符统一
    update_date_str = update_date_str.replace('/', '-').replace('.', '-')
    # 3、将无效内容替换
    valid_date_str = re.sub(r'[^0-9\-/: ]', '', update_date_str).strip()
    if valid_date_str == '':
        return
    if len(valid_date_str) > 19:
        valid_date_str = valid_date_str[:19]

    # 4、判断格式是否合法
    # %Y-%m-%d
    if re.match(r"\d{4}-\d{1,2}-\d{1,2}$", valid_date_str):
        dt = datetime.strptime(valid_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%Y-%m-%d')
    # %Y-%m-%d %H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$",
                  valid_date_str):
        dt = datetime.strptime(valid_date_str, '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d %H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}$", valid_date_str):
        dt = datetime.strptime('{}:00'.format(valid_date_str),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + valid_date_strs[-1]
        dt = datetime.strptime('{}:00'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + ':'.join(
                valid_date_strs[1:])
        dt = datetime.strptime('{}'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{3}:\d{1,2}:\d{1,2}$", valid_date_str):

        valid_date_str_format = split_time_str(valid_date_str)
        dt = datetime.strptime('{}'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{2}:\d{1,2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
                valid_date_strs[1:])
        dt = datetime.strptime('{}'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
                valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{3}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
                valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[
            0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + ':'.join(
                valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format),
                               '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        print('未格式化：', valid_date_str)
        formatted_date = valid_date_str

    return formatted_date


def split_time_str(time_str):

    time_str_list = time_str.split(':')
    # 时分秒格式默认为统一的，如时分秒有0填充位，则直接取连接处的后两位
    if time_str_list[-1].startswith('0'):

        formated_time_str = time_str_list[0][:-2] + ' ' + time_str_list[0][
            -2:] + ':' + time_str_list[-1]

        return formated_time_str

    time_str_list_1 = time_str_list[0].split('-')
    # 取连接处的后两位校验是否合法
    if int(time_str_list_1[-1][-2:]) > 23:

        formated_time_str = time_str_list[0][:-1] + ' ' + time_str_list[0][
            -1:] + ':' + time_str_list[-1]

        return formated_time_str

    else:

        formated_time_str = time_str_list[0][:-2] + ' ' + time_str_list[0][
            -2:] + ':' + ':'.join(time_str_list[1:])

        return formated_time_str


if __name__ == "__main__":

    # path = '/home/feng/workspace/WebCrawling/menet/test_menet/html/tmp.html'
    # content = read_html(path)
    # test_parse_page(content)
    # test_format_publish_time(content)
    # diff_japan_otc_batch(content)
    # diff_file(content)

    test_request()

    # match_rule()

    # myclass = MyClass()
    # myclass1 = MyClass1()
    # # myclass()
    # myclass.my_function()
    # myclass1.my_function()
