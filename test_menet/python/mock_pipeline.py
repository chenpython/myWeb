# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import asyncio, os
import datetime
import re
import time

import aiohttp
import pymongo
import json

import requests

import psycopg2
import psycopg2.extras
from crawlab.config import get_task_id
from . import settings
from .common_tools import db, const, tools, upload, proxy, log

proxy_instance = proxy.Proxy()

from unittest.mock import patch


class MenetTaskOpt:

    task_url = 'http://192.168.20.11:8080/api/tasks/'
    task_data_url = 'http://192.168.20.11:8080/api/tasks/%s/data?page=1&size=10'
    headers = {
        'Authorization':
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzNWY5NGJhNTJlYzllOTJjM2Q4ZDRhNyIsIm5iZiI6MTY3MTE4MTc4NSwidXNlcm5hbWUiOiJhZG1pbiJ9.16Z0gdtDR8XxI3qjZD-iI2tQNd3kWQiaB8hX6QqUWxM'
    }
    # 需要去掉命令参数的爬虫名
    half_cmd_spiders = [
        'drugs_fda', 'hma', 'japan_prescription', 'japan_otc_drug'
    ]
    insert_query = "insert into config_mongodb_tasks " \
                   "(_id, collection_name, website_location, crawl_time, cmd, task_begin_time, task_status) " \
                   "values (%s, %s, %s, %s, %s, %s, %s)"
    update_query = "update config_mongodb_tasks " \
                   "set task_end_time = '%s', task_status = '%s', task_sum = %s, update_time = '%s' " \
                   "where _id = '%s'"

    def __init__(self):
        self.conn, self.connect_time = self.connect_pg()
        self.need_update = False
        with patch('crawlab.config.get_task_id',
                   return_value='1232412431') as mocked_method:
            self.task_id = mocked_method()
        # self.task_id = get_task_id()
        self.opt_lock = settings.PG_OPT_LOCK
        self._redis = db.redis_client

    @staticmethod
    def connect_pg():
        try:

            conn = psycopg2.connect(database=settings.PG_DATABASE,
                                    user=settings.PG_USER,
                                    password=settings.PG_PWD,
                                    host=settings.PG_HOST,
                                    port=settings.PG_PORT)

            return conn, int(time.time())

        except Exception as e:

            raise Exception(f'connect pg error: {e}')

    def spider_open(self, spider):
        """启动爬虫的时候调用，不会把连接断开，
        如果爬虫时间长的话，可以在process_item中有连接时间的判断，
        settings里有关闭时长属性: PG_CLOSE_CONNECTION_TIME

        Args:
            spider: 爬虫实例化的对象
        """

        crawl_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        self.opt_lock += ':' + spider.name + ':' + crawl_time
        if self._redis.get(self.opt_lock):
            return
        self._redis.set(self.opt_lock, 'INSERT')

        cursor = self.conn.cursor()
        try:
            cmd = self.get_cmd(self.task_id)
            if not cmd:
                self._redis.delete(self.opt_lock)
                return

            mappings = self.get_mappings(cmd, cursor)
            if not mappings:
                self._redis.delete(self.opt_lock)
                return

            self.need_update = True
            self.insert_task_info(self.task_id, mappings, spider, cursor)

        except Exception as e:

            self.conn.rollback()
            log.error(f'spider open error: {e}')

        finally:
            self.conn.commit()
            cursor.close()

    # def process_item(self, item, spider):
    #
    #     # 如果连接时间过长，则先断开连接
    #     if (int(time.time()) - self.connect_time) >= settings.PG_CLOSE_CONNECTION_TIME:
    #         self.conn.close()
    #
    #     item['task_id'] = self.task_id
    #
    #     return item

    def spider_close(self, spider):

        if not self.need_update:
            return

        if self._redis.get(self.opt_lock) == 'UPDATE':
            return
        self._redis.set(self.opt_lock, 'UPDATE')

        # 判断连接是否断开，断开的话重新连接
        if not self.conn or (hasattr(self.conn, 'closed')
                             and self.conn.closed):
            self.conn, self.connect_time = self.connect_pg()

        cursor = self.conn.cursor()
        try:
            task_sum = self.get_task_sum(self.task_id)
            end_time_str = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
            update_query = self.update_query % (end_time_str, '已完成', task_sum,
                                                end_time_str, self.task_id)
            cursor.execute(update_query)

        except Exception as e:
            log.error(f'spider close error: {e}')
            self.conn.rollback()

        finally:
            self.conn.commit()
            cursor.close()
            self.conn.close()
            self._redis.delete(self.opt_lock)

    def get_task_sum(self, task_id):

        task_data_url = self.task_data_url % task_id
        total = 0
        resp = requests.get(url=task_data_url,
                            headers=self.headers,
                            timeout=15).json()

        if resp['status'] == 'ok':

            total = resp['total']

        return total

    def get_cmd(self, task_id):
        result = {
            '_id': '636bdc9052ec9e92c3d8d5eb',
            'spider_id': '636b404a52ec9e92c3d8d5d2',
            'status': 'finished',
            'node_id': '635f94bb52ec9e92c3d8d4a8',
            'cmd': 'python3 main.py who',
            'param': '',
            'error': '',
            'pid': 504,
            'schedule_id': '636b467252ec9e92c3d8d5df',
            'type': '',
            'mode': 'random',
            'node_ids': None,
            'parent_id': '000000000000000000000000',
            'priority': 5,
            'has_sub': False,
        }
        with patch.object(self, 'get_task_info',
                          return_value=result) as mocked_method:

            task_info = mocked_method(task_id)
            if not task_info:
                return

        # task_info = self.get_task_info(task_id)
        # if not task_info:
        #     return

        cmd = task_info['cmd']
        for half_cmd_spider in self.half_cmd_spiders:
            if half_cmd_spider in cmd:
                cmd = ' '.join(cmd.split(' ')[:3])
                break

        return cmd

    def get_crawl_time(self, spider):

        crawl_time = spider.crawl_time if hasattr(
            spider, 'crawl_time') else spider.public_content.get('crawl_time')

        return crawl_time

    def insert_task_info(self, task_id, mappings, spider, cursor):

        vars = []
        task_begin_time = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
        crawl_time = self.get_crawl_time(spider)
        if not crawl_time:
            crawl_time = task_begin_time

        for mapping in mappings:
            var = [
                task_id, f'results_{spider.name}', mapping[1], crawl_time,
                mapping[0], task_begin_time, '进行中'
            ]
            vars.append(var)

        try:
            cursor.executemany(self.insert_query, vars)
        except Exception as e:
            raise Exception(
                f'insert task info error: {e} -> task_id: {task_id}')

    def get_task_info(self, task_id):
        if not task_id:
            return

        url = self.task_url + task_id
        resp = requests.get(url=url, headers=self.headers).json()
        if resp['status'] == 'ok':

            task_info = resp['data']

            return task_info

        return None

    @staticmethod
    def get_mappings(cmd: str, cursor) -> list:

        query = f"select cmd, website_location from config_mongodb_tasks_mapping where cmd = '{cmd}'"

        try:
            cursor.execute(query)

            results = cursor.fetchall()

            return results

        except Exception as e:

            raise Exception(f'select mapping error: {e} -> cmd: {cmd}')

    def open_spider(self, spider):

        if not settings.BIND_CRAWLAB_TASK:
            return

        self.spider_open(spider)

    def validate_conn_keep_time(self):
        if not settings.BIND_CRAWLAB_TASK:
            return
        # 如果连接时间过长，则先断开连接
        if (int(time.time()) - self.connect_time
            ) >= settings.PG_CLOSE_CONNECTION_TIME and (not self.conn.closed):
            self.conn.close()


def retry_decorator(func):

    def wrapper(*args, **kwargs):

        err = ''

        for _ in range(20):

            try:

                result = func(*args, **kwargs)

                return result

            except Exception as e:

                err = str(e)

                time.sleep(1)

        log.error('Download file failed. url: {}, err: {}'.format(
            args[1], err))

        return ''

    return wrapper


class MenetPipelineMixin:

    @staticmethod
    def format_publish_time(item):

        for data_ in item['data']:

            if publish_time := data_.get('publish_time'):
                data_['ori_publish_time'] = publish_time

                if MenetPipelineMixin.validate_date(publish_time):
                    continue

                publish_time = tools.format_time(publish_time)
                data_['publish_time'] = publish_time

    @staticmethod
    def validate_date(date_string: str) -> bool:
        if not isinstance(date_string, str):
            return True
        pattern = r'^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}?$|^\d{4}-\d{1,2}-\d{1,2}?$'
        if re.match(pattern, date_string):
            return True
        return False


class MenetPipeline(MenetPipelineMixin, MenetTaskOpt):

    def __init__(self, db_name: str, collection_name: str):

        super().__init__()
        conn_str = tools.transform_password(settings.MONGO_BACKEND_URL)

        self.client = pymongo.MongoClient(conn_str,
                                          serverSelectionTimeoutMS=5000)

        self.db = self.client[db_name]
        self.collection = self.db.get_collection(collection_name)

    def process_item(self, item, spider):

        self.validate_conn_keep_time()

        self.format_publish_time(item)

        if spider.name != 'yaojian_review' or (spider.name == 'yaojian_review'
                                               and
                                               spider.review_type != '上市药品信息'):
            timestamp = int(time.time())
            item['timestamp'] = timestamp
            item['task_id'] = self.task_id

            self.collection.insert_one(item)

        return item

    def close_spider(self, spider):
        self.spider_close(spider)
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_name=crawler.settings.get('MONGODB_DB_NAME'),
            collection_name=crawler.settings.get('MONGODB_COLLECTION_NAME'))


class MenetRedisPipeline(MenetPipelineMixin, MenetTaskOpt):

    def __init__(self, sub_path: str, down_headers: dict,
                 collection_name: str):

        super().__init__()
        self.client = db.redis_client
        self.sub_path = sub_path
        self.down_headers = down_headers
        self.collection_name = collection_name

    def process_item(self, item, spider):

        self.validate_conn_keep_time()

        self.format_publish_time(item)

        if spider.name == 'yaojian_review' and spider.review_type != '上市药品信息':
            return item

        item['task_id'] = self.task_id
        sub_path = self.sub_path + '/' + item['version'].replace(
            ' ', '').replace(':', '')
        push_item = [item, self.collection_name, sub_path, self.down_headers]
        item_str = json.dumps(push_item)
        self.client.lpush(const.REDIS_ITEM_KEY, item_str)
        return item

    def close_spider(self, spider):
        self.spider_close(spider)
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sub_path=crawler.settings.get('SUBPATH',
                                          settings.DEFAULT_SUB_PATH),
            down_headers=crawler.settings.get(
                'DOWN_HEADERS', {
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
                }),
            collection_name=crawler.settings.get('MONGODB_COLLECTION_NAME'))


class DownloadFilePipeline:

    def __init__(self, sub_path):

        self.loop = asyncio.get_event_loop()

        self.handler = upload.UploadFileHandler()

        self.handler.loop = self.loop

        connector = aiohttp.TCPConnector(verify_ssl=False, loop=self.loop)

        self.handler.session = aiohttp.ClientSession(loop=self.loop,
                                                     connector=connector)

        self.dowloads_folder = os.path.join(settings.DOWNLOAD_PATH_TMP,
                                            sub_path)

        self.complete_folder = os.path.join(
            self.dowloads_folder,
            datetime.datetime.now().strftime("%Y%m%d"))

        if not os.path.exists(self.dowloads_folder):

            os.mkdir(self.dowloads_folder)

        if not os.path.exists(self.complete_folder):
            os.mkdir(self.complete_folder)

    @classmethod
    def from_crawler(cls, crawler):

        return cls(sub_path=crawler.spider.name)

    def process_item(self, item, spider):

        files = item['data'][0]['attachments']

        if not files:
            return item

        self.save_file_local_sync(files, spider.headers)

        # tasks = [
        #     self.loop.create_task(self.save_file_local(file_, spider.headers))
        #     for file_ in files
        # ]

        # self.loop.run_until_complete(asyncio.wait(tasks))

        return item

    def close_spider(self, spider):
        self.handler.close_global_session()

    def save_file_local_sync(self, file_items, dowload_headers):

        for file_item in file_items:

            url, filename = file_item['file_url'], file_item['filename']

            resp = self.dowload_file(url, dowload_headers)

            if not resp:
                log.error('下载文件失败，url: {}, filename: {}'.format(url, filename))

                continue

            try:

                with open(os.path.join(self.complete_folder, filename),
                          'wb') as f:

                    f.write(resp.content)

                file_item['local_path'] = os.path.dirname(
                    os.path.abspath(
                        os.path.join(self.complete_folder,
                                     filename))) + '/' + filename

            except Exception as e:

                log.error('保存文件失败，err：{}，file_item：{}'.format(
                    str(e), file_item))

    async def save_file_local(self, file_item, dowload_headers):

        url, filename = file_item['file_url'], file_item['filename']

        for _ in range(10):

            proxy = proxy_instance.random_one_proxy()

            if proxy is not None:

                proxy_url = 'http://{}'.format(proxy)

                break

        else:
            return

        fd = open(os.path.join(self.complete_folder, filename), 'wb')

        lp = asyncio.get_event_loop()

        async with aiohttp.ClientSession().get(url,
                                               proxy=proxy_url,
                                               headers=dowload_headers,
                                               timeout=5) as resp:
            while True:

                data = await resp.content.read(500)

                if not data:
                    break

                await lp.run_in_executor(None, self.save_file, fd, data)

        fd.close()

    def save_file(self, f, data):

        f.write(data)

    @retry_decorator
    def dowload_file(self, url, dowload_headers):

        try:

            proxy = proxy_instance.random_one_proxy()

            if proxy is None:

                raise Exception(
                    'Missing valid proxy when download url: {}'.format(url))

            proxies = {
                "http": 'http://{}'.format(proxy),
            }

            resp = requests.request(
                'GET',
                url,
                headers={
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47"
                },
                proxies=proxies,
                timeout=90)

            if resp.status_code == 404:
                raise Exception('Invalid response')

            return resp

        except Exception as e:

            error = 'Unknown error when downloa url: {}, err: {}'.format(
                url, e)

            raise Exception(error)
