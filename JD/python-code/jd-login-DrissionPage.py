import csv
import os
import random
import time

from DrissionPage import ChromiumOptions, ChromiumPage, WebPage
from DrissionPage.common import ActionChains
from lxml.html import etree
from PIL import Image


class JDCrawler:

    # from DrissionPage.easy_set import set_paths
    # 配置已保存到文件：/home/feng/workspace/myWeb/.venv/lib/python3.10/site-packages/DrissionPage/configs/configs.ini
    # set_paths(browser_path='/usr/bin/google-chrome-stable')
    # 弹出浏览器窗口，启动浏览器：google-chrome-stable  --remote-debugging-port=9222，通过代码接管当前浏览器
    # 开启无痕模式：google-chrome --remote-debugging-port=9222 --incognito
    base_dir = os.path.dirname(os.path.dirname(__file__))
    imgs_path = os.path.join(base_dir, 'images')

    # co = ChromiumOptions()
    # co.set_paths(local_port=9222)   # 弹出浏览器窗口
    # page = ChromiumPage(addr_driver_opts=co)

    def __init__(self) -> None:
        co = ChromiumOptions()
        co.set_proxy('http://59.58.211.243:8888')
        co.set_no_imgs(True)
        self.init_page = WebPage('d', driver_or_options=co)

        self.down_img_count = 90
        self.down_dir = os.path.join(self.imgs_path, 'jd4')

    def auto_login(self, url):

        tab_id = self.init_page.new_tab(url)  # 会导致截图、或者获取html内容只能拿到默认打开的无效标签页
        page = self.init_page.get_tab(tab_id)
        page.wait.load_start()
        print('--------------------进入页面: {} --------------------'.format(tab_id))

        try:

            page.wait.ele_display('#loginname', timeout=60)
            print('--------------------等待 {} 页面加载完成--------------------'.format(tab_id))

            bf_content = page.html
            self.save_page('htmls/bf_content.html', bf_content)
            self.save_page('cookies/bf_cookie', str(page.cookies))
            print('--------------------登录之前--------------------')

            ele = page.ele('#loginname', timeout=30)
            ele.input('rhftestaccount')
            page.ele('#nloginpwd', timeout=30).input('feng33314')
            logbtn = page.ele('#loginsubmit', timeout=30)
            time.sleep(2)
            logbtn.click()
            page.wait.load_start()

            af_content = page.html
            self.save_page('htmls/af_content.html', af_content)
            self.save_page('cookies/af_cookie', str(page.cookies))
            print('--------------------点击登录之后--------------------')

            # self.captch(3, page, logbtn)  # 滑块验证码

        except Exception as e:
            print('操作页面失败，错误：{}'.format(e))

        # finally:
        #     self.init_page.close_tabs(tab_id)   # 关闭当前页面

        print('--------------------end--------------------')

    def search(self, url, product):
        start_t = time.perf_counter()
        print(f'--------------------开始: {start_t} --------------------')
        tab_id = self.init_page.new_tab(url)
        page = self.init_page.get_tab(tab_id)
        page.wait.load_start()
        print('--------------------进入搜索页面: {} --------------------'.format(tab_id))

        try:

            search_key = page.ele('#key', timeout=30)
            for val in product:
                time.sleep(0.5)
                search_key.input(val, clear=False)

            time.sleep(1)

            submit = page.ele('.button')
            submit.click()
            page.wait.load_start()

            af_content = page.html
            self.save_page('htmls/af_search.html', af_content)
            self.save_page('cookies/af_search_cookie', str(page.cookies))
            print('--------------------点击搜索之后--------------------')

            self.screen_shot(page, 'images/search_result.png')

            print('--------------------开始获取商品信息--------------------')
            self.catch_products(af_content)
            print('--------------------获取商品信息结束--------------------')

        except Exception as e:
            print('操作页面失败，错误：{}'.format(e))

        else:
            end_t = time.perf_counter()
            spend_t = end_t - start_t
            print('--------------------结束耗时: {:.8f} --------------------'.format(spend_t))

        finally:
            self.init_page.close_tabs(tab_id)  # 关闭当前页面

        print('--------------------end--------------------')

    def catch_products(self, html):

        selector = etree.HTML(html)
        results = []
        products = selector.xpath(
            '//div[@id="J_goodsList"]/ul[@class="gl-warp clearfix"]/li[@class="gl-item"]/div[@class="gl-i-wrap"]')

        try:
            for product in products:
                p_img_obj = product.xpath('div[@class="p-img"]/a/img')[0].attrib
                p_img = 'https:' + (p_img_obj.get('src') or p_img_obj.get('data-lazy-img') or '')
                p_price = product.xpath('div[@class="p-price"]/strong/i')[0].text
                p_name = product.xpath('div[@class="p-name p-name-type-2"]/a/em')[0].xpath('string(.)')
                p_detail_addr = 'https:' + (product.xpath('div[@class="p-name p-name-type-2"]/a')[0].attrib.get('href')
                                            or '')
                p_commit = product.xpath('div[@class="p-commit"]/strong/a')[0].xpath('string(.)')  # 评价
                p_shop_name = product.xpath('div[@class="p-shop"]/span/a')[0].xpath('string(.)')
                p_shop_addr = 'https' + (product.xpath('div[@class="p-shop"]/span/a')[0].attrib.get('href') or '')
                p_icons = product.xpath('div[@class="p-icons"]/i/text()')
                print('--------------------准备获取详情--------------------')
                print(f'{p_name}: {p_price} {p_shop_name} {p_detail_addr}')
                try:
                    detail_info = self.view_detail(p_detail_addr)
                except Exception as e:
                    print('获取详情失败，{}'.format(e))
                    detail_info = {}
                print('--------------------获取详情结束--------------------')

                results.append({
                    'p_img': p_img,
                    'p_price': p_price,
                    'p_name': p_name,
                    'p_detail_addr': p_detail_addr,
                    'p_commit': p_commit,
                    'p_shop_name': p_shop_name,
                    'p_shop_addr': p_shop_addr,
                    'p_icons': p_icons,
                    'detail_info': detail_info
                })
                time.sleep(random.randrange(1, 5))

        except Exception as e:
            print('获取商品信息失败，{}'.format(e))

        finally:
            if results:
                with open(os.path.join(self.base_dir, "result.csv"), "w", newline="", encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(results)
            print('--------------------写入CSV完成--------------------')

    def view_detail(self, url):

        results = {}

        try:
            tab_id = self.init_page.new_tab()
            page = self.init_page.get_tab(tab_id)
            page.wait.set_targets(
                'color.yiyaojd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc')
            page.get(url)
            page.wait.load_start()
            resp = page.wait.data_packets()
            if resp:
                resp_data = resp if isinstance(resp, dict) else resp.body
            else:
                resp_data = {}

            detail_content = page.html
            self.save_page('htmls/detail_content.html', detail_content)
            self.save_page('cookies/detail_content_cookie', str(page.cookies))

            selector = etree.HTML(detail_content)

            sku_name = selector.xpath('//div[@class="sku-name"]')[0].text
            p_price = selector.xpath(
                '//div[@class="summary summary-first"]/div[@class="summary-price-wrap"]/div[@class="summary-price J-summary-price"]/div[@class="dd"]/span[@class="p-price"]/span'
            )[1].text
            summary_quan = selector.xpath(
                '//div[@class="summary summary-first"]/div[@class="summary-price-wrap"]/div[@id="summary-quan"]'
            )[0].xpath('string(.)')
            J_summary_top = selector.xpath(
                '//div[@class="summary summary-first"]/div[@class="summary-price-wrap"]/div[@id="J-summary-top"]'
            )[0].xpath('string(.)')
            summary_stock = selector.xpath(
                '//div[@class="summary p-choose-wrap"]/div[@class="summary-stock"]')[0].xpath('string(.)')
            SelfAssuredPurchase_li = selector.xpath(
                '//div[@class="summary p-choose-wrap"]/div[@class="SelfAssuredPurchase li"]')[0].xpath('string(.)')
            summary_supply = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="summary-supply"]')[0].xpath(
                'string(.)')
            summary_weight = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="summary-weight"]')[0].xpath(
                'string(.)')
            choose_attrs = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="choose-attrs"]')[0].xpath(
                'string(.)')

            parameter_brand = selector.xpath('//div[@class="p-parameter"]/ul[@id="parameter-brand"]/li')[0].xpath(
                'string(.)')
            parameter_brand_info = {
                i.text.split('：')[0]: i.text.split('：')[-1]
                for i in selector.xpath('//div[@class="p-parameter"]/ul[@class="parameter2 p-parameter-list"]/li')
            }
            Ptable = {
                i.getchildren()[0].text: i.getchildren()[1].text
                for i in selector.xpath('//div[@class="Ptable"]/div[@class="Ptable-item"]/dl//dl')
            }

            results = {
                'sku_name': sku_name,
                'p_price': p_price,
                'summary_quan': summary_quan,
                'J_summary_top': J_summary_top,
                'summary_stock': summary_stock,
                'SelfAssuredPurchase_li': SelfAssuredPurchase_li,
                'summary_supply': summary_supply,
                'summary_weight': summary_weight,
                'choose_attrs': choose_attrs,
                "parameter_brand": parameter_brand,
                "parameter_brand_info": parameter_brand_info,
                "Ptable": Ptable,
                'shopInfo': resp_data
            }

            star_div = selector.xpath('//div[@class="star"]/div[@class="star-bg"]/div[@class="star-gray"]')
            if star_div:
                star = star_div[0].attrib['title']
                results['shopInfo']['star'] = star
        except Exception as e:
            print('操作页面失败，错误：{}'.format(e))

        finally:
            self.init_page.close_tabs(tab_id)  # 关闭当前页面

        return results

    def save_page(self, file_name, content):
        # 文档编码模式获取：进入浏览器控制台，输入 document.charset
        # 浏览器打开文档乱码，将文档中的 head标签下 <meta charset="GBK"> 的 编码格式改为 utf-8

        with open(os.path.join(self.base_dir, file_name), 'w', encoding='utf-8') as f:
            f.write(content)

    def read_page(self, file_name):

        with open(file_name, 'r') as f:
            content = f.read()

        return content

    def screen_shot(self, page, file_name='images/screen_shot.png'):
        page.get_screenshot(path=os.path.join(self.base_dir, file_name), full_page=True)

    def end(self):
        self.init_page.quit()

    def captch(self, step, page, logbtn):
        slider = page.ele('.JDJRV-suspend-slide')
        if slider:
            print("--------------------进入滑块验证码流程--------------------")
            if step == 1:
                print("--------------------第一次登录开始下载素材--------------------")
                for i in range(self.down_img_count - 1):
                    self.get_images(page, step)
            elif step == 2:
                print("--------------------已下载过素材合并素材--------------------")
                img_path = os.path.join(self.imgs_path, '/jd3')
                i = 1
                while i <= 10:
                    if os.path.exists(img_path + str(i) + "d.png") and os.path.exists(img_path + str(i) + "u.png"):
                        imgu = Image.open(img_path + str(i) + "u.png")
                        imgd = Image.open(img_path + str(i) + "d.png")
                        img_temp = imgu.crop((0, 0, imgu.width, imgu.height / 2))
                        #img_temp.show();
                        imgd.paste(img_temp, (0, 0))
                        imgd.save(self.down_dir + str(i) + "m.png")
                        print("合并第" + str(i) + "张")
                    i = i + 1
            elif step == 3:
                print("--------------------已有素材开始登录--------------------")
                if slider:
                    for i in range(50):
                        self.do_login(page, step)
                        time.sleep(1.7)
                        title = page.title
                        if title == "京东-欢迎登录":
                            continue
                        else:
                            print("--------------------登录成功 {} --------------------".format(title))
                            break
                else:
                    time.sleep(1.2)
                    logbtn.click()

        else:
            print('--------------------页面未发现滑块直接登录--------------------')
            time.sleep(0.5)
            logbtn.click()

    def do_login(self, page, step):
        print("--------------------enter do_login--------------------")
        curent_img = self.get_images(page, step)
        curent_img.save(self.imgs_path + '/current.png')
        files = os.listdir(self.down_dir)
        simi_dict = dict()

        for f in files:
            temp_img = Image.open(self.down_dir + f)
            simi_val = self.compare2(temp_img, curent_img)
            simi_dict[f] = simi_val

        mini = min(simi_dict, key=simi_dict.get)
        image1 = Image.open(self.down_dir + mini)
        gap = self.get_gap(image1, curent_img)
        print(gap)

        track = self.get_track7(gap + 20.85)
        self.dragging(page, track)
        print("--------------------exit do_login--------------------")

    def get_images(self, page, step, find_this_img=""):
        print("--------------------enter get_images--------------------")
        time.sleep(0.8)
        btn_refesh = page.ele('.JDJRV-img-refresh')
        img = page.ele('.JDJRV-bigimg')
        location = img.location
        size = img.size
        left = location[0]  # x 坐标
        top = location[1]  # y 坐标
        right = left + size[0]  # width
        bottom = top + size[1]  # height

        time.sleep(0.99)
        page_snap_obj = self.get_snap(page)
        image_obj = page_snap_obj.crop((left, top, right, bottom))  # 返回图片的矩形区域

        # 图片相似才保存
        if find_this_img != "":
            dog = Image.open(find_this_img)
            if self.compare2(dog, image_obj) < 0.6:
                image_obj.save(self.imgs_path + '/image_' + str(time.time()) + '.png')
        else:
            image_obj.save(self.imgs_path + '/image_obj_' + str(time.time()) + '.png')
        if step == 1:
            btn_refesh.click()
        print("--------------------exit get_images--------------------")
        return image_obj

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 45
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold)
                and abs(pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_track7(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                a = random.uniform(2, 5)
            else:
                a = -(random.uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
                tracks.append(round(x, 2))

            elif 1 < current - distance < 1.5:
                x = x - 1.4
                tracks.append(round(x, 2))
            elif 1.5 < current - distance < 3:
                x = x - 1.8
                tracks.append(round(x, 2))

            else:
                tracks.append(round(x, 2))

        print(sum(tracks))
        return tracks

    def compare2(self, image1, image2):
        '''
        :图片相识度简单对比 图片越像返回值越趋近于0，返回 0-1 认为图片非常相似
        :param image1: 图片1对象
        :param image2: 图片2对象
        :return: 返回对比的结果
        '''

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b)**2, histogram1, histogram2))) / len(histogram1))
        return differ / 100

    def dragging(self, tracks, page):
        # 按照行动轨迹先正向滑动，后反滑动
        button = page.ele('.JDJRV-slide-btn')
        ActionChains(page).hold(button)

        for track in tracks:
            ActionChains(page).move_to(button, offset_x=track, offset_y=0)

        time.sleep(0.18)
        #反向滑动
        # tracks_backs = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]  #-20
        # for back in tracks_backs:
        #      ActionChains(self.dr).move_by_offset(xoffset=back, yoffset=0).perform()

        ActionChains(page).move_to(button, offset_x=-3, offset_y=0)
        ActionChains(page).move_to(button, offset_x=3, offset_y=0)

        time.sleep(0.7)
        ActionChains(page).release(button)

    def get_snap(self, page):
        """
        屏幕截图对象
        """
        full_snap = page.get_screenshot(os.path.join(self.imgs_path, 'full_snap.png'))
        page_snap_obj = Image.open(full_snap)
        return page_snap_obj

    def test(self):
        url = "https://item.jd.com/100018280931.html"
        tab_id = self.init_page.new_tab()
        page = self.init_page.get_tab(tab_id)

        page.wait.set_targets('color.yiyaojd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc')
        page.get(url)
        page.wait.load_start()
        resp_data = page.wait.data_packets()
        print(resp_data)


if __name__ == '__main__':
    login_url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
    search_url = "https://www.jd.com/"
    crawl = JDCrawler()
    # crawl.auto_login(login_url)
    crawl.search(search_url, '盐酸氨基葡萄糖')

    # test_file_path = os.path.join(crawl.base_dir, 'htmls/af_search.html')
    # cnt = crawl.read_page(test_file_path)
    # crawl.catch_products(cnt)

    # crawl.test()
