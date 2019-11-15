import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
plt.style.use('ggplot')

movies = pd.read_csv('txtdata/tmdb_5000_movies.csv')
credit = pd.read_csv('txtdata/tmdb_5000_credits.csv')

# 清洗TMDB数据集

# 数据读出来
# 首先：把数据合并
# 其次：把JSON数据读取出来转变成 XX/XX的形式

# 1 删除credit的title列，因为重复了
credit.drop(columns=['title'], inplace=True)
# 2 合并movies和credit

final = pd.merge(movies, credit, left_on='id', right_on='movie_id', how='left')

# 3 删除不需要的字段：主页，原始语言，原始标题，简介，宣传词

final.drop(['homepage','original_language',
            'original_title','overview',
            'spoken_languages',
           'status','tagline','movie_id'], inplace=True,axis=1)

# 4 JSON数据转换成 XX/XX 的字符串形式
# json格式的有genres,keywords,production_companies,production_countries,cast,crew
json_columns = ['genres','keywords','production_companies','production_countries','cast','crew']

# 由于原始是字符串，所以要转换成字典形式，使用json.loads
for column in json_columns:
    final[column] = final[column].apply(json.loads)

# 5 cast和crew有不同的取出规则，先把一般规则的转换成XX/XX的形式

normal_json_column = ['genres','keywords','production_companies','production_countries']

def json_get_name(row_list):
    list = []
    for s_dict in row_list:
        list.append(s_dict['name'])
    return '/'.join(list)

def json_get_actor(row_list):
    list = []
    for s_dict in row_list:
        list.append(s_dict['character'])
    return '/'.join(list[0:2])

def json_get_director(row_list):
    list = []
    for s_dict in row_list:
        if s_dict['job'] == 'Director':
            list.append(s_dict['name'])
    return '/'.join(list[0:1])


for json_column in normal_json_column:
    final[json_column] = final[json_column].apply(json_get_name)

final['cast'] = final['cast'].apply(json_get_name)
final['crew'] = final['crew'].apply(json_get_director)


# 最后写入文件
final.to_csv('tmdb_clean.csv', index=False)


