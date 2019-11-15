import requests
from bs4 import BeautifulSoup
import re


url = 'https://movie.douban.com/subject/3596509/'




# response = requests.get(url)
# response.encoding = 'utf-8'
# data = response.text

fr = open('movie_info.txt', 'r', encoding='utf-8')
data = fr.read()

html = BeautifulSoup(data, features='lxml')
info = html.select('#info')[0]

#开始匹配
patten_director = re.search('rel="v:directedBy">(.*?)</a>', str(info), re.S)
if patten_director:
    director = patten_director.group(1).strip()
else:
    director = ''

writer_patten = re.search('<span><span class="pl">编剧</span>: <span class="attrs"><a href=.*?>(.*?)</a>', str(info), re.S)
if writer_patten:
    writer = writer_patten.group(1)
else:
    writer = ''

actor_tag = info.select('span.actor')
if actor_tag:
    actor = actor_tag[0].select('.attrs')[0].get_text().replace(' ', '')
else:
    actor = ''

genre_list = info.find_all('span', attrs={'property': 'v:genre'})
genre = ''
if len(genre_list):
    for item in genre_list:
        genre = genre + item.get_text().strip() + '/'
    genre = genre.rstrip('/')
else:
    genre = ''
# 国家地区，语言不在tag之内，需要用正则表达式
# 步骤：先定位到有数据的那个地方
releasedate_tag = info.find('span', attrs={'property': 'v:initialReleaseDate'})
if releasedate_tag:
    releasedate = releasedate_tag.get_text().strip()
else:
    releasedate = ''
movietime_tag = info.find('span', attrs={'property': 'v:runtime'})
if movietime_tag:
    movietime = movietime_tag.get_text().replace(' ', '')
else:
    movietime = ''
# 国家/地区的正则表达式
patten_place = re.search('制片国家/地区:</span>(.*?)<br/>', str(info), re.S)
if patten_place:
    place = patten_place.group(1).replace(' ', '')
    #print(place)
else:
    place = ''
# 语言的正则表达式
language_place = re.search('语言:</span>(.*?)<br/>', str(info), re.S)
if language_place:
    language = language_place.group(1).replace(' ', '')
    #print(language)
else:
    language = ''

print(director + ',' + writer + ',' + actor + ',' + genre + ',' +
      place + ',' + language + ',' + releasedate + ',' +
      movietime)
