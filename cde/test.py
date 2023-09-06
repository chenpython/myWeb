import urllib

import requests


def getCookie(html_text, url_path):
    print('开始生成cookie')

    cookie_resp = requests.post('http://127.0.0.1:2229' + url_path, data={
        'html_text': html_text
    }, timeout=None)

    return cookie_resp.text

def home() -> None:
    print('开始请求菜单页')
    headers = {
        'Host': 'www.chinadrugtrials.org.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://www.chinadrugtrials.org.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer':
        'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml'

    resp = requests.get(url, headers=headers, timeout=20)
    print(resp.status_code)
    cookies_s = resp.cookies.get_dict()
    # cookies_s = {"FSSBBIl1UgzbN7N80S": "gI1.KOo4TP2YYLVgW693Bk9Cb89SOFAt3N8Vfdt4xeui.HSGykI7JDXr9Cqlp79w"}
    print(cookies_s)

    with open("/home/feng/workspace/myWeb/cde/home_html", "wb") as f:
        f.write(resp.content)
    cookie_t_str = getCookie(resp.text, '/v2/cde_home_cookie')
    # with open("/home/feng/workspace/myWeb/cde/首页返回.html", "w") as f:
    #     f.write(resp.text)

    # with open("/home/feng/workspace/myWeb/cde/cookie", "r") as f:
    #     cookie_t_str = f.read()

    cookies_t = {cookie_t_str.split('=')[0]: cookie_t_str.split("=")[1].split(';')[0]}
    cookies = {**cookies_s, **cookies_t}
    print(cookies)

    resp1 = requests.get(url, headers=headers, cookies=cookies, timeout=20)
    print(resp1.status_code)
    with open("/home/feng/workspace/myWeb/cde/success_home.html", "wb") as f:
        f.write(resp1.content)

    print('开始请求详情页')
    # with open("/home/feng/workspace/myWeb/cde/detail_html", "wb") as f:
    #     f.write(resp.content)
    cookie_t_str = getCookie(resp1.text,'/v2/cde_detail_cookie')
    # with open("/home/feng/workspace/myWeb/gansu_samr/detail_cookie", "r") as f:
    #     cookie_t_str = f.read()
    cookies_t = {cookie_t_str.split('=')[0]: cookie_t_str.split("=")[1].split(';')[0]}
    cookies = {**cookies_s, **cookies_t}

    detail_common_args = '&sort=desc&sort2=&rule=CTR&secondLevel=0&currentpage=1&keywords=&reg_no=&indication=&case_no=&drugs_name=&drugs_type=&appliers=&communities=&researchers=&agencies=&state='
    detail_args = {
        'id': '1967ac1f28cc42da9fd5c8e4366f92ac',
        'ckm_index': '1',
    }
    payload = urllib.parse.urlencode(
        detail_args) + detail_common_args

    url = "http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml"

    resp = requests.post(url, headers=headers,params=payload, timeout=20, cookies=cookies)
    print(resp.status_code)
    with open("/home/feng/workspace/myWeb/cde/success_detail.html", "wb") as f:
        f.write(resp1.content)

    print('程序结束')


def detail():
    print('开始请求详情页')
    headers = {
        'Host': 'www.chinadrugtrials.org.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://www.chinadrugtrials.org.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer':
        'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    detail_common_args = '&sort=desc&sort2=&rule=CTR&secondLevel=0&currentpage=1&keywords=&reg_no=&indication=&case_no=&drugs_name=&drugs_type=&appliers=&communities=&researchers=&agencies=&state='
    detail_args = {
        'id': '1967ac1f28cc42da9fd5c8e4366f92ac',
        'ckm_index': '1',
    }
    payload = urllib.parse.urlencode(
        detail_args) + detail_common_args

    url = "http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml"

    resp = requests.post(url, headers=headers, params=payload, timeout=20)
    print(resp.status_code)
    cookies_s = resp.cookies.get_dict()
    print(cookies_s)

    with open("/home/feng/workspace/myWeb/cde/detail_html", "wb") as f:
        f.write(resp.content)
    cookie_t_str = getCookie(resp.text)
    # with open("/home/feng/workspace/myWeb/gansu_samr/详情页返回.html", "w") as f:
    #     f.write(resp.text)
    # with open("/home/feng/workspace/myWeb/gansu_samr/detail_cookie", "r") as f:
    #     cookie_t_str = f.read()
    cookies_t = {cookie_t_str.split('=')[0]: cookie_t_str.split("=")[1].split(';')[0]}
    cookies = {**cookies_s, **cookies_t}
    print(cookies)

    resp1 = requests.post(url, headers=headers, params=payload,cookies=cookies, timeout=20)
    print(resp1.status_code)
    with open("/home/feng/workspace/myWeb/cde/success_detail.html", "wb") as f:
        f.write(resp1.content)
    print('程序结束')

if __name__ == "__main__":
    # detail()
    home()
    # for x in range(10):
    #     print(f'第{x}次尝试')
    #     home()
