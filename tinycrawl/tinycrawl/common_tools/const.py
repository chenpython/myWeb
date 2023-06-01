REDIS_IP_POOL_KEY = 'JG_PROXY_POOL'
REDIS_IP_MAP = 'REDIS_IP_MAP'

REDIS_IP_POOL_KEY_EXPIRED_TIME = 60 * 5  # time1 参数获取的 ip 有效时长在 1 - 5 分钟

UPDATE_IP_POOL_FLAG = 'UPDATING_IP_POOL'

UPDATE_IP_POOL_FLAG_VALUE = 'be updating'

INVALID_PROXY_COLUMN = 'valid_proxy'

REDIS_ITEM_KEY = 'SPIDER_ITEMS'

VALID_FILE_SUFFIX = ('pdf', 'xlsx', 'xls', 'doc', 'docx', 'csv', 'rar', 'wps',
                     'zip', 'mp4', 'accdb', 'pptx', 'txt', 'avi', 'rm', 'iso',
                     'exe', 'tmp', 'mdf', 'ppt', 'mid', 'hlp', 'arj', 'gz',
                     'z', 'wav', 'aif', 'mp3', 'au', 'ram', 'wma', 'mmf',
                     'amr', 'aac', 'flac', 'mpg', 'mov', 'swf')

VALID_WEB_PAGE_SUFFIX = ('html', 'htm', 'jsp', 'php', 'asp', 'phtml', 'shtml',
                         'nsp', 'cgi', 'aspx', 'com')

VALID_IMAGE_SUFFIX = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'ai', 'cdr',
                      'eps', 'pic', 'tif')

DEFAULT_RETRY_TIMES = 3
DEFAULT_UPLOAD_RETRY_TIMES = 1

RUNNING_UPLOAD_SERVER_FLAG = 'RUNNING_UPLOAD_SERVER_FLAG'

DEFAULT_UPLOAD_BATCH_SIZE = 5000
UPLOAD_SLICE = 100

HMA_URL_BATCH = 'HMA_URL_BATCH'

DEFAULT_WHO_DETAIL_BATCH_SIZE = 20

# 下载文件要生成cookie的website_name
cookie_website_names = ['国家药监局审评中心']

RESUMABLE_DOWNLOAD_CHUNK_SIZE = 1024 * 1024 * 3
DOWNLOAD_FILE_SIZE_LIMIT = 1024 * 1024 * 1000

DOWNLAOD_CONCURRENCY = 30  # 考虑代理限制

DOWNLOAD_FILE_EXPIRE_TIME = 3 * 60
UPLOAD_FILE_EXPIRE_TIME = 3 * 60
