from CoperProxy import ProxyDemo
import time
from config import settings

# 首先配置好config文件
while True:
    ProxyDemo().start()
    time.sleep(settings['interval'])
