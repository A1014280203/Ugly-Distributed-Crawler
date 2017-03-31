headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Referer': ''
}

r_server = {
    'ip': 'localhost',
    'port': '6379',
    'passwd': '',
    's_proxy': 'proxy_ip',
    's_url': 'url'
}

settings = {
    # 使用代理时最大尝试次数
    'maxtries': 3,
    # 每个版块遍历的页数
    'b_pages': 5,
    # 合格的回复下限
    'reply': 45,
    # 合格的阅读下限
    'read': 10000,
}
