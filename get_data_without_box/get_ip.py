# encoding=utf8
import urllib
from lxml import etree

import requests

from bs4 import BeautifulSoup

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'https://www.xicidaili.com/wn/4'

res = requests.get(url, headers=header).text
ip = etree.HTML(res)

ip = ip.xpath('//*[@id="ip_list"]/*')
myIp = ""
myPort = ""
data = ""
for i in range(0, len(ip)):
    'IP地址 端口'
    if i == 0:
        continue
    for j in range(0, len(ip[i])):

        if j == 1:
            myIp = ip[i][j].text

        if j == 2:
            res = myIp + " " + ip[i][j].text
            data = data + res + "\n"

with open("ip.txt", "w") as f:
    f.write(data)