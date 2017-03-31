#Ugly-Distributed-Crawler
## 简陋的分布式爬虫
新手向。
基于Redis构建的分布式爬虫  
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

#### 1. 为了更好地运行，cooperator/start.py 应提前开始并完成一次工作函数执行
> 第一次执行完后，每五分钟运行一次工作函数

#### 2. 启动 master/start.py 
> 默认只执行一次

#### 3. 启动 worker/start.py
> 默认循环监听是否有新的URL待解析
