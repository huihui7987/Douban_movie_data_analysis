# encoding=utf8
import urllib
import socket
from urllib import request

socket.setdefaulttimeout(3)
f = open("ip.txt")
fw = open('good_ip.txt', 'w')
lines = f.readlines()
proxys = []
# 把文档里的IP组装成一个列表
for i in range(0, len(lines)):
    ip = lines[i].strip("\n").split(" ")
    proxy_host = "https://" + ip[0] + ":" + ip[1]
    proxy_temp = {"https": proxy_host}
    proxys.append(proxy_temp)
# 一个一个测试
url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%BB%8F%E5%85%B8&start=0"
for proxy in proxys:
    try:
        proxy_support = request.ProxyHandler(proxy)
        opener = request.build_opener(proxy_support)
        res = opener.open(url).read()
        print(str(proxy) + 'is good!')
        fw.write(str(proxy) + '\n')
    except Exception as e:
        print(proxy)
        print(e)
        continue


f.close()
fw.close()