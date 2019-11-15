from bs4 import BeautifulSoup
import time
start = time.time()
headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': 'll="118308"; bid=cs3254cee5A; _vwo_uuid_v2=D0A14A64BEF614617B6A1C8DB29B129C6|96fd95a80214c4f63668c5dfafa0c068; douban-fav-remind=1; push_doumail_num=0; __utmv=30149280.7082; __utmz=30149280.1552399666.7.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/doulist/226734/; push_noty_num=0; __utma=30149280.693474884.1551052162.1555339917.1555653702.21; __utmc=30149280; __utmt=1; __utmb=30149280.1.10.1555653702; ap_v=0,6.0',
}

# url = 'https://movie.douban.com/subject/27202819/'
#
# response = requests.get(url)
# response.encoding = 'utf-8'
# data = response.text

fr = open('movie_info.txt', 'r', encoding='utf-8')
data = fr.read()

html = BeautifulSoup(data, features='lxml')


comments = html.select('#comments-section span.pl')[0]
comment_count = comments.get_text().replace(' ', '').replace('\n', '')
print(comment_count)

reviews = html.select('section.reviews.mod.movie-content span.pl')[0]
review_count = reviews.get_text().replace(' ', '')
print(review_count)

