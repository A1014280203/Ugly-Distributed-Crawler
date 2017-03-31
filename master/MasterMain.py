from .basic_func import get_url, make_redis_handler
from lxml import etree
from .config import settings, r_server
from multiprocessing import Pool


class MasterDemo(object):

    def __init__(self):
        self.index_url = 'http://bbs.kaoyan.com/'
        self.raw_block_url = dict()

    def get_block_url(self):
        print('get_block_url')
        resp = get_url(self.index_url)
        html = etree.HTML(resp.content.decode())
        a_tags = html.xpath('//*[@id="category_173"]/table/tr[1]/td[position()<5]//a')
        for a in a_tags:
            self.raw_block_url[a.text] = a.attrib['href'][:-1]

    def save_url(self, values, uhandler):
        print('save_url')
        uhandler.sadd(r_server['s_url'], *values)

    def delivery_post_url_by_block(self, raw_url):
        print('delivery_post_url_by_block')
        uhandler = make_redis_handler()
        for i in range(0, settings['b_pages']):
            made_url = raw_url + str(i+1)
            resp = get_url(made_url)
            html = etree.HTML(resp.content.decode())
            # 只记录符合阅读大于read，回复大于reply的
            raw_path = "//td[@class='num']/em[text()>{read_num}]/../a[text()>{reply_num}]/@href"
            made_path = raw_path.format(read_num=settings['read'], reply_num=settings['reply'])
            filtered_url_list = html.xpath(made_path)
            if len(filtered_url_list) < 1:
                print('Error: No data.@<delivery_post_url_by_block>:' + made_url)
                return
            self.save_url(filtered_url_list, uhandler)

    def delivery_post_url(self):
        print('delivery_post_url')
        # 使用多进程启动
        p = Pool(5)
        for url in self.raw_block_url.values():
            p.apply_async(self.delivery_post_url_by_block, args=(url,))
        p.close()
        p.join()

    def start(self):
        make_redis_handler().delete(r_server['s_url'])
        self.get_block_url()
        self.delivery_post_url()

if __name__ == "__main__":
    MasterDemo().start()
