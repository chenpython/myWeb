import requests


def getCookie(html_text):

    cookie_resp = requests.post('http://127.0.0.1:2229/hubei_home_cookie', data={
        'html_text': html_text
    }, timeout=15)
    cookies_t = {cookie_resp.text.split("=")[0]: cookie_resp.text.split("=")[1].split(';')[0]}
    
    return cookies_t

def home() -> None:
    headers = {
        "Host": "scjg.hubei.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://scjg.hubei.gov.cn/zfxxgk/zcwj/qtwj/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    url = "http://scjg.hubei.gov.cn/zfxxgk/zcwj/qtwj/"

    resp = requests.get(url, headers=headers, timeout=20)
    print(resp.status_code)
    cookies_t = getCookie(resp.text)

    cookies = cookies_t
    print(cookies)
    data_url = "http://scjg.hubei.gov.cn/zfxxgk/zcwj/qtwj/zcwj.json"
    resp1 = requests.get(data_url, headers=headers, cookies=cookies, timeout=20)
    print(resp1.status_code)
    with open("/home/feng/workspace/myWeb/hubei_samr/success_home.html", "wb") as f:
        f.write(resp1.content)

    detail_url = "http://scjg.hubei.gov.cn/zfxxgk/zcwj/qtwj/202308/t20230828_4813376.shtml"
    resp2 = requests.get(detail_url, headers=headers, cookies=cookies, timeout=20)
    print(resp2.status_code)
    with open("/home/feng/workspace/myWeb/hubei_samr/success_detail.html", "wb") as f:
        f.write(resp2.content)

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
