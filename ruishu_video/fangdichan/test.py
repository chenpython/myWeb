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
# cookies_s = {"FSSBBIl1UgzbN7N80S": "wYpkeL5ayG8UNsMNXjg9CXB5QnAORh1dUsR6QvH6IGcSCqGDy3k6cvt.9d235mq6"}
print(cookies_s)
with open("/home/feng/workspace/myWeb/ruishu_video/fangdichan/home_html", "w") as f:
    f.write(resp.text)
with open("/home/feng/workspace/myWeb/ruishu_video/fangdichan/首页返回.html", "w") as f:
    f.write(resp.text)
cookies_t = {
    "FSSBBIl1UgzbN7N80T":
    "4LD1xn9bZe1aBFh19HU8FstIV3BqIWpB4RDTPWX9e0ut6rB8553AOSSVIToGeDkZ5UVuIvdVS9lXLHrn4vxF3L.mqOVWb8BNFWQSHQoyaPqOi88ej74E5kkCpkLWhJ1MN9Y.FUwr3BY3M9CJkRgCMyCOWgff3T6uAwkh8SayqTu5zCwfQS7GpBJvl4GgnaoH9JPW15VnT6EQ2En8TubIN7dFc24O0nWDq90xa4l_iLqyOFdpMpe1rzvAvrEv3dIk2cJfSVsgHX0.ghP86iShp4rx0qTSgY4EkuKctSarwAmTM8.zqP_t20ly4ICtGSEmBAe3"
}

cookies = {**cookies_t, **cookies_s}

resp1 = requests.get(url, headers=headers, cookies=cookies)
print(resp1.status_code)
