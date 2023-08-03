import requests

url = 'http://yp.hnggzyjy.cn/HomePage/TitleList.aspx?index=1'

headers = {
    'Origin': 'http://yp.hnggzyjy.cn',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://yp.hnggzyjy.cn/HomePage/TitleList.aspx?index=1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

data = {
    '__EVENTTARGET': 'ddlNoteStatus',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE':
    '/wEPDwUKMTk1MjM0MDE2OA9kFgICAQ9kFgYCAg8PFgIeBFRleHQFDOmAmuefpeWFrOWRimRkAgMPEGRkFgECAWQCBg9kFgICAQ8PFgQfAAXBBjxkaXYgYWxpZ249cmlnaHQ+PC9kaXY+PGZvbnQgY29sb3I9JyNDMEMwQzAnPuS4iuS4gOmhtTwvZm9udD4gPGEgaHJlZj0iamF2YXNjcmlwdDpEYlBhZ2VGbGlwKDIpIj7kuIvkuIDpobU8L2E+IO+8u+W9k+WJjeesrCAxIOmhteOAgOWFsSAyOCDpobXjgIDorqEgNDE1IOadoe+8vSDovazliLDnrKw8c2VsZWN0IG9uY2hhbmdlPSJqYXZhc2NyaXB0OkRiUGFnZUZsaXAodGhpcy5zZWxlY3RlZEluZGV4KzEpIj48b3B0aW9uIHNlbGVjdGVkPjE8L29wdGlvbj48b3B0aW9uPjI8L29wdGlvbj48b3B0aW9uPjM8L29wdGlvbj48b3B0aW9uPjQ8L29wdGlvbj48b3B0aW9uPjU8L29wdGlvbj48b3B0aW9uPjY8L29wdGlvbj48b3B0aW9uPjc8L29wdGlvbj48b3B0aW9uPjg8L29wdGlvbj48b3B0aW9uPjk8L29wdGlvbj48b3B0aW9uPjEwPC9vcHRpb24+PG9wdGlvbj4xMTwvb3B0aW9uPjxvcHRpb24+MTI8L29wdGlvbj48b3B0aW9uPjEzPC9vcHRpb24+PG9wdGlvbj4xNDwvb3B0aW9uPjxvcHRpb24+MTU8L29wdGlvbj48b3B0aW9uPjE2PC9vcHRpb24+PG9wdGlvbj4xNzwvb3B0aW9uPjxvcHRpb24+MTg8L29wdGlvbj48b3B0aW9uPjE5PC9vcHRpb24+PG9wdGlvbj4yMDwvb3B0aW9uPjxvcHRpb24+MjE8L29wdGlvbj48b3B0aW9uPjIyPC9vcHRpb24+PG9wdGlvbj4yMzwvb3B0aW9uPjxvcHRpb24+MjQ8L29wdGlvbj48b3B0aW9uPjI1PC9vcHRpb24+PG9wdGlvbj4yNjwvb3B0aW9uPjxvcHRpb24+Mjc8L29wdGlvbj48b3B0aW9uPjI4PC9vcHRpb24+PC9zZWxlY3Q+6aG1PGlucHV0IHR5cGU9J2hpZGRlbicgbmFtZT0nQ3VycmVudGx5UGFnZUluZGV4JyB2YWx1ZT0nMSc+HgdFbmFibGVkZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQlidG5TZWFyY2gLvfGIOacMk8UCQdf/wY8MoFBiJQ==',
    '__VIEWSTATEGENERATOR': '8DF45F70',
    '__EVENTVALIDATION':
    '/wEWBwL6urqfAQLrtcqSBAKj+IH5BwL72uD8CALk2uD8CAKoqY+/BwKln/PuCjJ8vsIrG2msE5aHs9sI3CbJ7oOl',
    'ddlNoteStatus': '1',
    'txtTital': '',
    'CurrentlyPageIndex': '1'
}

resp = requests.post(url=url, headers=headers, data=data)

print(resp.status_code)

import requests

headers = response.request.headers.to_unicode_dict()
url = response.url
payload = response.request.body.decode()

resp = requests.post(url, headers=headers, data=payload)
resp = requests.get(url, headers=headers)
{
    'host': 'yycg.hnsggzy.com',
    'content-length': '350',
    'connection': 'keep-alive',
    'cache-control': 'max-age=0',
    'sec-ch-ua':
    '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'origin': 'https://yycg.hnsggzy.com',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36Edg/107.0.1418.62',
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://yycg.hnsggzy.com/HomePage/MessageNews.aspx',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.',
    'cookie': 'ASP.NET_SessionId=pi5xxcvajcfown45knznar45'
}
