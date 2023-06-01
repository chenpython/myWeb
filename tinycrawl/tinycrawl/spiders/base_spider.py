from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider


class RedisCustomBaseSpider(RedisSpider):

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 20,
        'DOWNLOAD_DELAY': 0.2,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_FAIL_ON_DATALOSS': False,  # 数据完整性
        'RANDOMIZE_DOWNLOAD_DELAY': True  # 请求延迟
    }


class CustomBaseSpider(Spider):

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 20,
        'DOWNLOAD_DELAY': 0.2,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_FAIL_ON_DATALOSS': False,  # 数据完整性
        'RANDOMIZE_DOWNLOAD_DELAY': True  # 请求延迟
    }