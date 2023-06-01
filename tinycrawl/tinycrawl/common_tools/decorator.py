import asyncio
import random
import time

from . import log


def retry_decorator(func):

    async def wrapper(*args, **kwargs):
        retry_times = 5
        result = {}

        while retry_times:
            try:

                result = await func(*args, **kwargs)
            except Exception as e:
                retry_times -= 1
                await asyncio.sleep(random.randint(1, 3))
                continue
            else:
                return result

        return result

    return wrapper


def retry_decorator_custom_sync(retry_times=5, need_sleep=True, sleep_random=[1, 3], err_result='', err_log_cnt=''):

    def decorator(func):

        def wrapper(*args, **kwargs):

            pre_retry_times = local_retry_times = retry_times

            result = err_result
            err = [' ---unknow--- ']

            while local_retry_times:
                try:

                    result = func(*args, **kwargs)
                except Exception as e:
                    err.append(str(e))
                    local_retry_times -= 1

                    if need_sleep:
                        time.sleep(random.randint(*sleep_random))
                    continue
                else:
                    return result
            if err_log_cnt:
                log.error(err_log_cnt.format(err=err[-1], retry_times=pre_retry_times, *args[1:]))
            return result

        return wrapper

    return decorator


def retry_decorator_custom(retry_times=5, need_sleep=True, sleep_random=[1, 3], err_result='', err_log_cnt=''):

    def decorator(func):

        async def wrapper(*args, **kwargs):

            pre_retry_times = local_retry_times = retry_times

            result = err_result
            err = ' ---unknow--- '

            while local_retry_times:
                try:

                    result = await func(*args, **kwargs)
                except Exception as e:
                    err = str(e)
                    local_retry_times -= 1

                    if need_sleep:
                        await asyncio.sleep(random.randint(*sleep_random))
                    continue
                else:
                    return result

            if err_log_cnt:
                log.error(err_log_cnt.format(err=err, retry_times=pre_retry_times, *args[1:]))
            return result

        return wrapper

    return decorator
