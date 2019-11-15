import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from pandas.plotting import scatter_matrix

# 图5-7 收益与各种因素的关系图

plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
plt.style.use('ggplot')

tmdb = pd.read_csv('txtdata/tmdb_5000_movies.csv')


# 任务1：国内外电影类型对比
# 抽取出的字段：电影评分，电影类型
# tmdb_genres = tmdb['genres'].apply(json.loads)

# # JSON变列表
# for row in tmdb_genres:
#     for index in range(len(row)):
#         row[index] = row[index]['name']

# # 列表取单
# tmdb_genres = tmdb_genres.str.get(0).dropna()
# # 计算个数
# tmdb_genres_count = tmdb_genres.value_counts(ascending=True)
# tmdb_genres_count = pd.DataFrame(tmdb_genres_count)
# tmdb_genres_count = tmdb_genres_count[tmdb_genres_count['genres'] > 80]


# # 取国内数据集
#
# douban = pd.read_csv('txtdata/1959-2019painting.txt')
# douban_genres = douban['genre'].str.split('/').str.get(0).dropna()
# douban_genres_count = douban_genres.value_counts(ascending=True)
# df_douban_count = pd.DataFrame(douban_genres_count)
#
# df_douban_count = df_douban_count[df_douban_count['genre'] > 100]
#
#
# plt.figure(figsize=(10,10))
# plt.subplot(2,2,1)
# df_douban_count['genre'].plot(kind='barh')
# plt.title('电影类型分布(国内)',fontsize=18)
# plt.xlabel('数量')
#
# plt.subplot(2,2,2)
# df_douban_count['genre'].plot(kind='pie', autopct='%1.1f%%', legend=False)
# plt.title('电影类型分布(国内)',fontsize=18)
# plt.ylabel('')
#
# plt.subplot(2,2,3)
# tmdb_genres_count['genres'].plot(kind='barh')
# plt.title('电影类型分布(国外)',fontsize=18)
# plt.xlabel('数量')
#
#
# plt.subplot(2,2,4)
# tmdb_genres_count['genres'].plot(kind='pie', autopct='%1.1f%%', legend=False)
# plt.ylabel('')
# plt.title('电影类型分布(国外)',fontsize=18)
# plt.show()


# 类型对比结束-----------------------

# 图5-7 收益与各种因素的关系
# 取budget  genres popularity revenue vote_average vote_count
# col = ['budget', 'popularity', 'revenue', 'vote_average', 'vote_count']
# need_columns = tmdb[col]
# need_columns[['budget', 'revenue']] = need_columns[['budget','revenue']].apply(lambda row : row/100000000)
#
# plt.figure(figsize=(12, 12))
# plt.subplot(2, 2, 1)
# plt.scatter(x=need_columns['budget'], y=need_columns['revenue'])
# plt.title('预算和收益的关系',fontsize=20)
# plt.xlabel('预算(亿元)',fontsize=20)
# plt.ylabel('收益(亿元)',fontsize=20)
# plt.subplot(2, 2, 2)
# plt.scatter(x=need_columns['popularity'], y=need_columns['revenue'])
# plt.title('人气和收益的关系',fontsize=20)
# plt.xlabel('人气',fontsize=20)
# plt.ylabel('收益(亿元)',fontsize=20)
# plt.subplot(2,2,3)
# plt.scatter(x=need_columns['vote_average'], y=need_columns['revenue'])
# plt.title('电影评分和收益的关系',fontsize=20)
# plt.xlabel('电影评分(打分范围0-10)',fontsize=20)
# plt.ylabel('收益(亿元)',fontsize=20)
# plt.subplot(2, 2, 4)
# plt.scatter(x=need_columns['vote_count'], y=need_columns['revenue'])
# plt.title('IMDB评分人数和收益的关系',fontsize=20)
# plt.xlabel('评分人数',fontsize=20)
# plt.ylabel('收益(亿元)',fontsize=20)
# plt.show()

#-------------------------------------------


col = ['budget', 'popularity', 'revenue', 'vote_average', 'vote_count']
need_columns = tmdb[col].copy()
#plt.figure(figsize=(7, 12))
#plt.subplot(2, 2, 1)
#plt.scatter(x=need_columns['budget'], y=need_columns['revenue'])
# plt.title('预算和收益的关系',fontsize=20)
# plt.xlabel('预算(亿元)',fontsize=20)
# plt.ylabel('收益(亿元)',fontsize=20)
# plt.show()



