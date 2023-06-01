# Scrapy settings for tinycrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = "tinycrawl"

SPIDER_MODULES = ["tinycrawl.spiders"]
NEWSPIDER_MODULE = "tinycrawl.spiders"

# ====================== scrapy-redis settings ========================

# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 指定去重方法
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 指定scheduler队列
# SCHEDULER_PERSIST = True  # 队列中内容是否持久保存，为False的时候会在关闭redis的时候清空redis
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 400, # scrapy_redis实现的items保存到redis的pipeline
# }
# REDIS_URL = 'redis://:szkj@20221009@192.168.5.201:6379'  # 指定redis的地址

# ====================== scrapy-redis settings ========================

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "tinycrawl (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "tinycrawl.middlewares.TinycrawlSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "tinycrawl.middlewares.TinycrawlDownloaderMiddleware": 543,
    'tinycrawl.middlewares.TinyCrawlHttpProxyMiddleware': 545
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "tinycrawl.pipelines.TinycrawlPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DEFAULT_PROXY_NUMS_PER_BATCH = 3
MONGO_BACKEND_URL = os.environ.get("MONGO_BACKEND_URL", "mongodb://rdpsMongo:menetrdpsMongo@5@192.168.5.201")

REDIS_BACKEND_URL = os.environ.get('REDIS_BACKEND_URL', 'redis://default:SZkj&pcbs@3986@192.168.20.13:6379/0')

REDIS_HOST = os.environ.get('REDIS_HOST', '192.168.5.201')
REDIS_PORT = os.environ.get("REDIS_PORT", '6379')
REDIS_PSWD = os.environ.get('REDIS_PSWD', 'szkj@20221009')
REDIS_DB = os.environ.get("REDIS_DB", 4)

JG_PROXY_IP_URL = 'http://d.jghttp.alicloudecs.com/getip'
JG_PROXY_BALANCE_URL = 'https://webapi.jghttp.alicloudecs.com/index/index/get_my_balance'
JG_PROXY_SAVE_WHITE = 'https://webapi.jghttp.alicloudecs.com/index/index/save_white'
JG_PROXY_NEEK = '50804'
JG_PROXY_APPKEY = 'e887b568fd33a2d09cd3591432001720'

FILE_LOG = True
LOG_PATH = './logs'

CHROME_PATH = '/usr/bin/google-chrome-stable'
DOWNLOAD_PATH_TMP = '/home/feng/tmp'