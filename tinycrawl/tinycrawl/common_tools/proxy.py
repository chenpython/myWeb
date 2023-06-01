import collections
import datetime
import json
import re
import string
import time
from urllib.parse import urlencode

import aiohttp
import requests

from . import const, db, log, scrapy_settings

logger = log
redis_client = db.redis_client


class Proxy:

    def __init__(self):

        self.payload = {
            'num': scrapy_settings.DEFAULT_PROXY_NUMS_PER_BATCH,  #  获取数量
            'type': 2,  # 数据格式（1TXT 2JSON 3html）
            'city': 0,  # 城市
            'yys': 0,  # 运营商(100026:联通 100017:电信)
            'port': 1,  # IP协议（1:HTTP 2:SOCK5 11:HTTPS ）
            'time': 3,  # 稳定时长：01 - 05 分钟
            'ts': 1,  # 是否显示IP过期时间（1显示 2不显示）
            'ys': 0,  #  是否显示IP运营商（1显示 0不显示）
            'cs': 1,  # 是否显示位置信息（1显示 0不显示）
            'lb': 1,  # 分隔符(1:\r\n 2:/br 3:\r 4:\n 5:\t 6 :自定义)
            'sb': 0,  # 自定义分隔符
            'pb': 45,  # 端口位数（4：4位；5：5位）
            'mr': 1,  # 去重选择（1、自动去重；2、单日去重；3、不去重）
            'regions': '',  # 全国混发地区
            'pro': ''  # 代表省份
        }

        self.white_payload = {
            'neek': scrapy_settings.JG_PROXY_NEEK,
            'appkey': scrapy_settings.JG_PROXY_APPKEY,
            'white': ''
        }

        self.detection_website = 'http://www.baidu.com/'

        self.obtain_own_ip_url = 'http://icanhazip.com'

    def get_one_ip(self, payload):

        # time2 有效时长 30 分钟 到 3 小时

        ip_key = json.dumps(payload)

        ip = redis_client.get(ip_key)

        if ip:

            return ip.decode()

        params = urlencode(payload)

        url = '{}?{}'.format(scrapy_settings.JG_PROXY_IP_URL, params)

        try:
            response = requests.request('GET', url)

            result = response.json()

            if result['code'] != 0:
                if result['code'] == 113:

                    self.save_white()
                    time.sleep(2)

                    return self.get_one_ip(payload)

                elif result["code"] == 111:  # 请求频率过快
                    time.sleep(2)
                    return self.get_one_ip(payload)

                else:
                    raise Exception(result)

            ip_ = result['data'][0]

            proxy = "{ip}:{port}".format(ip=ip_['ip'], port=ip_['port'])

            redis_client.set(ip_key, proxy, ex=3 * 60 * 60)
        except Exception as e:
            logger.error(f'get one ip error: {e}')
            proxy = ''

        return proxy

    def get_ip_list(self):

        params = urlencode(self.payload)

        url = '{}?{}'.format(scrapy_settings.JG_PROXY_IP_URL, params)

        try:

            start_time = time.perf_counter()

            response = requests.request('GET', url)

            result = response.json()

            if result['code'] != 0:

                if result['code'] == 113:
                    # 添加白名单
                    self.save_white()
                    time.sleep(2)

                    return self.get_ip_list()

                raise Exception(result)

            logger.info("It takes {} seconds to obtain the proxy".format(time.perf_counter() - start_time))

        except Exception as e:

            logger.error("Failed to obtain the proxy ip list, err: {}, url: {}".format(e, url))

            msg = {
                "title": "获取代理失败",
                "text": "#### **获取代理失败详情**\n\n##### - 失败原因: \n\n{}\n\n - 请求 url: \n{}".format(e, url)
            }

            return []

        return result['data']

    def update_ip_pool(self):

        ip_list = self.get_ip_list()

        if not ip_list:
            return

        self.create_ip_pool(ip_list)

    def create_ip_pool(self, ip_list: list):

        ip_info_map_ = [
            self.package_proxy_info("{ip}:{port}".format(ip=ip_['ip'], port=ip_['port']), ip_['expire_time'])
            for ip_ in ip_list
        ]

        ip_info_map = dict(collections.ChainMap(*ip_info_map_))

        valid_ip_list = ip_info_map.keys()

        redis_client.sadd(const.REDIS_IP_POOL_KEY, *valid_ip_list)

        redis_client.hset(const.REDIS_IP_MAP, mapping=ip_info_map)

        redis_client.expire(const.REDIS_IP_POOL_KEY, const.REDIS_IP_POOL_KEY_EXPIRED_TIME)

        redis_client.expire(const.REDIS_IP_MAP, const.REDIS_IP_POOL_KEY_EXPIRED_TIME + 10)

        logger.info("Updating the proxy pool is complete")

    def package_proxy_info(self, proxy, expire_time):

        time_array = time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")
        expire_timestamp = int(time.mktime(time_array))

        return {proxy: expire_timestamp}

    async def check_ip(self, proxy: string, expire_time: string):

        async with aiohttp.ClientSession() as session:

            try:

                proxy_url = 'http://{}'.format(proxy)

                async with session.get(self.detection_website, proxy=proxy_url) as res:

                    if res.status != 200:
                        return

            except Exception as e:

                logger.error('Proxy detection failure. err: {}'.format(e))

                return

        time_array = time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")
        expire_timestamp = int(time.mktime(time_array))

        return json.dumps({'url': proxy, 'expire_timestamp': expire_timestamp})

    def save_white(self):

        try:

            resp = requests.get(self.obtain_own_ip_url)

            if resp.status_code != 200:
                raise Exception(resp.text)

            self.white_payload['white'] = resp.text.replace("\n", "")

        except Exception as e:

            logger.error('Failed to obtain the ip address of the current host, err: {}'.format(e))

            msg = {"title": "获取当前IP失败", "text": "#### **获取当前IP失败详情**\n\n##### - 失败原因: \n\n{}\n\n".format(e)}

            return

        params = urlencode(self.white_payload)

        url = '{}?{}'.format(scrapy_settings.JG_PROXY_SAVE_WHITE, params)

        try:

            response = requests.request('GET', url)

            result = response.json()

            if result['code'] not in [0, 115]:

                raise Exception(result)

        except Exception as e:

            logger.error("Failed to save white ip list, err: {}, url: {}".format(e, url))

            msg = {
                "title": "添加白名单失败",
                "text": "#### **添加白名单失败详情**\n\n##### - 失败原因: \n\n{}\n\n - 请求 url: \n{}".format(e, url)
            }

    def random_one_proxy(self):

        while True:

            proxy_info = redis_client.srandmember(const.REDIS_IP_POOL_KEY)

            if not proxy_info:

                # 避免线程重复更新
                if redis_client.setnx(const.UPDATE_IP_POOL_FLAG, const.UPDATE_IP_POOL_FLAG_VALUE):

                    redis_client.expire(const.UPDATE_IP_POOL_FLAG, const.REDIS_IP_POOL_KEY_EXPIRED_TIME)

                    self.update_ip_pool()

                    redis_client.delete(const.UPDATE_IP_POOL_FLAG)

                return

            proxy = proxy_info.decode()

            try:

                if not redis_client.hget(const.REDIS_IP_MAP, proxy) or int(
                        redis_client.hget(const.REDIS_IP_MAP, proxy).decode()) <= int(
                            datetime.datetime.now().timestamp()):

                    self.remove_proxy(proxy)

            except AttributeError:

                self.remove_proxy(proxy)

            else:
                break

        return proxy

    def remove_proxy(self, proxy: string):

        if not proxy:
            return

        if isinstance(proxy, bytes):
            proxy = proxy.decode()

        regex = r"([0-9.:]+)$"

        match_value = re.search(regex, proxy)

        if not match_value:
            return

        value = match_value.groups()[0]

        redis_client.srem(const.REDIS_IP_POOL_KEY, value)

        redis_client.hdel(const.REDIS_IP_MAP, value)