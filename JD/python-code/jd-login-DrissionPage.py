import base64
import csv
import os
import random
import time

import cv2
import ddddocr
import numpy as np
import requests
from DrissionPage import ChromiumOptions, ChromiumPage, WebPage
from DrissionPage.common import ActionChains, Keys
from lxml.html import etree


class JDCrawler:

    # from DrissionPage.easy_set import set_paths
    # 配置已保存到文件：/home/feng/workspace/myWeb/.venv/lib/python3.10/site-packages/DrissionPage/configs/configs.ini
    # set_paths(browser_path='/usr/bin/google-chrome-stable')
    # 弹出浏览器窗口，启动浏览器：google-chrome-stable  --remote-debugging-port=9222，通过代码接管当前浏览器
    # 开启无痕模式：google-chrome --remote-debugging-port=9222 --incognito
    base_dir = os.path.dirname(os.path.dirname(__file__))
    imgs_path = os.path.join(base_dir, 'images')
    slider_path = os.path.join(imgs_path, 'slider_imags')
    verify_code_path = os.path.join(imgs_path, 'verify_code')

    captch_items = {
        '验证',
    }

    # co = ChromiumOptions()
    # co.set_paths(local_port=9222)   # 弹出浏览器窗口
    # page = ChromiumPage(addr_driver_opts=co)

    def __init__(self) -> None:
        self.sys_proxy = '59.58.211.243:8888'
        co = ChromiumOptions()
        co.set_proxy('http://' + self.sys_proxy)
        co.set_no_imgs(True)
        self.init_page = WebPage('d', driver_or_options=co)

        self.down_img_count = 90
        self.down_dir = os.path.join(self.imgs_path, 'jd4')

    @staticmethod
    def handle_distance(distance):
        """将直线距离转为缓慢的轨迹"""

        slow_distance = []
        while sum(slow_distance) <= distance:
            slow_distance.append(random.uniform(1, 4))

        if sum(slow_distance) != distance:
            slow_distance.append(distance - sum(slow_distance))
        return slow_distance

    @staticmethod
    def img2cv(img_data):
        """openCV 读取 base64 图片"""
        data = img_data.replace('data:image/png;base64,', '')
        img_data = base64.b64decode(data)
        img = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.COLOR_RGB2BGR)
        return img

    @staticmethod
    def img2xy(bg_img, tp_img):
        """识别图片缺口位置

        Args:
            bg_img : 背景图片
            tp_img : 缺口图片

        Returns:
            返回缺口的左上角、右下角坐标
        """
        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
        tl = max_loc  # 左上角点的坐标

        th, tw = tp_pic.shape[:2]
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标

        # cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(os.path.join(JDCrawler.slider_path, "result_new.png"), bg_img)  # 保存在本地

        return max_loc, br

    def slider(self, page):
        # 保存背景图片、缺口图片
        # 背景图片
        bg_ele = page.ele('xpath://div[@class="JDJRV-bigimg"]/img')
        bg_img = bg_ele.attr('src')
        bg = self.img2cv(bg_img)
        # 缺口图片
        patch_ele = page.ele('xpath://div[@class="JDJRV-smallimg"]/img')
        patch_img = patch_ele.attr('src')
        patch = self.img2cv(patch_img)
        if bg is None or patch is None:
            raise Exception('滑块图片定位异常')
        # 识别图片缺口位置
        location = self.img2xy(bg, patch)
        print(f'缺口识别坐标：{location}')
        # 模拟轨迹，移动滑块
        upper_left = location[0]  # 缺口框的左上角坐标
        patch_position = patch_ele.location  #  滑块左上角坐标
        patch_size = patch_ele.size
        # 移动距离
        distance = upper_left[0] / 1.487603305785124
        # distance = abs((upper_left[0] + bg_ele.location[0])  # 缺口左上角x
        #                - patch_position[0]  # 缺口图片的左上角x
        #                - patch_size[1]  # 滑块宽度
        #                )
        tracks = self.handle_distance(distance + random.uniform(-1, 1))
        print(f'移动距离：{distance}，移动轨迹：{tracks}')

        button = page.ele('xpath://div[@class="JDJRV-slide-inner JDJRV-slide-btn"]')

        print('缺口图片的坐标：{}，滑动按钮的坐标：{}，背景图片坐标：{}'.format(patch_position, button.location, bg_ele.location))
        ac = ActionChains(page)
        print('开始移动滑块')
        ac.move_to(button)
        ac.hold(button)
        # 移动滑块
        for pos in tracks:
            y = random.uniform(-1, 2)
            ac.move(pos, y)
        # ac.move_to(button, distance + patch_size[0]).hold()
        self.screen_shot(page, 'images/slider_imags/slider_screen.png')
        ac.release(button)
        page.wait.load_start()
        time.sleep(5)
        print('滑动滑块完成')

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

            for _ in range(5):
                slider_ele = page.ele('xpath://div[@class="JDJRV-suspend-slide"]')
                if slider_ele:
                    self.slider(page)

            print('登录成功')

        except Exception as e:
            print('操作页面失败，错误：{}'.format(e))

        finally:
            self.init_page.close_tabs(tab_id)  # 关闭当前页面
            print('--------------------end--------------------')

    def check_is_captch_page(self, title):
        for item in self.captch_items:
            if item in title:
                return True
        return False

    def search(self, url, product):
        start_t = time.perf_counter()
        print(f'--------------------开始: {start_t} --------------------')
        tab_id = self.init_page.new_tab(url)
        page = self.init_page.get_tab(tab_id)
        page.wait.load_start()
        print('--------------------进入搜索页面: {} --------------------'.format(tab_id))

        try:
            title = page.ele('tag:title').text
            if self.check_is_captch_page(title):
                return

            search_key = page.ele('#key', timeout=30)
            for val in product:
                time.sleep(0.5)
                search_key.input(val, clear=False)

            time.sleep(1)

            submit = page.ele('.button')
            submit.click()
            page.wait.load_start()

            print('--------------------点击搜索之后--------------------')

            # af_content = page.html
            # self.save_page('htmls/af_search.html', af_content)
            # self.save_page('cookies/af_search_cookie', str(page.cookies))
            # self.screen_shot(page, 'images/search/search_result.png')

            print('--------------------开始滑动页面--------------------')
            page.scroll.to_half()
            page.wait.load_start()

            af_scroll_content = page.html
            self.save_page('htmls/af_scroll_content.html', af_scroll_content)
            self.save_page('cookies/af_scroll_content_cookie', str(page.cookies))
            # self.screen_shot(page, 'images/search/af_scroll_content_result.png')

            print('--------------------开始获取商品信息--------------------')
            self.catch_products(af_scroll_content)

            print('--------------------开始翻页--------------------')
            page.ele('xpath://a[@class="pn-next"]').click()
            page.wait.load_start()
            af_flip_content = page.html
            self.save_page('htmls/af_flip_content.html', af_flip_content)
            self.save_page('cookies/af_flip_content_cookie', str(page.cookies))
            self.screen_shot(page, 'images/search/af_flip_content_result.png')

            # curr_page = page.ele('xpath://span[@class="p-num"]//a[@class="curr"]').text
            # print(f'当前页：{curr_page}')

            print('--------------------开始获取商品信息--------------------')
            self.catch_products(af_scroll_content)

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
        products = selector.xpath('//div[@id="J_goodsList"]/ul[@class="gl-warp clearfix"]/li/div[@class="gl-i-wrap"]')

        try:
            if not products:
                raise Exception('检索页面异常，未发现商品')
            print('--------------------当前采集的商品数：{} --------------------'.format(len(products)))

            for product in products:
                p_img_obj = product.xpath('div[@class="p-img"]/a/img')[0].attrib
                p_img = 'https:' + (p_img_obj.get('src') or p_img_obj.get('data-lazy-img') or '')
                p_price = product.xpath('div[@class="p-price"]/strong/i')
                if p_price:
                    p_price = p_price[0].text
                p_name = product.xpath('div[@class="p-name p-name-type-2"]/a/em')
                if p_name:
                    p_name = p_name[0].xpath('string(.)')
                p_detail_addr = product.xpath('div[@class="p-name p-name-type-2"]/a')
                if p_detail_addr:
                    p_detail_addr = 'https:' + (p_detail_addr[0].attrib.get('href') or '')
                p_commit = product.xpath('div[@class="p-commit"]/strong/a')
                if p_commit:
                    p_commit = p_commit[0].xpath('string(.)')  # 评价
                p_shop_name = product.xpath('div[@class="p-shop"]/span/a')
                if p_shop_name:
                    p_shop_name = p_shop_name[0].xpath('string(.)')
                p_shop_addr = product.xpath('div[@class="p-shop"]/span/a')
                if p_shop_addr:
                    p_shop_addr = 'https' + (p_shop_addr[0].attrib.get('href') or '')
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
                with open(os.path.join(self.base_dir, "result.csv"), "a+", newline="", encoding='utf-8') as file:
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
            print('--------------------进入详情页完成--------------------')

            detail_content = page.html
            self.save_page('htmls/detail_content.html', detail_content)
            self.save_page('cookies/detail_content_cookie', str(page.cookies))

            title = page.ele('tag:title').text
            if self.check_is_captch_page(title):
                file_name = url.split('/')[-1].split('.')[0]
                self.screen_shot(page, 'images/search/{}.png'.format(file_name))
                raise Exception('出现验证页面')

            print('--------------------抓包数据--------------------')
            resp = page.wait.data_packets()
            if resp:
                resp_data = resp if isinstance(resp, dict) else resp.body
            else:
                resp_data = {}

            print('--------------------开始解析页面--------------------')
            selector = etree.HTML(detail_content)

            sku_name = selector.xpath('//div[@class="sku-name"]')
            if sku_name:
                sku_name = sku_name[0].text
            p_price = selector.xpath(
                '//div[@class="summary-price-wrap"]/div[@class="summary-price J-summary-price"]/div[@class="dd"]/span[@class="p-price"]/span'
            )
            if p_price:
                p_price = p_price[1].text if len(p_price) > 1 else p_price[0].text
            summary_quan = selector.xpath(
                '//div[@class="summary summary-first"]/div[@class="summary-price-wrap"]/div[@id="summary-quan"]')
            if summary_quan:
                summary_quan = summary_quan[0].xpath('string(.)')
            J_summary_top = selector.xpath(
                '//div[@class="summary summary-first"]/div[@class="summary-price-wrap"]/div[@id="J-summary-top"]')
            if J_summary_top:
                J_summary_top = J_summary_top[0].xpath('string(.)')
            summary_stock = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@class="summary-stock"]')
            if summary_stock:
                summary_stock = summary_stock[0].xpath('string(.)')
            SelfAssuredPurchase_li = selector.xpath(
                '//div[@class="summary p-choose-wrap"]/div[@class="SelfAssuredPurchase li"]')
            if SelfAssuredPurchase_li:
                SelfAssuredPurchase_li = SelfAssuredPurchase_li[0].xpath('string(.)')
            summary_supply = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="summary-supply"]')
            if summary_supply:
                summary_supply = summary_supply[0].xpath('string(.)')
            summary_weight = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="summary-weight"]')
            if summary_weight:
                summary_weight = summary_weight[0].xpath('string(.)')
            choose_attrs = selector.xpath('//div[@class="summary p-choose-wrap"]/div[@id="choose-attrs"]')
            if choose_attrs:
                choose_attrs = choose_attrs[0].xpath('string(.)')

            parameter_brand = selector.xpath('//div[@class="p-parameter"]/ul[@id="parameter-brand"]/li')
            if parameter_brand:
                parameter_brand = parameter_brand[0].xpath('string(.)')
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

    def screen_shot(self, page, file_name='images/screen_shot.png', **screen_kwargs):
        full_path = os.path.join(self.base_dir, file_name)
        page.get_screenshot(path=full_path, **screen_kwargs)
        return full_path

    def end(self):
        self.init_page.quit()

    def test(self):
        url = "https://item.jd.com/100018280931.html"
        tab_id = self.init_page.new_tab()
        page = self.init_page.get_tab(tab_id)

        page.wait.set_targets('color.yiyaojd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc')
        page.get(url)
        page.wait.load_start()
        resp_data = page.wait.data_packets()
        print(resp_data)

    def business_info(self, url):

        tab_id = self.init_page.new_tab(url)  # 会导致截图、或者获取html内容只能拿到默认打开的无效标签页
        page = self.init_page.get_tab(tab_id)
        page.wait.load_start()
        print('--------------------进入页面: {} --------------------'.format(tab_id))

        try:
            bf_captch_cnt = page.html
            self.save_page('htmls/bf_captch_cnt.html', bf_captch_cnt)
            self.save_page('cookies/bf_captch_cnt_cookie', str(page.cookies))
            print('--------------------验证之前--------------------')

            captch_img = page.ele('xpath://img[@id="verifyCodeImg"]')
            loc = captch_img.location
            right_bottom = (loc[0] + 80, loc[1] + 30)

            screen_kwargs = {'left_top': loc, 'right_bottom': right_bottom, 'full_page': False}
            print('参数：{}'.format(screen_kwargs))
            path = self.screen_shot(page, 'images/verify_code/verify_img.png', **screen_kwargs)
            word = self.captcha_handler_by_file(path)
            page.ele('#verifyCode').input(word)
            self.screen_shot(page, 'images/verify_code/input_screen_shot.png')
            page.ele('xpath://button[@class="btn"]').click()
            page.wait.load_start()
            print('--------------------输入验证之后--------------------')
            self.screen_shot(page, 'images/verify_code/af_verify.png')

        except Exception as e:
            print('操作页面失败，错误：{}'.format(e))

        finally:
            self.init_page.close_tabs(tab_id)  # 关闭当前页面
            print('--------------------end--------------------')

    def img_pre_handler(self, path):
        """图片预处理"""

        img = cv2.imread(path)  # 读取图片

        Grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图片

        ret, thresh = cv2.threshold(Grayimg, 150, 255, cv2.THRESH_BINARY)  # 二值化图片，颜色阈值为 0~255

        cv2.imwrite(path, thresh)  # 保存图片

    def extract_word_ddddocr(self, path):
        """使用ddddocr提取图片中的文字"""

        ocr = ddddocr.DdddOcr(old=True)

        with open(path, 'rb') as f:
            image = f.read()

        result = ocr.classification(image)

        return result

    def captcha_handler_by_file(self, path):
        self.img_pre_handler(path)

        word = self.extract_word_ddddocr(path)

        print('识别 {} 验证码：{}'.format(path, ord))

        return word


if __name__ == '__main__':
    login_url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
    search_url = "https://www.jd.com/"
    captch_url = "https://mall.jd.com/showLicence-119174.html"
    crawl = JDCrawler()
    crawl.business_info(captch_url)
    # crawl.auto_login(login_url)
    # crawl.search(search_url, '盐酸氨基葡萄糖')

    # test_file_path = os.path.join(crawl.base_dir, 'htmls/af_search.html')
    # cnt = crawl.read_page(test_file_path)
    # crawl.catch_products(cnt)

    # crawl.test()
