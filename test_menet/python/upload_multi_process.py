import json
import os
import random
import time
from unittest.mock import AsyncMock, patch
import requests
import string
import asyncio
import aiohttp
import datetime

import multiprocessing

from os import environ
from aiohttp.formdata import FormData
from . import db, const, logger, notice, scrapy_settings, decorator
from .. import proxy_instance
from ..middlewares import YaojianDownloaderMiddleware

logger = logger.Logger('UploadLogger')

redis_client = db.redis_client

lua_script = """local function trpop(list_key, count)
  -- 将要弹出的元素数量转换为整数
  count = tonumber(count)

  -- 获取要弹出的元素范围，并将其转换为0-based索引
  local start = -count
  local stop = -1

  -- 使用lrange命令获取要弹出的元素
  local result_data = redis.call('lrange', list_key, start, stop)

  -- 使用ltrim命令截断列表
  redis.call('ltrim', list_key, 0, start - 1)

  -- 返回弹出的元素
  return result_data
end

-- 从列表末尾弹出指定个数元素

  local result = trpop(KEYS[1], ARGV[1])

  return result

"""


class UploadException(Exception):
    pass


class DownloadException(Exception):
    pass


def package_notice_content(failed_url=None, err_msg=None):

    notice_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = {
        "title":
        "上传文件失败",
        "text":
        "#### **失败文件详情**\n\n ##### - 失败原因: \n{}\n\n##### - 文件地址: \n{}\n\n##### - 通知时间: {}"
        .format(err_msg, failed_url, notice_time)
    }

    return msg


def cookie_decorator(func):

    async def wrapper(*args, **kwargs):

        item = args[1]
        down_header = args[-1]

        if item.get('website_name') in const.cookie_website_names:
            proxy_url = get_proxy()

            if item['website_name'] == '国家药监局审评中心' and item[
                    'website_location'] == '上市药品信息':
                cookie = YaojianDownloaderMiddleware.review_cookie(
                    item['website_domain'], proxy_url)
                down_header['Cookie'] = cookie

        result = await func(*args, **kwargs)

        return result

    return wrapper


def get_proxy():
    return

    proxy = proxy_instance.random_one_proxy()

    if proxy is None:
        raise DownloadException('No proxy is currently available.')

    proxy_url = 'http://{}'.format(proxy)

    return proxy_url


class UploadFileHandler:

    upload_url = scrapy_settings.UPLOAD_URL

    upload_headers = {
        'Authorization':
        scrapy_settings.TOKEN,
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
    }

    def __init__(self):

        self.mongo_client = db.get_mongo_client(
        )  # mongodb 连接为线程安全，非进程安全，需要重新获取连接实例

    def insert_mongo(self, item, collection):
        timestamp = int(datetime.datetime.now().timestamp())
        item['timestamp'] = timestamp

        col = self.mongo_client[collection]
        col.insert_one(item)

    async def content_handler(self, data):

        tasks = []
        insert_data = []

        for item_str in data:

            item, mongo_key, sub_path, down_header = json.loads(item_str)
            insert_data.append([mongo_key, item])
            tasks.append(
                asyncio.create_task(
                    self.files_handler(item, sub_path, down_header)))

        await asyncio.gather(*tasks)

        for mongo_key, item in insert_data:
            self.insert_mongo(item, mongo_key)

    @cookie_decorator
    async def files_handler(self, item, sub_path, down_header):

        for record in item['data']:

            all_files = record.get('attachments', []) + record.get(
                'images', [])
            if not all_files:
                continue

            try:
                await self.upload_files_asynchronously(all_files, sub_path,
                                                       down_header)
                self.replace_content(record)
            except Exception as e:
                logger.error(
                    'Failed to handle item files, err: {}, item: {}'.format(
                        repr(e), item))

    def retry_(self, retry):

        retry_times = retry.get('retry_times', 0) + 1
        file_url = retry["file_url"] if "file_url" in retry else retry['url']
        if retry_times <= 3:
            logger.info(
                f'retry upload attachment {retry_times} times -> url: {file_url}'
            )
            retry['retry_times'] = retry_times

            return True
        else:
            logger.info(f'give up retry upload attachment: {file_url}')
            if 'retry_times' in retry:
                retry.pop('retry_times')

            return False

    async def upload_files_asynchronously(self, all_files, sub_path,
                                          down_header):
        upload_files_tasks = []
        for file_ in all_files:

            filename, url = file_['filename'], file_["file_url"]

            upload_files_tasks.append(
                asyncio.create_task(
                    self.upload_asynchronously(url, filename, sub_path,
                                               down_header, file_)))

        await asyncio.gather(*upload_files_tasks)

    async def upload_asynchronously(self, url, filename: string, sub_path,
                                    down_headers, file_item):

        content = await self.download_total_file(url, down_headers)
        if not content:
            return

        with patch.object(self,
                          '_upload',
                          new_callable=AsyncMock,
                          return_value='test_tmp_path') as mocked_upload:
            path = await mocked_upload(url, content, filename, sub_path)
        if path:
            file_item['file_url'] = path

    @decorator.retry_decorator_custom(
        retry_times=const.DEFAULT_RETRY_TIMES,
        need_sleep=False,
        err_result=None,
        err_log_cnt=
        'Give up retry get attachment size: {}, err: {err}, retry_times: {retry_times}'
    )
    async def get_file_size(self, url, down_headers):

        proxy_url = get_proxy()
        head_resp = await self.session.head(
            url,
            proxy=proxy_url,
            headers=down_headers,
            timeout=aiohttp.ClientTimeout(const.DOWNLOAD_FILE_EXPIRE_TIME))

        file_length = head_resp.headers.get('Content-Length', None)
        if file_length is None:
            return -1
        try:
            file_size = int(file_length)
            return file_size
        except Exception:
            return

    async def download_total_file(self, url, down_headers):
        # logger.info('\n' + '-' * 20 + '开始下载' + '-' * 20 +
        #             '\nurl: {}\n'.format(url) + '-' * 50)

        download_tasks = []
        chunk_size = const.RESUMABLE_DOWNLOAD_CHUNK_SIZE
        sem = asyncio.Semaphore(const.DOWNLAOD_CONCURRENCY)

        with patch.object(self,
                          'get_file_size',
                          new_callable=AsyncMock,
                          return_value=1024) as mocked_size:
            file_size = await mocked_size(url, down_headers)

        if file_size is None:
            logger.info('{} 长度异常，取消下载'.format(url))
            return

        elif 0 < file_size < const.DOWNLOAD_FILE_SIZE_LIMIT:
            for start in range(0, file_size, chunk_size):
                end = min(start + chunk_size - 1, file_size - 1)
                download_tasks.append(
                    asyncio.ensure_future(
                        self.download_resumable(url,
                                                down_headers=down_headers,
                                                start=start,
                                                end=end,
                                                sem=sem)))

        elif file_size == -1 or file_size == 0:
            download_tasks.append(
                asyncio.ensure_future(
                    self.download_resumable(url,
                                            down_headers=down_headers,
                                            start=0,
                                            end='',
                                            sem=sem)))

        elif file_size >= const.DOWNLOAD_FILE_SIZE_LIMIT:
            msg = package_notice_content(url, '文件超过上传限制大小')
            notice.ding_talk_client.send_msg(msg)
            return  # 后端暂时不支持大于500M的文件上传

        else:
            logger.info('{} 长度小于0，取消下载'.format(url))
            return

        try:
            results = await asyncio.gather(*download_tasks,
                                           return_exceptions=False)
        except (asyncio.CancelledError, DownloadException, Exception) as e:
            logger.error('{} 文件分段下载失败，取消当前文件所有任务下载，err：{}'.format(url, str(e)))
            for task in download_tasks:
                task.cancel()
            return

        file_content = bytearray()
        for cnt in results:
            file_content.extend(cnt)

        # logger.info('\n' + '-' * 20 + '下载完成' + '-' * 20 +
        # '\nurl: {}\n'.format(url) + '-' * 50)
        return file_content

    async def download_resumable(self, url, down_headers, start, end, sem):
        async with sem:
            # logger.info('{} ***** {}:{} 开始下载'.format(url, start, end))

            down_headers['Range'] = f'bytes={start}-{end}'
            await asyncio.sleep(60)
            with patch.object(self,
                              '_download',
                              new_callable=AsyncMock,
                              return_value=b'test') as mocked_download:
                content = await mocked_download(url, down_headers)
            if not content:
                raise DownloadException('{} 的 {}:{} 分段内容下载失败'.format(
                    url, start, end))

            # logger.info('{} ***** {}:{} 下载结束'.format(url, start, end))
            return content

    @decorator.retry_decorator_custom(
        retry_times=const.DEFAULT_RETRY_TIMES,
        need_sleep=False,
        err_result='',
        err_log_cnt=
        'Give up retry dowload attachment: {}, err: {err}, retry_times: {retry_times}'
    )
    async def _download(self, url, down_headers):

        try:
            proxy_url = get_proxy()
            download_resp = await self.session.get(
                url,
                proxy=proxy_url,
                headers=down_headers,
                timeout=aiohttp.ClientTimeout(const.DOWNLOAD_FILE_EXPIRE_TIME))

            if download_resp.status != 200 and download_resp.status != 206:
                raise DownloadException(
                    "Invalid downloading response: {}.".format(
                        download_resp.reason))

            content = await download_resp.read()
            return content

        except asyncio.TimeoutError as e:

            error = "File download Timeout. url: {}, proxy_url: {}, err: {}, detail err: {}".format(
                url, proxy_url, str(e), repr(e))

            raise DownloadException(error)

        except Exception as e:

            error = "An unknown error occurred during file download. url: {}, proxy_url: {}, err: {}, detail err: {}".format(
                url, proxy_url, str(e), repr(e))

            raise DownloadException(str(e))

    @decorator.retry_decorator_custom(
        retry_times=const.DEFAULT_UPLOAD_RETRY_TIMES,
        need_sleep=True,
        err_result='',
        err_log_cnt=
        'Give up retry upload attachment: {}, err: {err}, retry_times: {retry_times}'
    )
    async def _upload(self, file_url, content, filename, sub_path):
        # logger.info('\n' + '-' * 20 + '开始上传' + '-' * 20 +
        #             '\nfile_url: {}\nsub_path: {}\nfilename: {}\n'.format(
        #                 file_url, sub_path, filename) + '-' * 50)

        try:

            data = FormData(quote_fields=False)
            data.add_field('file', content, filename=filename)
            data.add_field('subPath', sub_path)

            upload_resp = await self.session.post(
                self.upload_url,
                data=data,
                headers=self.upload_headers,
                timeout=aiohttp.ClientTimeout(
                    total=const.UPLOAD_FILE_EXPIRE_TIME))

            if upload_resp.status != 200:

                raise UploadException('Invalid uploading response: {}'.format(
                    upload_resp.reason))

            result = await upload_resp.json()

            if result.get('code') is None or result['code'] != 0:

                raise UploadException('Invalid uploading response: {}'.format(
                    result.get('msg', '')))

            if not result.get('data'):
                raise UploadException('Invalid result: {}'.format(result))

            # logger.info('\n' + '-' * 20 + '上传完成' + '-' * 20 +
            #             '\nfile_url: {}\nsub_path: {}\nfilename: {}\n'.format(
            #                 file_url, sub_path, filename) + '-' * 50)
            return result['data'][0]

        except Exception as e:

            error = "An unknown error occurred during file upload. url: {}, err: {}, detail err: {}".format(
                file_url, str(e), repr(e))

            raise UploadException(error)

    def replace_content(self, record):

        all_files = record.get('attachments', []) + record.get('images', [])

        for file_item in all_files:

            if not record.get("content", False):
                continue

            ori_url = file_item['ori_url']
            path = file_item['file_url']

            record['content'] = record['content'].replace(ori_url, path)

    def package_file_object(self,
                            url: string,
                            filename: string,
                            headers: dict = None,
                            **kwargs):
        file_resp = self._get(url, headers)

        files = [('file', (
            filename,
            file_resp.content,
        ))] if file_resp.status_code == 200 else []

        return files

    def upload_to_file_system(self,
                              url: string,
                              full_path: string,
                              headers: dict = None):

        try:
            sub_path, filename = full_path.split('/')
            payload = {'subPath': sub_path}

            files = self.package_file_object(url, filename, headers)

            if files:
                path = self._upload(files, payload)
            else:
                path = url

            return path

        except (UploadException, DownloadException) as e:

            logger.error(
                'Failed to Upload the file to the file system, err: {}, url: {}'
                .format(e, url))

            return url
            # TODO: 失败任务重试

    def _get(self, url, headers=None):

        try:
            resp = requests.request('GET', url, headers=headers)
        except Exception as e:
            raise DownloadException(str(e))

        return resp

    def _upload_sync(self, files, payload):
        try:

            resp = requests.request("POST",
                                    self.upload_url,
                                    headers=self.upload_headers,
                                    files=files,
                                    data=payload)

            if resp.status_code != 200:
                raise UploadException(resp.text)

            result = resp.json()

            if not result.get('data'):
                raise UploadException('Invalid result: {}'.format(result))

            return result['data']

        except Exception as e:
            raise UploadException(str(e))

    def close_global_session(self):

        self.loop.run_until_complete(self.session.close())


def item_handler(data):

    loop = asyncio.new_event_loop()

    handler = UploadFileHandler()

    handler.loop = loop

    connector = aiohttp.TCPConnector(verify_ssl=False, loop=loop)

    handler.session = aiohttp.ClientSession(loop=loop, connector=connector)

    tasks = [loop.create_task(handler.content_handler(data))]

    loop.run_until_complete(asyncio.wait(tasks))

    logger.info('处理 {} 个 item 完成'.format(len(data)))

    handler.close_global_session()

    handler.mongo_client.close()  # 及时关闭连接，否则子进程较多的时候可能会发生连接较多的情况


def main():
    logger.info('开始处理item ……………………')

    process_count = multiprocessing.cpu_count() // 3

    pool = multiprocessing.Pool(process_count)

    data_list = redis_client.lrange(const.REDIS_ITEM_KEY, 0,
                                    const.DEFAULT_UPLOAD_BATCH_SIZE)
    if not data_list:
        # 没有需要保存的item
        return

    for index in range(
            -1, const.DEFAULT_UPLOAD_BATCH_SIZE - const.UPLOAD_SLICE + 1,
            const.UPLOAD_SLICE):

        cur_index = index + 1
        end_index = cur_index + const.UPLOAD_SLICE

        data = data_list[cur_index:end_index]
        if not data:
            break

        pool.apply_async(item_handler, args=(data, ))

    pool.close()
    pool.join()

    logger.info('处理item结束 ……………………')


async def download_file_with_cookies(session, file_url, headers, data):

    try:
        resp = await session.post(file_url, json=data, headers=headers)
        if resp.status != 200:
            return ''
        content = await resp.read()
    except Exception as e:
        logger.error('Download file error: {}'.format(str(e)))
        return ''

    return content


if __name__ == '__main__':

    handler = UploadFileHandler()
    handler.main()
