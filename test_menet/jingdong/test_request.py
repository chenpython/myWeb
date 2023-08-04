import requests

url = "https://search.jd.com/Search?keyword=%E7%9B%90%E9%85%B8%E6%B0%A8%E5%9F%BA%E8%91%A1%E8%90%84%E7%B3%96&enc=utf-8&wq=%E7%9B%90%E9%85%B8%E6%B0%A8%E5%9F%BA%E8%91%A1%E8%90%84%E7%B3%96"
headers = {
    # "Host": "search.jd.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.jd.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
# params = {"keyword": "盐酸氨基葡萄糖", "enc": "utf-8", "wq": "盐酸氨基葡萄糖"}

# response = requests.get(url, headers=headers, params=params)
response = requests.get(url, headers=headers)

print(response.text)
print(response.status_code)
