from pyquery import PyQuery
import requests
from requests.exceptions import ProxyError
import redis
from threading import Thread
from config import r_server


class ProxyDemo(object):

    def __init__(self):
        print("begin")
        print('create instance start')
        self.query_address = 'http://www.ip.cn/'
        self.proxy_address = ['http://www.xicidaili.com/nn/', 'http://www.xicidaili.com/nt/']
        self.primary_ip = ''
        self.proxy_ip = list()
        self.headers = {
            'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
            'Referer': ''
        }
        self.redis_handler = self.connect_redis_server()
        print("create instance stop")

    def connect_redis_server(self):
        pool = redis.ConnectionPool(host=r_server['ip'], port=r_server['port'], password=['passwd'])
        return redis.Redis(connection_pool=pool)

    def set_primary_ip(self):
        print('set_primary_ip start')
        self.headers['Referer'] = self.query_address
        html = PyQuery(self.query_address, encoding='utf8', headers=self.headers)
        result = html('code').eq(0).text()
        self.primary_ip = result
        print('set_primary_ip stop')

    def get_proxy_ip(self):
        print('get_proxy_ip start')
        for address in self.proxy_address:
            self.headers['Referer'] = address
            html = PyQuery(address, encoding='utf8', headers=self.headers)
            result = html('tr')
            del result[0]
            for i in result.items():
                self.proxy_ip.append(
                    i('td').eq(1).text() + ":" + i('td').eq(2).text())
        print('get_proxy_ip stop')

    def check_and_save(self, proxy):
        self.headers['Referer'] = self.query_address
        try:
            resp = requests.get(self.query_address, proxies={'http': proxy}, headers=self.headers)
            html = PyQuery(resp.content.decode())
        except ProxyError:
            print('Expired:', proxy)
            return
        except UnicodeDecodeError:
            return
        result = html('code').eq(0).text()
        if result != self.primary_ip:
            self.redis_handler.sadd(r_server['s_name'], proxy)

    def save_proxy_ip(self):
        print('check_and_save start')
        self.redis_handler.delete(r_server['s_name'])
        for proxy in self.proxy_ip:
            Thread(target=self.check_and_save, args=(proxy,)).start()
        print('check_and_save stop')

    def start(self):
        self.set_primary_ip()
        self.get_proxy_ip()
        self.save_proxy_ip()
        print("end")

if __name__ == "__main__":
    ProxyDemo().start()
