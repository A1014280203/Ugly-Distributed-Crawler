from requests.api import request
from requests.exceptions import ProxyError
import redis
from .config import headers, settings, r_server


def make_redis_handler():
    pool = redis.ConnectionPool(host=r_server['ip'], port=r_server['port'],
                                password=r_server['passwd'])
    return redis.Redis(connection_pool=pool)


def make_proxy_handler():
    return make_redis_handler()


def get_proxy():
    phandler = make_proxy_handler()
    return phandler.srandmember('proxy_ip', 1)[0].decode()


def pop_url():
    uhandler = make_redis_handler()
    return uhandler.spop('url').decode()


def get_url(url):
    headers['Referer'] = url
    count = 0
    while True:
        count += 1
        if count < settings['maxtries']:
            proxy = get_proxy()
        else:
            proxy = None
        try:
            resp = request('get', url, headers=headers, proxies={'http': proxy})
            return resp
        except ProxyError:
            if count > settings['maxtries']+2:
                print('Exit: Could not get url.<@get_url>')
                exit(1)
            continue

if __name__ == '__main__':
    get_url('http://bbs.kaoyan.com')