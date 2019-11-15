import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 早期只抓到2010-2019数据的时候学习的作图

matplotlib.rcParams['font.family'] = 'SimHei'   #配置中文字体
matplotlib.rcParams['font.size'] = 15           #更改默认字体大小

df = pd.read_csv('clean2000-2009.txt')

# 以下是一些新增的数据清洗工作，在数据分析之前执行
# 增加一个新列：主要类型
df['main_genre'] = df['genre'].str.split('/').str.get(0)
df = df[(df['year'] > 2010) & (df['year'] < 2019)]



# 增加一个新值：电影类型的数量，大于100部的电影类型留下
genre_count = pd.DataFrame(df['main_genre'].value_counts(), columns=['counts'])
genre_count = genre_count[genre_count['counts'] > 100]


# -----------------------------------

#以下是数据分析

#处理类型全过程

# genre_sta = df['genre'].str.split('/', expand=True).fillna('0')
# print(genre_sta.head())
# a = genre_sta.apply(pd.value_counts).fillna(0)
# print(a.head())
# a = a.apply(lambda row: row.sum(),axis=1).astype(int)
# print(a)
# final_genre = pd.DataFrame(a, columns=['counts'])
# final_genre = final_genre.drop('0')
# print(final_genre)
# final_genre = final_genre.sort_values('counts', ascending=False).astype(int)
# print(final_genre)
# final_genre = final_genre[final_genre['counts'] > 100]
# final_genre.plot(kind='bar', figsize=(10, 5))
# plt.xticks(rotation=360)
# plt.xlabel("genre")
# plt.ylabel("counts")
# plt.show()


#-------------------------

#处理年份全过程

# year_sta = df['year'].value_counts()
# year_sta = pd.DataFrame(year_sta)
# year_sta.columns = ['counts']
# year_sta = year_sta.sort_index().astype(int)
# print(year_sta)
# year_sta = year_sta[year_sta['counts'] > 100]
# year_sta.plot(kind='bar')
# plt.xlabel("year")
# plt.ylabel("movies")
# plt.yticks(range(100, 900, 100))
# plt.show()

#---------------------------


# 处理演员的过程
# 和处理genre相似，但是由于演员较多，应该只选取一部分
# 思路是：处理之后，取一部分[[0, 1, 2, 3, 4, 5]]

# actor_sta = df['actor'].str.split('/', expand=True).fillna('0')
# actor_sta = actor_sta[[0, 1, 2, 3, 4, 5]]
# a = actor_sta.apply(pd.value_counts).fillna(0)
# print(a.head())
# a = a.apply(lambda row: row.sum(), axis=1).astype(int)
# print(a.head())
# final_actor = pd.DataFrame(a, columns=['counts'])
# final_actor = final_actor.drop('0')
# print(final_actor.head())
# final_actor = final_actor.sort_values('counts', ascending=False)
# #删除出现次数小于10的演员
# final_actor = final_actor[final_actor['counts'] > 10]
# print(final_actor)

#-----------------------------


# 国家处理全过程,生成饼图

# country_sta = df['place'].str.split('/', expand=True).fillna('0')
# a = country_sta.apply(pd.value_counts).fillna(0)
# a = a.apply(lambda row: row.sum(), axis=1).astype(int)
# final_country = pd.DataFrame(a, columns=['counts'])
# final_country = final_country.drop('0')
# final_country = final_country.sort_values('counts', ascending=False).astype(int)
# more_country = final_country[final_country['counts'] > 200].astype(int)
# less_country = final_country[final_country['counts'] < 200].astype(int)
# less_country = less_country.apply(lambda column: column.sum(), axis=0).astype(int)
# less_country = pd.DataFrame(less_country, columns=['counts'])
# less_country.index = ['其他']
# final_country = pd.concat([more_country, less_country])
# final_country.plot(kind='pie', y='counts', figsize=(10, 10), autopct='%1.1f%%', legend=False)
# #plt.legend(loc='upper right', ncol=3)
# plt.show()

# --------------------

# '类型' 和'年代' 结合一起分析
# 我现在有每部电影的年代和类型
# 处理的结果：'动作','2018年','XX部'



# groupby返回结果：index（单个或多个，根据你分组的依据），单值的series

# 主类型的饼图 插曲，不一定用得上
# genre_count = df[['main_genre']].groupby(['main_genre']).size()
# genre_count = genre_count.sort_values(ascending=False, by='counts')
# others = genre_count[genre_count['counts'] < 100].apply(lambda row: row.sum(), axis=0)
# final = genre_count[genre_count['counts'] > 100]
# final.loc['其他'] = others
# print(final)
# final.plot(kind='pie', y='counts', figsize=(10, 10), autopct='%1.1f%%', legend=False)
# plt.show()

#---------------

# 类型随年代变化的 多折线图

# 类型从多到少：剧情，喜剧，动作，动画，爱情，惊悚，悬疑，科幻，恐怖

# 以下是得到这个类型的list的过程
# genre_count = df[['main_genre']].groupby(['main_genre']).size()
# genre_count = pd.DataFrame(genre_count.sort_values(ascending=False), columns=['counts'])
# genre_count = genre_count[genre_count['counts'] > 100]

# 得到了这个list，开始画图
# index_list = genre_count.index.values
# genre_year = df[['main_genre', 'year']].groupby(['main_genre', 'year']).size()
# color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5']
# count = 0
# fig = plt.figure(figsize=(10, 10))
# # 8个类型，8种颜色
# for index in index_list:
#     plt.plot(genre_year[index].index, genre_year[index].values, color=color[count], label=index)
#     count += 1
# plt.legend(ncol=3)
# plt.show()

#-----------------------------------------------


# 哪类电影的平均分更高？
# 思路：取类型和评分两列出来，按类型分组，求平均值，画图
# 网上有一个做得很漂亮的例子，基于类型数量然后把平均分的点画上去
# 我先把平均分画出来
# 评价人数起码大于1000


genre_rate = df[['main_genre', 'rate']]
genre_rate_group = genre_rate.groupby('main_genre')
genre_rate_mean = genre_rate_group.mean()
genre_rate_count = genre_rate_group.count()
# 删除行满足以下条件：counts小于100
print(genre_rate_mean)
print(genre_rate_count)
final = pd.concat([genre_rate_mean, genre_rate_count], axis=1)
final.columns = ['mean', 'counts']
final = final[final['counts'] > 100].sort_values('counts', ascending=False)
final = final.round(1)
print(final)

fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(111)
ax1.bar(final.index, final['counts'].values,color='orange')
ax1.set_ylabel('电影数')

for x, y in zip(final.index, final['counts'].values):
    ax1.text(x, y, y, ha='center', va='bottom', fontsize=20)

ax2 = ax1.twinx()

ax2.plot(final.index, final['mean'].values, 'bo-', ms=40)

for x, y in zip(final.index, final['mean'].values):
    ax2.annotate(round(y, 1), xy=(x, y), color='white', fontsize=20, weight='bold', ha='center', va='center')
ax2.set_yticks(range(0, 11, 1))
ax2.set_ylabel('平均分')
plt.show()



# 分析“这个属性” 和 “这个属性出现的次数” 有关的问题
# 例如：电影类型和个数的关系，电影制作国家和个数的关系
# 写成一个函数
# 传入原本的dataframe和处理的字段名，返回一个处理好的dataframe
def analy_counts(dataframe, label):
    label = dataframe[label].str.split('/', expand=True).fillna('0')
    label_counts = label.apply(pd.value_counts).fillna(0)
    label_counts = label_counts.apply(lambda row: row.sum(), axis=1).astype(int)
    final_counts = pd.DataFrame(label_counts, columns=['counts'])
    final_counts = final_counts.drop('0')
    final_counts = final_counts.sort_values('counts', ascending=False).astype(int)
    return final_counts


