#这个文件专门用来测试正则表达式匹不匹配
import re
from bs4 import BeautifulSoup

html = """"""

#data = BeautifulSoup(html, features='lxml')

#得到所有导演的思路： 先正则抓到所有导演的HTML内容，用BS4解析，再get_text出来

# director_patten = re.search("<span><span class='pl'>导演</span>:(.*?)<br/>", html, re.S)
# if director_patten:
#     dictor_raw = all_place.group(1)
#     dictor_html = BeautifulSoup(data, features='lxml')
#     print(dictor_html.get_text().replace(' ', ''))

# 得到所有编剧：一样
# fr = open('movie_info.txt', 'r', encoding='utf-8')
# data = fr.read()
#
#
# html = BeautifulSoup(data, features='lxml')

# 得到全部编剧
# writer_patten = re.search('<span><span class="pl">编剧</span>:(.*?)<br/>', str(html), re.S)
# if writer_patten:
#     writer_raw = writer_patten.group(1)
#     writer_html = BeautifulSoup(writer_raw, features='lxml')
#     print(writer_html.get_text().replace(' ', ''))


#得到单个编剧
# html = BeautifulSoup(data, features='lxml')
#
# writer_patten = re.search('<span><span class="pl">编剧</span>: <span class="attrs"><a href=.*?>(.*?)</a>', str(html), re.S)
# if writer_patten:
#     print(writer_patten.group(1))


# 票房
comment = '【进口分账】2010年1月4日开画，截至4月25日累计票房13.5亿元。'
all_place = re.search('总票房(.*?)元', comment, re.S)
if not all_place:
    accu_place = re.search('累计票房(.*?)元', comment, re.S)
    if accu_place:
        box = accu_place.group(1)
        if '亿' in box:
            box = int(float(box[:-1]) * 100000000)

        else:
            box = int(float(box[:-1]) * 10000)
else:
    box = all_place.group(1)
    if '亿' in box:
        box = int(float(box[:-1]) * 100000000)
    else:
        box = int(float(box[:-1]) * 10000)

print(box)

