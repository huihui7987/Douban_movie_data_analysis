import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter



#给URL，得到详情页数据，适用于有票房的电影
def get_details(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    data = response.text

    # fr = open('movie_info.txt', 'r', encoding='utf-8')
    # data = fr.read()

    html = BeautifulSoup(data, features='lxml')
    info = html.select('#info')[0]


    # 开始匹配
    str_info = str(info)
    patten_director = re.search('rel="v:directedBy">(.*?)</a>', str_info, re.S)
    if patten_director:
        director = patten_director.group(1).strip()
    else:
        director = ''

    writer_patten = re.search('<span><span class="pl">编剧</span>: <span class="attrs"><a href=.*?>(.*?)</a>', str_info,
                              re.S)
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
        releasedate = releasedate_tag.get_text().strip().split('(')[0]
    else:
        releasedate = ''
    movietime_tag = info.find('span', attrs={'property': 'v:runtime'})
    if movietime_tag:
        movietime = movietime_tag.get_text().replace(' ', '').split('(')[0]
    else:
        movietime = ''
    # 国家/地区的正则表达式
    patten_place = re.search('制片国家/地区:</span>(.*?)<br/>', str_info, re.S)
    if patten_place:
        place = patten_place.group(1).replace(' ', '')
        # print(place)
    else:
        place = ''
    # 语言的正则表达式
    language_place = re.search('语言:</span>(.*?)<br/>', str_info, re.S)
    if language_place:
        language = language_place.group(1).replace(' ', '')
        # print(language)
    else:
        language = ''

    # print(director + ',' + writer + ',' + actor + ',' + genre + ',' +
    #       place + ',' + language + ',' + releasedate + ',' +
    #       movietime)
    return director, writer, actor, genre, place, language, releasedate, movietime, comment_count, review_count

#给URL，得到详情页数据，适用于无票房的电影
#取消上映日期和票房，以电影上映年份和参与评分的人数代替
# 优化了导演的爬取机制
def get_details_without_box(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': 'bid=mX5JoV-6zIs; __yadk_uid=l0Vp43WiHzMy3sNeTiT8cidnCFShnuEW; douban-fav-remind=1; douban-profile-remind=1; dbcl2="70820094:N5wIjv23m4I"; ll="108088"; ct=y; gr_user_id=f8468c45-4579-4a91-80bb-bc3320e042cb; ck=NSf_; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1555679903%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utmt=1; _vwo_uuid_v2=DB9EED638DF4E43689945E7939854DDD9|904d1fd966f7217fc34c216bc11e0cdb; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=a9e508f8247aaccd.1548340344.61.1555681962.1555667441.; _pk_ses.100001.4cf6=*; __utma=30149280.1609998180.1555232765.1555667220.1555679548.16; __utmb=30149280.6.10.1555679548; __utmc=30149280; __utmz=30149280.1555679548.16.15.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.7082; __utma=223695111.1678517466.1551056746.1555667436.1555679903.53; __utmb=223695111.0.10.1555679903; __utmc=223695111; __utmz=223695111.1555679903.53.41.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
    }

    proxies = {
        'http': '110.52.235.114:9999',
        'https': '110.52.235.114:9999',
    }
    # #设置超时重连机制
    # s = requests.Session()
    # s.mount('http://', HTTPAdapter(max_retries=3))
    # s.mount('https://', HTTPAdapter(max_retries=3))

    #连接
    try:
        response = requests.get(url=url, timeout=4, headers=headers)
    except requests.exceptions.RequestException as e:
        #如果url超时就把错误信息写进log
        fw = open('log.txt', 'a', encoding='utf-8')
        fw.write('连接超时，url地址是:' + url + '\n')
        fw.close()
        error_info = {'status': 404}
        return error_info

    response.encoding = 'utf-8'
    data = response.text

    # fr = open('movie_info.txt', 'r', encoding='utf-8')
    # data = fr.read()

    html = BeautifulSoup(data, features='lxml')
    info_tag = html.select('#info')
    if not info_tag:
        error_info = {'status': 404}
        return error_info

    info = info_tag[0]


    # 开始匹配
    str_info = str(info)

    #电影名字
    name_tag = html.find('span', attrs={'property': 'v:itemreviewed'})
    if name_tag:
        name = name_tag.get_text().split()[0]
    else:
        name = ''

    #评分，评分人数
    rate_tag = html.select('strong.ll.rating_num')
    if rate_tag:
        rate = rate_tag[0].get_text().strip()
    else:
        rate = ''

    rating_people_tag = html.select('div.rating_sum span')
    if rating_people_tag:
        rating_people = rating_people_tag[0].get_text().strip()
    else:
        rating_people = ''

    #导演
    director = html.find_all('a', attrs={'rel': 'v:directedBy'})
    if director:
        list_director = list(map(BeautifulSoup.get_text, director))
        director = '/'.join(list_director).strip()
    else:
        director = ''

    writer_patten = re.search('<span><span class="pl">编剧</span>: <span class="attrs"><a href=.*?>(.*?)</a>', str_info,
                              re.S)
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

    # 上映日期取消，变成年份
    year = html.select('span.year')
    if year:
        year = year[0].get_text().strip('() ')
    else:
        year = ''

    movietime_tag = info.find('span', attrs={'property': 'v:runtime'})
    if movietime_tag:
        movietime = movietime_tag.get_text().replace(' ', '').split('(')[0]
    else:
        movietime = ''
    # 国家/地区的正则表达式
    patten_place = re.search('制片国家/地区:</span>(.*?)<br/>', str_info, re.S)
    if patten_place:
        place = patten_place.group(1).replace(' ', '')
        # print(place)
    else:
        place = ''
    # 语言的正则表达式
    language_place = re.search('语言:</span>(.*?)<br/>', str_info, re.S)
    if language_place:
        language = language_place.group(1).replace(' ', '')
        # print(language)
    else:
        language = ''

    # # 短评总数
    # comments = html.select('#comments-section span.pl')
    # if comments:
    #     comment_count = comments[0].get_text().replace(' ', '').replace('\n', '')
    # else:
    #     comment_count = ''
    # # 长评总数
    # reviews = html.select('section.reviews.mod.movie-content span.pl')
    # if reviews:
    #     review_count = reviews[0].get_text().replace(' ', '')
    # else:
    #     review_count = ''

    movie_info = {
        'status': 200,
        'name': name,
        'rate': rate,
        'rating_people': rating_people,
        'director': director,
        'writer': writer,
        'actor': actor,
        'genre': genre,
        'place': place,
        'language': language,
        'year': year,
        'movietime': movietime,
        # 'comment': comment_count,
        # 'review': review_count,
    }
    return movie_info

def get_comments(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': 'bid=mX5JoV-6zIs; __yadk_uid=l0Vp43WiHzMy3sNeTiT8cidnCFShnuEW; douban-fav-remind=1; douban-profile-remind=1; dbcl2="70820094:N5wIjv23m4I"; ll="108088"; ct=y; gr_user_id=f8468c45-4579-4a91-80bb-bc3320e042cb; ck=NSf_; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1555679903%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utmt=1; _vwo_uuid_v2=DB9EED638DF4E43689945E7939854DDD9|904d1fd966f7217fc34c216bc11e0cdb; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=a9e508f8247aaccd.1548340344.61.1555681962.1555667441.; _pk_ses.100001.4cf6=*; __utma=30149280.1609998180.1555232765.1555667220.1555679548.16; __utmb=30149280.6.10.1555679548; __utmc=30149280; __utmz=30149280.1555679548.16.15.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.7082; __utma=223695111.1678517466.1551056746.1555667436.1555679903.53; __utmb=223695111.0.10.1555679903; __utmc=223695111; __utmz=223695111.1555679903.53.41.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
    }
    #连接
    try:
        response = requests.get(url=url, timeout=4, headers=headers)
    except requests.exceptions.RequestException as e:
        #如果url超时就把错误信息写进log
        fw = open('log.txt', 'a', encoding='utf-8')
        fw.write('连接超时，url地址是:' + url + '\n')
        fw.close()
        error_info = {'status': 404}
        return error_info

    response.encoding = 'utf-8'
    data = response.text

    # fr = open('movie_info.txt', 'r', encoding='utf-8')
    # data = fr.read()

    html = BeautifulSoup(data, features='lxml')
    info_tag = html.select('#info')
    if not info_tag:
        error_info = {'status': 404}
        return error_info

    info = info_tag[0]


    # 开始匹配
    str_info = str(info)

    #电影名字
    name_tag = html.find('span', attrs={'property': 'v:itemreviewed'})
    if name_tag:
        name = name_tag.get_text().split()[0]
    else:
        name = ''

    # 短评总数
    comments = html.select('#comments-section span.pl')
    if comments:
        comment_count = comments[0].get_text().replace(' ', '').replace('\n', '')
    else:
        comment_count = ''
    # 长评总数
    reviews = html.select('section.reviews.mod.movie-content span.pl')
    if reviews:
        review_count = reviews[0].get_text().replace(' ', '')
    else:
        review_count = ''

    movie_info = {
        'status': 200,
        'name': name,
        'comment': comment_count,
        'review': review_count,
    }
    return movie_info

if __name__ == '__main__':
    print(get_details_without_box(url=url))