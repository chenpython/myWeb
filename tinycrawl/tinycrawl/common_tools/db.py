import pymongo
import redis

from . import scrapy_settings, tools


def get_redis_client():

    # conn_str = tools.transform_password(scrapy_settings.REDIS_BACKEND_URL)

    # pool = redis.BlockingConnectionPool.from_url(conn_str,
    #                                              max_connections=40,
    #                                              timeout=5)

    pool = redis.BlockingConnectionPool(host=scrapy_settings.REDIS_HOST,
                                        password=scrapy_settings.REDIS_PSWD,
                                        port=int(scrapy_settings.REDIS_PORT),
                                        db=int(scrapy_settings.REDIS_DB),
                                        max_connections=40,
                                        timeout=5)

    client = redis.Redis(connection_pool=pool, decode_responses=True)

    return client


def get_mongo_client():
    conn_str = tools.transform_password(scrapy_settings.MONGO_BACKEND_URL)
    db_name = scrapy_settings.MONGODB_DB_NAME

    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

    db = client[db_name]

    return db


redis_client = get_redis_client()
# mongo_client = get_mongo_client()
