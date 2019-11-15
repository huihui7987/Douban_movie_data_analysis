from get_data_without_box.get_movie_info import get_details_without_box
import requests
import time

#功能：抓取没有票房信息的电影数据
#解释：要先从网页上看爬网页的套路

# 常量定义
# 访问JSON API的headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Cookie': 'bid=mX5JoV-6zIs; __yadk_uid=l0Vp43WiHzMy3sNeTiT8cidnCFShnuEW; douban-fav-remind=1; douban-profile-remind=1; dbcl2="70820094:N5wIjv23m4I"; ll="108088"; ct=y; gr_user_id=f8468c45-4579-4a91-80bb-bc3320e042cb; ck=NSf_; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1555679903%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utmt=1; _vwo_uuid_v2=DB9EED638DF4E43689945E7939854DDD9|904d1fd966f7217fc34c216bc11e0cdb; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=a9e508f8247aaccd.1548340344.61.1555681962.1555667441.; _pk_ses.100001.4cf6=*; __utma=30149280.1609998180.1555232765.1555667220.1555679548.16; __utmb=30149280.6.10.1555679548; __utmc=30149280; __utmz=30149280.1555679548.16.15.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.7082; __utma=223695111.1678517466.1551056746.1555667436.1555679903.53; __utmb=223695111.0.10.1555679903; __utmc=223695111; __utmz=223695111.1555679903.53.41.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
}

count = 0
fw = open('txtdata/6.12.txt', 'w', encoding='utf-8')
fw.write('name,movie_url,comment,review' + '\n')
#程序开始
while(count < 4600):
    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=' + str(count) + '&year_range=2010,2019'
    print('当前轮第一部电影的序号是:', count)
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    jsondata = response.json()
    if len(jsondata):
        data = jsondata['data']
        for item in data:
            movie_url = item['url']
            # return name, rat
            # e, rating_people,director, writer, actor, genre, place, language, year, movietime
            # result 是一个字典，通过里面的status可以知道抓详情页是否成功
            result = get_details_without_box(movie_url)
            if result['status'] == 404:
                time.sleep(1)
                continue
            else:
                record = result['name'] + ',' + movie_url + ',' + result['rate'] + ',' + result['rating_people'] \
                         + ',' + result['director'] + ',' + result['writer'] + ',' + result['actor'] + ',' \
                         + result['genre'] + ',' + result['place'] + ',' \
                         + result['language'] + ',' + result['year'] \
                         + ',' + result['movietime'] + ',' + '\n'
                print(record)
                fw.write(record)
                time.sleep(1)
        #走到这里：说明这一页的JSON已经扒完,换下一页
        count += 20
    else:
        break
fw.close()

# # 只抓评论数
# while(count < 6000):
#     url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=' + str(count) + '&year_range=2010,2019'
#     print('当前轮第一部电影的序号是:', count)
#     response = requests.get(url=url, headers=headers)
#     response.encoding = 'utf-8'
#     jsondata = response.json()
#     if len(jsondata):
#         data = jsondata['data']
#         for item in data:
#             movie_url = item['url']
#             result = get_comments(movie_url)
#             if result['status'] == 404:
#                 time.sleep(4)
#                 continue
#             else:
#                 record = result['name'] + ',' + movie_url + ',' + result['comment'] + ',' + result['review'] + '\n'
#                 print(record)
#                 fw.write(record)
#                 time.sleep(4)
#         #走到这里：说明这一页的JSON已经扒完,换下一页
#         count += 20
#     else:
#         break

# --------------------------------------------
