# Ugly-Distributed-Crawler
## 简陋的分布式爬虫
新手向，基于Redis构建的分布式爬虫。
以爬取考研网的贴子为例，利用 PyQuery, lxml 进行解析，将符合要求的文章文本存入MySQ数据库中。
## 结构简介
#### cooperator
协作模块，用于为Master&Worker模块提供代理IP支持
#### master
提取满足条件的文章url，并交给Worker进一步处理
#### Worker
解析文章内容，将符合要求的存入数据库

## 环境依赖 ##
sqlalchemy => 1.0.13  
pyquery => 1.2.17  
requests => 2.12.3  
redis => 2.10.5  
lxml => 3.6.0  
> 1. 需要预先安装MySQL-server 和 Redis-server.  
> 2. MySQL中应有名为kybsrc的数据库，且该数据库包含一个名为posts的表，拥有num(INT AUTO_INCREMENT)和post(TEXT)两个字段。

## 如何启动

#### 0. 先配置好各模块所引用的配置文件  

#### 1. 为了更好地运行，cooperator/start.py 应提前开始并完成一次工作函数执行
> 第一次执行完后，每五分钟运行一次工作函数

#### 2. 启动 master/start.py 
> 默认只执行一次

#### 3. 启动 worker/start.py
> 默认循环监听是否有新的URL待解析

## 核心点说明
#### 1. 通过Redis的集合类型进行代理IP和URL的传递

```python
# Summary Reference
# ---------
# 创建句柄
def make_redis_handler():
    pool = redis.ConnectionPool(host=r_server['ip'], port=r_server['port'], password=r_server['passwd'])
    return redis.Redis(connection_pool=pool)

# 获得句柄
def make_proxy_handler():
    return make_redis_handler()

# 保存到指定的set下
def check_and_save(self, proxy):
 'pass'
   self.redis_handler.sadd(r_server['s_name'], proxy)
```
#### 2. 由于在验证代理IP和使用封装的get_url()函数的时候网络IO较多，所以使用多线程（效果还是很明显的）。 

```python
#Summary Reference
#---------
def save_proxy_ip(self):
    'pass'
    for proxy in self.proxy_ip:
        Thread(target=self.check_and_save, args=(proxy,)).start()

def get_url(url):
    'pass'
    while True:
    'pass'
        resp = request('get', url, headers=headers, proxies={'http': proxy})
    'pass'
```

## 项目地址
#### https://github.com/PyCN/Ugly-Distributed-Crawler
> 有任何问题可以与我联系(微信：smartseer)
