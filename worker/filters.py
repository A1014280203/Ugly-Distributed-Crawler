from config import filters
from pyquery import PyQuery
import re


def is_locked(html):
    # 判断楼主是否被禁言或者需要回复查看
    doc = PyQuery(html)
    if doc('div').filter('.locked').length:
        return True
    return False


def is_poll(html):
    # 判断是不是投票贴
    doc = PyQuery(html)
    if doc('form').filter('#poll').length:
        return True
    return False


def need_to_login(html):
    # 是否需要登陆后查看
    result = html.xpath("//div/h3")
    if len(result):
        return True
    return False


def text_length_is_short(html):
    # 判断首楼内容是不是过短
    result = html.xpath("//div[@id='postlist']/div[1]//td[@class='t_f']//text()")
    if len(''.join(result)) < filters['txt-len']:
        return True
    return False


def auth_reply_over_max(html):
    # 判断楼主在第一页中是否回复太多
    raw_auth_href_list = html.xpath("//div[@class='pi']/div[@class='authi']/a/@href")
    try:
        basic_href = raw_auth_href_list[0]
    except Exception:
        return None
    count = 0
    count_max = filters['re-max']
    for href in raw_auth_href_list:
        if basic_href == href:
            count += 1
            if count > count_max:
                return None
    if basic_href == raw_auth_href_list[1]:
        return 2
    else:
        return 1


def clear_text(text=''):
    t_text = text.replace(r'\xa0', ' ')
    t_text = t_text.replace('下载附件', '')
    t_text = re.subn('\(.* Bytes, 下载次数: .*\)', '', t_text)[0]
    t_text = re.subn('\d*-\d*-\d* \d*:\d* 上传', '', t_text)[0]
    t_text = re.subn('.*\.png\s', '', t_text)[0]
    return t_text.strip()
