import requests

headers = {
    "Host": "www.fangdi.com.cn",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

url = "http://www.fangdi.com.cn/new_house/new_house.html"

resp = requests.get(url, headers=headers)
print(resp.status_code)
cookies_s = resp.cookies.get_dict()
# cookies_s = {"FSSBBIl1UgzbN7N80S": "gI1.KOo4TP2YYLVgW693Bk9Cb89SOFAt3N8Vfdt4xeui.HSGykI7JDXr9Cqlp79w"}
print(cookies_s)
with open("/home/feng/workspace/myWeb/ruishu_video/fangdichan/home_html", "wb") as f:
    f.write(resp.content)
# with open("/home/feng/workspace/myWeb/ruishu_video/fangdichan/首页返回.html", "w") as f:
#     f.write(resp.text)
# cookies_t = {
#     "FSSBBIl1UgzbN7N80T":
#     "4MORQ75Y0R20IN2xbOEoDLaJgTO.l1v4yV8DQdF0w3214m3M4UCa9FJKZ63amG.xdLQPdCKUh2K.LcCbuHq8eLJ4a24POHZmkgRzOPbfj8pdwz_Ub3j_tB7VhvbpbMQdXkXmSvV1X8_BI9F46Q0RGsjgjWNjTDIJtrbY_1hIAvCDAz9vIKhB3rMPLbLpvQ8GstpxJsCfEAMgOXpuuSn.84Q3A"
# }
with open("/home/feng/workspace/myWeb/ruishu_video/fangdichan/cookie", "r") as f:
    cookie_t_str = f.read()
cookies_t = {"FSSBBIl1UgzbN7N80T": cookie_t_str}
cookies = {**cookies_t, **cookies_s}

resp1 = requests.get(url, headers=headers, cookies=cookies)
print(resp1.status_code)
