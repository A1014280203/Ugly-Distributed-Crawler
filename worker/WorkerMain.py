from .basic_func import make_redis_handler, get_url, pop_url
from .filters import is_poll, is_locked, text_length_is_short, \
    need_to_login, auth_reply_over_max, clear_text
from pyquery import PyQuery
from lxml import etree
from .db import db_add
import threading
import time


class WorkerDemo(object):

    def __init__(self):
        self.uhandler = make_redis_handler()

    def check_post(self, html):
        if is_locked(html):
            return False
        if is_poll(html):
            return False
        if text_length_is_short(html):
            return False
        if need_to_login(html):
            return False
        return auth_reply_over_max(html)

    def get_text_of_post(self, url):
        resp = get_url(url)
        flag = self.check_post(etree.HTML(resp.content.decode()))
        if flag:
            doc = PyQuery(resp.content.decode())
            td_tags = doc('td').filter('.t_f')
            del td_tags[flag:]
            text = ''
            for td in td_tags.items():
                text += clear_text(td.text())
            return text

    def save_single_post(self, url):
        text = self.get_text_of_post(url)
        db_add(text)

    def save_all_posts(self):
        while True:
            url = pop_url()
            if not url:
                time.sleep(3)
                continue
            threading.Thread(target=self.save_single_post, args=(url,)).start()

    def start(self):
        self.save_all_posts()

if __name__ == '__main__':
    WorkerDemo().get_text_of_post('http://bbs.kaoyan.com/t7729132p1')