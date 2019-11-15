import requests
from bs4 import BeautifulSoup
import re
from get_data_without_box.get_movie_info import get_details

import time

# 一页运行时间：33秒
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.douban.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

#有票房电影抓取：豆列---详情页总过程
def get_and_write(year,url_id):
    print('目前在进行第'+year+'年的抓取\n')
    count = 0
    fw = open('all_movie_detail_' + year + '.txt', 'a', encoding='utf-8')
    fw.write('name,url,rate,box,director,writer,actor,genre,place,language,releasedate,movietime' + '\n')

    while(1):
        url = 'https://www.douban.com/doulist/' + url_id + '/?start=' + str(count) + '&sort=seq&playable=0&sub_type='
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.text

        html = BeautifulSoup(data, features='lxml')
        article = html.select('.article')[0]
        doulist = article.select('.doulist-item')
        #判断一下当前页面有没有电影可以抓
        if len(doulist):
            print("这一页第一部电影的序号是：%s" % (count))
            count += 25
        else:
            break
        # 获取所有详情页连接
        for item in doulist:
            a = item.find_all('div', attrs={"class": "title"})[0].select('a')[0]
            name = a.get_text().strip().split()[0]
            movie_url = a['href']

            # 评分也在这里顺便抓下来
            douban_rate_tag = item.select('span.rating_nums')
            if douban_rate_tag:
                douban_rate = douban_rate_tag[0].get_text().strip()
            else:
                douban_rate = ''

            str_item = str(item)
            # 需要用正则表达式提取出票房box
            comment = item.select('div.comment-item.content')[0].get_text().strip()
            all_place = re.search('总票房(.*?)元', str_item, re.S)
            if not all_place:
                accu_place = re.search('累计票房(.*?)元', str_item, re.S)
                if accu_place:
                    box = accu_place.group(1)
                    if '亿' in box:
                        box = int(float(box[:-1].replace(',', '.')) * 100000000)
                    else:
                        if '千万' in box:
                            box = int(float(box[:-2]) * 10000)
                        else:
                            box = int(float(box[:-1]) * 10000)
            else:
                box = all_place.group(1)
                if '亿' in box:
                    box = int(float(box[:-1]) * 100000000)
                else:
                    if '千万' in box:
                        box = int(float(box[:-2]) * 10000)
                    else:
                        box = int(float(box[:-1]) * 10000)
            #print(movie_url + ',' + str(douban_rate) + ',' + str(box))
            director, writer, actor, genre, place, language, releasedate, movietime = get_details(url=movie_url)
            record = name + ',' + movie_url + ',' + str(douban_rate) + ',' + str(box) \
                     + ',' + director + ',' + writer + ',' + actor + ',' \
                     + genre + ',' + place + ',' \
                     + language + ',' + releasedate \
                     + ',' + movietime + '\n'
            print(record)
            fw.write(record)
            time.sleep(1)

    fw.close()
    return

if __name__ == '__main__':
    url_every_year = {'2015': '37815319', '2016': '42975662', '2017': '45837913', '2018': '46436333',
                      '2019': '111687014'}
    for year, year_id in url_every_year.items():
        get_and_write(year=year, url_id=year_id)
