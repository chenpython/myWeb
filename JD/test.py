import requests

url = "https://api.m.jd.com/"
headers = {
    "Host": "api.m.jd.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "accept": "*/*",
    "x-referer-page": "https://search.jd.com/Search",
    "x-rp-client": "h5_1.0.0",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "https://search.jd.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://search.jd.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
# params = {
#     'appid': 'search-pc-java',
#     'functionId': 'pc_search_s_new',
#     'client': 'pc',
#     'clientVersion': '1.0.0',
#     't': '1697425766970',
#     'body': '{"keyword":"盐酸氨基葡萄糖","pvid":"29b29c69e98742d6957e0c9b231a9eec","isList":0,"page":"3","s":"57","click":"0","log_id":"1697421976026.3232","show_items":""}',
#     'loginType': '3',
#     'uuid': '122270672.16974209225882065326461.1697420923.1697420923.1697420923.1',
#     'area': '19_1601_0_0',
#     'h5st': '20231016110927006;ngn53ti96znzgnj5;f06cc;tk03wcd161d2018nzHhPdTNRDZGEriP4VBmKFe_Ylyxu3zCudAvyKcn0GyQQ8IkdPrqfVHvH6eMrK-aM0Aby8kivOsQb;011a970d1a43edb70e115e61e6b54b22;4.1;1697425767006;ee3cf7f6b94dc20e9265d83066bb9ceece4bb89e2b7e8bf5afb1bfd928788174bfa06c210ddd4437d8a2e234330c3a397ae8268c7f7c5fb3780158b8fa4e73d08336abe4b79d34906258dbb79cecd4769b752da1b84c54d1a95071351c73c853facadf62b978ecd13b1a6133cc8a4f632965b1dc24a78d93c75b5552c8a341a09a0662c4eb6974e0cad76d47a49883bfb54b5165533d8628b88d6a530be05fcd35557f1b56197906752bc35bb4cf0331cfeb6b1faddc1b9068e843aa512cc83ed7f4f9077fb5f4cd60cda4af881113e77ee65494baf65a2dc05bd7d5d1d5e15efcdf5bf85baa23d6edb57cebff939aa42189ce08d78ade0d9bad50d2ebb832b33e2b53dfb6d9229c9cec6fbfedbf701ef8e96641432d5253200451e3a0d20356',
#     'x-api-eid-token': 'jdd037M5AVFZ2HT2SA5SZC7BICJSWBJG7U4KSIYNBOHHIL7EBR7WW63CSB3P6KRACYGZ553JLWA3Q5CN3FDSAJLW5OU2HOUAAAAMLGY5ZGSIAAAAACZ5R3FCSBPMHE4X'
# }

params = {
    'appid': 'search-pc-java',
    'functionId': 'pc_search_s_new',
    'client': 'pc',
    'clientVersion': '1.0.0',
    't': '1697425766970',
    'body': '{"keyword":"盐酸氨基葡萄糖","pvid":"29b29c69e98742d6957e0c9b231a9eec","isList":0,"page":"3","s":"57","click":"0","log_id":"1697421976026.3232","show_items":""}',
    'loginType': '3',
    'uuid': '122270672.16974209225882065326461.1697420923.1697420923.1697420923.1',
    'area': '19_1601_0_0',
    'h5st': '20231016110927006;ngn53ti96znzgnj5;f06cc;tk03wcd161d2018nzHhPdTNRDZGEriP4VBmKFe_Ylyxu3zCudAvyKcn0GyQQ8IkdPrqfVHvH6eMrK-aM0Aby8kivOsQb;011a970d1a43edb70e115e61e6b54b22;4.1;1697425767006;ee3cf7f6b94dc20e9265d83066bb9ceece4bb89e2b7e8bf5afb1bfd928788174bfa06c210ddd4437d8a2e234330c3a397ae8268c7f7c5fb3780158b8fa4e73d08336abe4b79d34906258dbb79cecd4769b752da1b84c54d1a95071351c73c853facadf62b978ecd13b1a6133cc8a4f632965b1dc24a78d93c75b5552c8a341a09a0662c4eb6974e0cad76d47a49883bfb54b5165533d8628b88d6a530be05fcd35557f1b56197906752bc35bb4cf0331cfeb6b1faddc1b9068e843aa512cc83ed7f4f9077fb5f4cd60cda4af881113e77ee65494baf65a2dc05bd7d5d1d5e15efcdf5bf85baa23d6edb57cebff939aa42189ce08d78ade0d9bad50d2ebb832b33e2b53dfb6d9229c9cec6fbfedbf701ef8e96641432d5253200451e3a0d20356',
    'x-api-eid-token': 'jdd037M5AVFZ2HT2SA5SZC7BICJSWBJG7U4KSIYNBOHHIL7EBR7WW63CSB3P6KRACYGZ553JLWA3Q5CN3FDSAJLW5OU2HOUAAAAMLGY5ZGSIAAAAACZ5R3FCSBPMHE4X'
}

response = requests.get(url=url, headers=headers, params=params, timeout=30)


print(response.status_code)

