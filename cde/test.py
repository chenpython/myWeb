import requests


def getCookie(html_text):
    print('开始生成cookie')

    cookie_resp = requests.post('http://127.0.0.1:2229/cde_home_cookie', data={
        'html_text': html_text
    }, timeout=None)

    return cookie_resp.text

def home() -> None:
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
    cookie_t_str = getCookie(resp.text)
    # with open("/home/feng/workspace/myWeb/cde/home_html", "wb") as f:
    #     f.write(resp.content)
    # with open("/home/feng/workspace/myWeb/cde/首页返回.html", "w") as f:
    #     f.write(resp.text)

    # with open("/home/feng/workspace/myWeb/cde/cookie", "r") as f:
    #     cookie_t_str = f.read()

    cookies_t = {cookie_t_str.split('=')[0]: cookie_t_str.split("=")[1].split(';')[0]}
    cookies = {**cookies_t, **cookies_s}
    print(cookies)

    resp1 = requests.get(url, headers=headers, cookies=cookies, timeout=20)
    print(resp1.status_code)
    with open("/home/feng/workspace/myWeb/cde/success_home.html", "wb") as f:
        f.write(resp1.content)
    print('程序结束')


def detail():
    headers = {
        "Host": "scjg.gansu.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    url = "http://scjg.gansu.gov.cn/scjg/c110159/202205/2032457.shtml"

    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    cookies_s = resp.cookies.get_dict()
    # cookies_s = {"FSSBBIl1UgzbN7N80S": "gI1.KOo4TP2YYLVgW693Bk9Cb89SOFAt3N8Vfdt4xeui.HSGykI7JDXr9Cqlp79w"}
    print(cookies_s)
    cookie_t_str = getCookie(resp.text)

    # with open("/home/feng/workspace/myWeb/gansu_samr/detail_html", "wb") as f:
    #     f.write(resp.content)
    # with open("/home/feng/workspace/myWeb/gansu_samr/详情页返回.html", "w") as f:
    #     f.write(resp.text)
    # cookies_t = {
    #     "FSSBBIl1UgzbN7N80T":
    #     "4MORQ75Y0R20IN2xbOEoDLaJgTO.l1v4yV8DQdF0w3214m3M4UCa9FJKZ63amG.xdLQPdCKUh2K.LcCbuHq8eLJ4a24POHZmkgRzOPbfj8pdwz_Ub3j_tB7VhvbpbMQdXkXmSvV1X8_BI9F46Q0RGsjgjWNjTDIJtrbY_1hIAvCDAz9vIKhB3rMPLbLpvQ8GstpxJsCfEAMgOXpuuSn.84Q3A"
    # }
    # with open("/home/feng/workspace/myWeb/gansu_samr/detail_cookie", "r") as f:
    #     cookie_t_str = f.read()
    cookies_t = {"4hP44ZykCTt5T": cookie_t_str}
    cookies = {**cookies_t, **cookies_s}

    resp1 = requests.get(url, headers=headers, cookies=cookies)
    print(resp1.status_code)
    with open("/home/feng/workspace/myWeb/gansu_samr/success_detail.html", "wb") as f:
        f.write(resp1.content)
    print('程序结束')

if __name__ == "__main__":
    # detail()
    home()
    # for x in range(10):
    #     print(f'第{x}次尝试')
    #     home()
