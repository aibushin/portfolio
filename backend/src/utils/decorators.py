from functools import wraps
import logging
from time import time, monotonic


import asyncio
import functools
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.debug("func:%r args:[%r, %r] took: %2.4f sec" % (f.__name__, args, kw, te - ts))
        return result

    return wrap


def duration(func):
    @contextmanager
    def wrapping_logic():
        start_ts = monotonic()
        yield
        dur = monotonic() - start_ts
        logger.debug("{} took {:.2} seconds".format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:

            async def tmp():
                with wrapping_logic():
                    return await func(*args, **kwargs)

            return tmp()

    return wrapper
