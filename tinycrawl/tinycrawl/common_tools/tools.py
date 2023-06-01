import collections
import copy
import os
import random
import re
import string
import urllib
from datetime import datetime

import cv2
import ddddocr
import requests
from aip import AipOcr
from lxml import etree

from . import scrapy_settings

ALL_VALID_USER_AGENTS = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "MAC：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
    "Windows：Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999", "NOKIA5700/ UCWEB7.0.2.37/28/999", "Openwave/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999")

TOTAL_AGENTS_NUMS = len(ALL_VALID_USER_AGENTS)


def get_random_agents():

    index = random.randint(0, TOTAL_AGENTS_NUMS - 1)

    return ALL_VALID_USER_AGENTS[index]


def transform_password(org_str: string):

    pass_str = re.search(r":([^\/]*)@\d+", org_str)

    if not pass_str:
        return org_str

    pass_str = pass_str.groups()[0]

    conn_str = org_str.split(pass_str)[0] + urllib.parse.quote(pass_str) + org_str.split(pass_str)[-1]

    return conn_str


def format_data(data, replace_str=None, regex=False):
    """格式化数据对象

    Args:
        data (Any): 需要格式化的对象
        replace_str (list | dict, optional): 需要替换的内容。传入 list 对象默认替换为空；传入字典对象可以指定对应替换内容. Defaults to None.
        regex (bool, optional): 是否使用正则匹配. Defaults to False.
    """

    def replace_target(data):
        if regex:
            if isinstance(replace_str, dict):
                # 字典形式
                for match, custom_str in replace_str.items():
                    data = re.sub(match, custom_str, data)
            else:
                raise Exception('正则模式必须使用字典给出pattern和替换内容')

            return data

        if isinstance(replace_str, list):
            for match in replace_str:
                data = data.replace(match, '')
            return data

        else:
            # 字典形式
            for match, custom_str in replace_str.items():
                data = data.replace(match, custom_str)
            return data

    def _format(data):

        if isinstance(data, str):
            data = replace_target(data)
            return data

        if isinstance(data, list):
            result = collections.deque()
            for d in data:
                d = _format(d)
                result.append(d)
            return list(result)

        if isinstance(data, dict):
            for key, value in data.items():
                value = _format(value)
                data[key] = value
            return data

        return data

    if not replace_str:
        return data

    data = _format(data)
    return data


def merge_str(strs, union_str='', result=''):
    """根据传入的 union_str 合并 list、dict 的值"""
    if not strs:
        return result

    if isinstance(strs, str):
        return strs

    elif isinstance(strs, list):

        for str_ in strs:
            if not isinstance(str_, str):
                str_ = merge_str(str_, union_str)
            result = result + union_str + str_ if result else str_

    elif isinstance(strs, dict):
        for str_ in strs.values():
            if not isinstance(str_, str):
                str_ = merge_str(str_, union_str)
            result = result + union_str + str_ if result else str_

    return result


def split_time_str(time_str):
    """分割时间字符串"""

    time_str_list = time_str.split(':')
    # 时分秒格式默认为统一的，如时分秒有0填充位，则直接取连接处的后两位
    if time_str_list[-1].startswith('0'):

        formated_time_str = time_str_list[0][:-2] + ' ' + time_str_list[0][-2:] + ':' + time_str_list[-1]

        return formated_time_str

    time_str_list_1 = time_str_list[0].split('-')
    # 优先取连接处的后两位校验是否合法
    if int(time_str_list_1[-1][-2:]) > 23:

        formated_time_str = time_str_list[0][:-1] + ' ' + time_str_list[0][-1:] + ':' + time_str_list[-1]

        return formated_time_str

    else:

        formated_time_str = time_str_list[0][:-2] + ' ' + time_str_list[0][-2:] + ':' + ':'.join(time_str_list[1:])

        return formated_time_str


def format_time(time_str):
    """格式化时间字符串"""

    # 1、将中文替换
    update_date_str = time_str.replace("年", "-").replace("月", "-").replace("日", "")
    # 2、将分隔符统一
    update_date_str = update_date_str.replace('/', '-').replace('.', '-')
    # 3、将无效内容替换
    valid_date_str = re.sub(r'[^0-9\-/: ]', '', update_date_str).strip()
    if valid_date_str == '':
        return
    # 有效长度：yyyy-mm-dd hh-mm-ss
    if len(valid_date_str) > 19:
        valid_date_str = valid_date_str[:19]

    # 4、判断格式是否合法
    # %Y-%m-%d
    if re.match(r"\d{4}-\d{1,2}-\d{1,2}$", valid_date_str):
        dt = datetime.strptime(valid_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%Y-%m-%d')
    # %Y-%m-%d %H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$", valid_date_str):
        dt = datetime.strptime(valid_date_str, '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d %H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}$", valid_date_str):
        dt = datetime.strptime('{}:00'.format(valid_date_str), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + valid_date_strs[-1]
        dt = datetime.strptime('{}:00'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + ':'.join(
            valid_date_strs[1:])
        dt = datetime.strptime('{}'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{3}:\d{1,2}:\d{1,2}$", valid_date_str):

        valid_date_str_format = split_time_str(valid_date_str)
        dt = datetime.strptime('{}'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M:%S
    elif re.match(r"\d{4}-\d{1,2}-\d{2}:\d{1,2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
            valid_date_strs[1:])
        dt = datetime.strptime('{}'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{2}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
            valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{3}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-1] + ' ' + valid_date_strs[0][-1] + ':' + ':'.join(
            valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    # %Y-%m-%d%H:%M
    elif re.match(r"\d{4}-\d{1,2}-\d{4}:\d{1,2}$", valid_date_str):
        valid_date_strs = valid_date_str.split(':')
        valid_date_str_format = valid_date_strs[0][:-2] + ' ' + valid_date_strs[0][-2:] + ':' + ':'.join(
            valid_date_strs[1:])
        dt = datetime.strptime('{}:00'.format(valid_date_str_format), '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_date = ''  # 不合法的时间格式置空

    return formatted_date


def split_merged_cells(table: etree._Element):
    """处理table标签中的合并单元格

    Args:
        table (lxml.etree._Element): table元素
    Return:
        new_table (lxml.etree._Element): 新的 table 元素
    """

    new_table = copy.deepcopy(table)
    all_tr = new_table.xpath('//tr')

    for tr in all_tr:
        all_tds = tr.xpath('td')

        for td in all_tds:
            rowspan = int(td.get('rowspan', 1))  # 多行合并
            colspan = int(td.get('colspan', 1))  # 多列合并

            if rowspan > 1:
                td.attrib.pop('rowspan', None)

                for i in range(1, rowspan):
                    insert_tr_index = all_tr.index(tr) + i
                    insert_td_index = all_tds.index(td)
                    new_cell = copy.deepcopy(td)
                    all_tr[insert_tr_index].insert(insert_td_index, new_cell)

    return new_table