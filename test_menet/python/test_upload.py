import json
import os
import random
import time
import requests
import string
import asyncio
import aiohttp
import datetime

import multiprocessing

from os import environ
from aiohttp.formdata import FormData
from ...menet.common_tools import db, const, logger, notice, scrapy_settings

import aiohttp
import asyncio

logger = logger.Logger('UploadLogger')


async def fetch_file_size(session, url):
    async with session.head(url) as response:
        size = int(response.headers.get('Content-Length', 0))
        return size


async def fetch_file_content(session, url, start, end):
    headers = {'Range': f'bytes={start}-{end}'}
    async with session.get(url, headers=headers) as response:
        content = await response.read()
        return content


async def main():
    url = 'http://example.com/file'
    async with aiohttp.ClientSession() as session:
        size = await fetch_file_size(session, url)
        print(f'File size: {size}')

        # Calculate the range for each segment
        segment_size = size // 4
        ranges = [(i * segment_size, (i + 1) * segment_size - 1)
                  for i in range(4)]

        # Fetch each segment using different IP addresses (proxies)
        proxies = [
            'http://ip1:port1', 'http://ip2:port2', 'http://ip3:port3',
            'http://ip4:port4'
        ]
        tasks = [
            fetch_file_content(session, url, start, end)
            for start, end in ranges
        ]
        contents = await asyncio.gather(*tasks)

        # Save the content to local file
        with open('file', 'wb') as f:
            for content in contents:
                f.write(content)


class UploadException(Exception):
    pass


class DownloadException(Exception):
    pass


def retry_decorator(func):

    async def wrapper(*args, **kwargs):

        url = args[1]

        download_key = 'download_{}'.format(url)
        upload_key = 'upload_{}'.format(url)

        result = ''

        while True:

            try:

                result = await func(*args, **kwargs)

            except DownloadException as e:

                retry_times = db.redis_client.get(download_key) or 0

                if retry_times:
                    retry_times = int(retry_times.decode())

                if retry_times >= const.DEFAULT_RETRY_TIMES:
                    logger.info(
                        f'give up retry dowload attachment: {url}, err: {e}')
                    break

                retry_times = db.redis_client.incrby(download_key, 1)

                await asyncio.sleep(random.randint(0, 3))

            except UploadException as e:

                retry_times = db.redis_client.get(upload_key) or 0

                if retry_times:
                    retry_times = int(retry_times.decode())

                # 由于目前上传文件接口不稳定，经常超时，暂时不做过多尝试
                if retry_times >= const.DEFAULT_UPLOAD_RETRY_TIMES:
                    logger.info(
                        f'give up retry upload attachment: {url}, err: {e}')

                    # 暂时不开启通知，待上传接口稳定后开启
                    # TODO:控制消息发送频率，建议单独将通知消息放到一个队列，由定时任务去消费通知
                    # msg = package_notice_content(url, str(e))
                    # notice.ding_talk_client.send_msg(msg)
                    break

                retry_times = db.redis_client.incrby(upload_key, 1)
                await asyncio.sleep(random.randint(0, 3))
            else:
                break

        db.redis_client.delete(upload_key, download_key)
        return result

    return wrapper


class Test:
    upload_url = scrapy_settings.UPLOAD_URL
    upload_headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Host': '219.128.140.162:20190',
        # 'Origin': 'http://219.128.140.162:20190',
        # 'Pragma': 'no-cache',
        # 'Proxy-Connection': 'keep-alive',
        # 'Referer': 'http://219.128.140.162:20190/dasui/',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Authorization': scrapy_settings.TOKEN,
        # "User-Agent":
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
    }

    async def main(self, url, down_headers, filename, sub_path):

        content = await self.download_total_file(url, down_headers)

        if not content:
            return

        path = await self._upload(url, content, filename, sub_path)
        print('path: {}'.format(path))

        await self.session.close()

    async def download_total_file(self, url, down_headers):
        print('{} 准备下载'.format(url))
        proxy_url = None

        file_content = bytearray()
        chunk_size = 1024 * 1024

        head_resp = await self.session.head(url,
                                            proxy=proxy_url,
                                            headers=down_headers,
                                            timeout=aiohttp.ClientTimeout(60))
        file_size = int(head_resp.headers.get('Content-Length', 0))
        if not file_size:
            return

        for start in range(0, file_size, chunk_size):
            end = min(start + chunk_size - 1, file_size - 1)
            await self._download(url,
                                 down_headers=down_headers,
                                 start=start,
                                 end=end,
                                 file_content=file_content)

        print('{} 完成下载'.format(url))
        return file_content

    @retry_decorator
    async def _download(self, url, down_headers, start, end, file_content):
        print('{} 下载 {} 到 {} 开始'.format(url, start, end))
        proxy_url = None

        try:
            down_headers['Range'] = f'bytes={start}-{end}'

            download_resp = await self.session.get(
                url,
                proxy=proxy_url,
                headers=down_headers,
                timeout=aiohttp.ClientTimeout(60))

            if download_resp.status != 200 and download_resp.status != 206:
                raise DownloadException(
                    "Invalid downloading response: {}.".format(
                        download_resp.reason))

            content = await download_resp.read()
            print('{} 下载 {} 到 {} 完成'.format(url, start, end))
            return content

        except asyncio.exceptions.TimeoutError or asyncio.TimeoutError as e:

            # proxy_instance.remove_proxy(proxy)

            error = "File download Timeout. url: {}, proxy_url: {}, err: {}, detail err: {}".format(
                url, proxy_url, str(e), repr(e))

            raise DownloadException(error)

        except Exception as e:

            # bproxy_instance.remove_proxy(proxy)

            error = "An unknown error occurred during file download. url: {}, proxy_url: {}, err: {}, detail err: {}".format(
                url, proxy_url, str(e), repr(e))

            raise DownloadException(str(e))

    async def _upload(self, file_url, content, filename, sub_path):

        try:
            print('{} 准备上传'.format(file_url))
            # with open(filename, 'wb') as f:
            #     f.write(content)

            data = FormData(quote_fields=False)
            data.add_field('file', content, filename=filename)
            data.add_field('subPath', sub_path)

            upload_resp = await self.session.post(
                self.upload_url,
                data=data,
                headers=self.upload_headers,
                timeout=aiohttp.ClientTimeout(total=60))

            if upload_resp.status != 200:

                raise UploadException('Invalid uploading response: {}'.format(
                    upload_resp.reason))

            result = await upload_resp.json()

            if not result.get('data') or not result.get('data')['url']:
                raise UploadException('Invalid result: {}'.format(result))

        except Exception as e:

            error = "An unknown error occurred during file upload. url: {}, err: {}, detail err: {}".format(
                file_url, str(e), repr(e))

            raise UploadException(error)
        print('{} 准备成功, path: {}'.format(file_url, result['data']['url']))


def main():

    loop = asyncio.new_event_loop()

    handler = Test()

    handler.loop = loop

    connector = aiohttp.TCPConnector(verify_ssl=False, loop=loop)

    handler.session = aiohttp.ClientSession(loop=loop, connector=connector)

    kwargs = {
        'url': 'http://amr.gd.gov.cn/attachment/0/365/365086/2647892.zip',
        'down_headers': {
            'Host': 'amr.gd.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        },
        'filename': '2647892.zip',
        'sub_path': '20230403_test_local'
    }

    loop.run_until_complete(handler.main(**kwargs))
