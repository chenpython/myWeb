import asyncio
import logging
import multiprocessing
import os
import string
import time
from multiprocessing import Manager
from aiohttp.formdata import FormData

import aiohttp

loop = asyncio.get_event_loop()

logger = logging.getLogger(__name__)


# class CustomBaseDistributedSpider(CustomBaseSpider):

#     @property
#     def distributed_lock(self):
#         distributed_lock = 'distributed_lock:{}:{}'.format(
#             self.name, self.public_content['crawl_time'])

#         return distributed_lock

#     def set_distributed_lock(self):
#         success = redis_client.setnx(self.distributed_lock, 1)
#         if success:
#             redis_client.expire(self.distributed_lock, 60 * 60 * 24 * 30)
#             return True
#         return False

#     def closed(self, reason):
#         redis_client.delete(self.distributed_lock)
async def create_session():
    return aiohttp.ClientSession(loop=loop)


session = asyncio.get_event_loop().run_until_complete(create_session())


class UploadException(Exception):
    pass


class DownloadException(Exception):
    pass


# 业务类
class BaiJiaHao():

    async def upload_asynchronously(self,
                                    url,
                                    filename: string,
                                    sub_path,
                                    down_headers,
                                    title=''):

        # proxy = proxy_instance.random_one_proxy()

        # proxy_url = 'http://{}'.format(proxy)

        logger.info("sub_path: {}".format(sub_path))

        sub_path = sub_path['title']

        proxy_url = proxy = None

        try:

            download_start_time = time.perf_counter()

            download_resp = await session.get(url,
                                              proxy=proxy_url,
                                              headers=down_headers,
                                              timeout=5)

            if download_resp.status != 200:
                raise DownloadException(
                    "Invalid downloading response: {}.".format(
                        download_resp.reason))

            dowload_spend_time = time.perf_counter() - download_start_time

            logger.info('{}: 下载文件成功：{} \n耗时：{}'.format(title, url,
                                                       dowload_spend_time))

            redis_key = self.tmp_get_redis_key(dowload_spend_time)

            # redis_client.hincrby(const.DOWNLOAD_REQUEST_SUCCESS, redis_key, 1)

            # if dowload_spend_time >= 5:
            #     redis_client.hset('download-' + redis_key, url,
            #                       dowload_spend_time)

        except asyncio.exceptions.TimeoutError or asyncio.TimeoutError:

            # proxy_instance.remove_proxy(proxy)

            dowload_spend_time = time.perf_counter() - download_start_time

            logger.info('{}: 下载文件失败：{} \n耗时：{}'.format(title, url,
                                                       dowload_spend_time))

            # redis_client.hincrby(const.DOWNLOAD_REQUEST_FAILURE,
            #                      self.tmp_get_redis_key(dowload_spend_time), 1)

            return

        except Exception as e:

            # proxy_instance.remove_proxy(proxy)

            dowload_spend_time = time.perf_counter() - download_start_time

            logger.info('{}: 下载文件失败：{} \n耗时：{}'.format(title, url,
                                                       dowload_spend_time))

            # redis_client.hincrby(const.DOWNLOAD_REQUEST_FAILURE,
            #                      self.tmp_get_redis_key(dowload_spend_time), 1)

            logger.error('下载文件发生未知报错，错误：{}，url：{}'.format(e, url))

            return

        try:

            data = FormData(quote_fields=False)
            data.add_field('file', download_resp.content, filename=filename)
            data.add_field('subPath', sub_path)

            logger.info('{}：准备上传文件：{}'.format(title, url))

            upload_start_time = time.perf_counter()

            upload_resp = await session.post(self.url,
                                             data=data,
                                             headers=self.upload_headers,
                                             timeout=15)

            if upload_resp.status != 200:

                raise UploadException('Invalid uploading response: {}'.format(
                    upload_resp.reason))

            upload_spend_time = time.perf_counter() - upload_start_time

            logger.info('{}: 上传文件成功：{} \n耗时：{}'.format(title, url,
                                                       upload_spend_time))

            redis_key_1 = self.tmp_get_redis_key(upload_spend_time)

            result = await upload_resp.json()

            if not result.get('data') or not result.get('data')[0]:
                raise UploadException('Invalid result: {}'.format(result))

        except Exception as e:

            upload_spend_time = time.perf_counter() - upload_start_time

            logger.info('{}: 上传文件失败：{} \n耗时：{}'.format(title, url,
                                                       upload_spend_time))

            logger.error('上传文件发生报错，错误：{}，{}，url：{}'.format(
                str(e), repr(e), url))

            return

        return result['data'][0]

    async def get_author(self, rec):
        """
        协程代码
        """
        print('enter get author,wait for: %d' % rec['num'])
        # 模拟IO操作，耗时根据传进来的num决定
        await asyncio.sleep(rec['num'])
        # 返回协程任务完成后的结果
        return rec

    def run(self):
        # 假定我们有11个任务要跑，每个任务耗时为num秒，串行的话需要43秒。
        # 但我们这个demo跑完只需要这些任务中的最大值：8秒
        list = [
            {
                'title': 'title1',
                'num': 2
            },
            {
                'title': 'title2',
                'num': 1
            },
            {
                'title': 'title3',
                'num': 3
            },
            {
                'title': 'title4',
                'num': 8
            },
            {
                'title': 'title5',
                'num': 2
            },
            {
                'title': 'title6',
                'num': 5
            },
            {
                'title': 'title7',
                'num': 7
            },
            {
                'title': 'title8',
                'num': 3
            },
            {
                'title': 'title9',
                'num': 4
            },
            {
                'title': 'title10',
                'num': 3
            },
            {
                'title': 'title11',
                'num': 5
            },
        ]
        result = run_get_author_in_multi_process(list)
        print('result', result)


def get_chunks(iterable, chunks=1):
    """
    此函数用于分割若干任务到不同的进程里去
    """
    lst = list(iterable)
    return [lst[i::chunks] for i in range(chunks)]


def run_get_author(lists, queue):
    """
    这个就是子进程运行的函数，接收任务列表和用于进程间通讯的Queue
    """
    print('exec run_get_author.child process id : %s, parent process id : %s' %
          (os.getpid(), os.getppid()))
    # 每个子进程分配一个新的loop
    loop = asyncio.new_event_loop()
    # 初始化业务类，转成task或future
    spider = BaiJiaHao()
    tasks = [
        loop.create_task(
            spider.upload_asynchronously(
                'https://www.smpaa.cn/gjsdcg/files/file8289.pdf', 'test.pdf',
                rec, {
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
                })) for rec in lists
    ]
    # 协程走起
    loop.run_until_complete(asyncio.wait(tasks))
    # 往queue写入每个任务的结果
    for task in tasks:
        queue.put(task.result())


def run_get_author_in_multi_process(task_lists):
    """
    父进程函数，主要是分割任务并初始化进程池，启动进程并返回结果
    """
    # process_count = len(tasks) % 2
    # 进程数这里我用机器上的核心数，注意：未考虑核心数比任务多的情况
    process_count = multiprocessing.cpu_count()
    print('process_count: %d' % process_count)
    split_lists = get_chunks(task_lists, process_count)
    pool = multiprocessing.Pool(process_count)
    queue = Manager().Queue()
    for lists in split_lists:
        pool.apply_async(run_get_author, args=(
            lists,
            queue,
        ))
    pool.close()
    pool.join()
    result = []
    # 从子进程读取结果并返回
    while not queue.empty():
        result.append(queue.get())
    return result


def prepare_item():

    if redis_client.exists(const.REDIS_ITEM_KEY):
        result = redis_client.lrange(const.REDIS_ITEM_KEY, 0, -1)
        redis_client.lpush('SPIDER_ITEMS_BACKUP', *result)
        return

    result = redis_client.lrange('SPIDER_ITEMS_BACKUP', 0, -1)
    redis_client.lpush(const.REDIS_ITEM_KEY, *result)


def tmp_get_redis_key(self, spend_time):

    if spend_time < 3:
        return 'rank1-fast'

    if spend_time >= 3 and spend_time < 5:
        return 'rank2-medium'

    if spend_time >= 5 and spend_time < 8:
        return 'rank3-slower'

    if spend_time >= 8:
        return 'rank4-high-slow'


# ======== 图片验证码补全代码 ===========


def get_image(browser, wait):
    """
    获取图片截图
    bg.png==>原始图片
    fullbg.png==>无滑块图片
    """
    button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/form/div[3]/div/div[3]/div[2]/div[1]/div[3]')))
    button.click()
    geetest_canvas_bg = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_bg')))
    time.sleep(0.5)
    js = 'var change = document.getElementsByClassName("geetest_canvas_slice");change[0].style = "display: none;"'
    browser.execute_script(js)
    geetest_canvas_bg.screenshot('bg.png')

    js = 'var change1 = document.getElementsByClassName("geetest_canvas_fullbg");change1[0].style = "display: block;"'
    browser.execute_script(js)
    time.sleep(0.5)
    geetest_canvas_fullbg = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_bg')))
    geetest_canvas_fullbg.screenshot('fullbg.png')
    image_bg = Image.open('bg.png')
    image_fullbg = Image.open('fullbg.png')
    js = 'var change = document.getElementsByClassName("geetest_canvas_slice");change[0].style = "display: block;"'
    browser.execute_script(js)
    return image_bg, image_fullbg


def get_diff_location(image1, image2):
    '''
    通过像素对比 找到缺口位置
    :param image1:
    :param image2:
    :return:
    '''
    for x in range(60, image1.size[0]):
        for y in range(1, image2.size[1]):
            if is_similar(image1, image2, x, y) == False:
                # 判断成立 表示xy这个点 两张图的像素点是不一样的
                return x


def is_similar(image1, image2, x, y):
    '''
    找两个像素点不同之处
    '''
    pixel1 = image1.getpixel((x, y))
    pixel2 = image2.getpixel((x, y))  # 元组

    for i in range(0, 3):
        if abs(pixel1[i] - pixel2[i]) >= 50:
            return False

    return True


def get_tracks(x: int):
    tracks = [0, 0]
    num = 0
    while num + 20 < x:
        num += 20
        tracks.append(20)
    while num + 10 < x:
        num += 10
        tracks.append(10)
    while num + 5 < x:
        num += 5
        tracks.append(5)
    while num + 3 < x:
        num += 3
        tracks.append(3)
    for i in range((x - num) + 2):
        tracks.append(1)
    tracks.append(-1)
    tracks.append(-1)
    return tracks


def get_gap(image1, image2):
    """
    获取缺口偏移量
    :param image1: 带缺口图片
    :param image2: 不带缺口图片
    :return:
    """
    left = 60
    print(image1.size[0])
    print(image1.size[1])
    for i in range(left, image1.size[0]):
        for j in range(image1.size[1]):
            if not is_pixel_equal(image1, image2, i, j):
                left = i
                return left
    return left


def is_pixel_equal(image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    threshold = 60
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(
            pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] -
                                                       pixel2[2]) < threshold:
        return True
    else:
        return False


def Geetest(url, path):
    # browser = webdriver.Firefox(executable_path=path)
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    image_bg, image_fullbg = get_image(browser, wait)
    x = get_diff_location(image_bg, image_fullbg)
    print('偏移距离：' + str(x))
    tracks = get_tracks(x - 5)
    elem = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
    ActionChains(browser).click_and_hold(elem).perform()
    for track in tracks:
        ActionChains(browser).move_by_offset(xoffset=track,
                                             yoffset=0).perform()
    time.sleep(1)
    ActionChains(browser).release(elem).perform()


# ======== 图片验证码补全代码 ===========

now = lambda: time.time()

if __name__ == '__main__':
    start = now()
    spider = BaiJiaHao()
    spider.run()
    print('done', 'TIME: ', now() - start)
