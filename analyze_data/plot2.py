import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import wordcloud

# 图5-1到图5-6；电影产业的概况图

font = r'C:\Windows\Fonts\simfang.ttf'
matplotlib.rcParams['font.family'] = 'SimHei'   #配置中文字体
matplotlib.rcParams['font.size'] = 15           #更改默认字体大小
plt.style.use('ggplot')

def analy_counts(dataframe, label):
    label = dataframe[label].str.split('/', expand=True).fillna('0')
    label_counts = label.apply(pd.value_counts).fillna(0)
    label_counts = label_counts.apply(lambda row: row.sum(), axis=1).astype(int)
    final_counts = pd.DataFrame(label_counts, columns=['counts'])
    final_counts = final_counts.drop('0')
    final_counts = final_counts.sort_values('counts', ascending=False).astype(int)
    return final_counts

# 柱状图，某一文本类型 + 平均分
def label_plus_rate(df,label,title):
    df.dropna(subset=[label], inplace=True)
    genre_rate = df[[label, 'rate']]
    genre_rate_group = genre_rate.groupby(label)
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
    plt.title(title,fontsize=16)
    ax1 = fig.add_subplot(111)
    ax1.bar(final.index, final['counts'].values, color='orange')
    ax1.set_ylabel('电影数',fontsize=16)

    for x, y in zip(final.index, final['counts'].values):
        ax1.text(x, y, y, ha='center', va='bottom', fontsize=20)

    ax2 = ax1.twinx()

    ax2.plot(final.index, final['mean'].values, 'o-', ms=40, color='cadetblue')

    for x, y in zip(final.index, final['mean'].values):
        ax2.annotate(round(y, 1), xy=(x, y), color='white', fontsize=20, weight='bold', ha='center', va='center')
    ax2.set_yticks(range(0, 11, 1))
    ax2.set_ylabel('平均分',fontsize=16)
    plt.tick_params(top='off', right='off')
    plt.show()


def generate_cloud(df, label):
    movie_premium = df[(df['rate'] > 8.0) & (df['rating_people'] > 1000)].dropna()
    movie_premium.dropna(subset=[label], inplace=True)
    director_premium = movie_premium[label].str.split('/')

    director_string = ''
    for i in director_premium:
        for j in i:
            if '·' in j:
                j = j.replace('·', '')
            director_string += ''.join(j) + ' '

    print(director_string)

    cloud = wordcloud.WordCloud(background_color="black",scale=4,max_words=100,
                                    width=1000, height=1000, margin=2,max_font_size=150,
                                    font_path=font)
    cloud.generate_from_text(director_string)
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()
    cloud.to_file(label+'_word_cloud.png')

# 用词云统计导演
# df = pd.read_csv('txtdata/1959-2019painting.txt')
# movie_premium = df[(df['rate'] > 7.0) & (df['rating_people'] > 1000)].dropna()
#
# director_premium = movie_premium['director'].str.split('/')
#
# director_string = ''
# for i in director_premium:
#     for j in i:
#         if '·' in j:
#             j = j.replace('·', '')
#         director_string += ''.join(j) + ' '
#
# print(director_string)
#
# wordcloud = wordcloud.WordCloud(background_color="black",scale=4,max_words=100,
#                                 width=1000, height=1000, margin=2,max_font_size=150,
#                                 font_path=font)
# wordcloud.generate_from_text(director_string)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
# wordcloud.to_file('director.png')

# 用词云统计演员
# # 演员只选前三
# actor_premium = movie_premium['actor'].str.split('/').apply(lambda row: row[:3])
#
# actor_string = ''
# for i in actor_premium:
#     for j in i:
#         if '·' in j:
#             j = j.replace('·', '')
#             actor_string += ''.join(j) + ' '
#
# print(actor_string)
# wordcloud = wordcloud.WordCloud(background_color="black",scale=4,max_words=100,
#                                 width=1000, height=1000, margin=2,max_font_size=150,
#                                 font_path=font)
# wordcloud.generate_from_text(actor_string)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
# wordcloud.to_file('actor.png')

#----------------------------

#

df = pd.read_csv('txtdata/1959-2019painting.txt')
print(df.info())
df.drop_duplicates(inplace=True)

# 图5-4 年份图（条形）
# plt.figure(figsize=(10,10))
# df['main_genre'] = df['genre'].str.split('/').str.get(0)
# year_count = df[df['year'] > 1980]
# year_count = year_count['year'].value_counts(ascending=False)
# year_count.plot(kind='line')
# plt.show()


# 电影时长分布图(直方图)
# runtime = df['movietime']
# runtime = runtime.dropna().astype(np.int64)
# plt.hist(runtime, bins=14, range=(50, 200), color='steelblue',edgecolor='k')
# plt.xticks(np.arange(50, 200, 10))
# plt.tick_params(top='off', right='off')
# plt.title('电影时长分布')
# plt.xlabel('时长(分钟)')
# plt.ylabel('电影数')
# plt.savefig('电影时长分布')
# plt.show()

# -----------------------

# 5-2 处理国家 + 平均分
# df['main_genre'] = df['genre'].str.split('/').str.get(0)
# label_plus_rate(df, 'main_genre', '电影类型分布以及平均分')
# 5-1 处理类型 + 平均分
# df['main_country'] = df['place'].str.split('/').str.get(0)
# label_plus_rate(df, 'main_country', '电影制作国家/制作地区分布以及平均分')

#------------------------

# 5-5,5-6 处理演员和导演（词云）
# generate_cloud(df, 'director')


# 5-4 年代 + 不同类型电影数量
# df['main_genre'] = df['genre'].str.split('/').str.get(0)
# df = df[(df['year'] > 1940) & (df['year'] < 2019)]
# genre_count = df[['main_genre']].groupby(['main_genre']).size()
# genre_count = pd.DataFrame(genre_count.sort_values(ascending=False), columns=['counts'])
# genre_count = genre_count[genre_count['counts'] > 100]
#
# # 得到了这个list，开始画图
# index_list = genre_count.index.values
# print(index_list)
# genre_year = df[['main_genre', 'year']].groupby(['main_genre', 'year']).size()
# color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5', 'orange']
# count = 0
# fig = plt.figure(figsize=(5, 5))
# # 8个类型，8种颜色
# for index in index_list:
#     plt.plot(genre_year[index].index, genre_year[index].values, color=color[count], label=index)
#     count += 1
# plt.title('每年的电影数(按类型区分)')
# plt.xlabel('年份')
# plt.ylabel('电影数')
# plt.legend(ncol=3)
# plt.show()

#-----------------------------------



# 图5-3 类型 +  制作国家
# 选出需要用的属性：类型，国家
# df['main_genre'] = df['genre'].str.split('/').str.get(0)
# df['main_place'] = df['place'].str.split('/').str.get(0)
# df1 = df[['name', 'main_genre', 'main_place']]
# var1 = df1.groupby(['main_genre', 'main_place']).count()
# var1 = var1[var1['name'] > 50]
# var1.columns = ['电影数量']
# var1_unstack = var1.unstack().plot(kind='bar', stacked=True, grid=True, colormap='tab20',figsize=(10,5))
#
# #var1_unstack.plot(kind='bar', stacked=True, grid=True, colormap='tab20')
# plt.title('电影类型分布以及电影的制作国家/制作地区')
# plt.xlabel('电影类型')
# plt.xticks(rotation=360)
# plt.ylabel('电影数')
# plt.show()

# ----------------------------------









