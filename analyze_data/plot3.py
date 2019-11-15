import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 生成使用TMDB数据集生成的，研究收益的图

plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)
movies = pd.read_csv('txtdata/tmdb_clean.csv')
#print(movies.info())
need = movies[['id','title','budget', 'revenue', 'genres', 'cast', 'crew', 'production_companies','runtime']].copy()
need = need[(need['budget'] != 0) & (need['revenue'] != 0)]
need['rev/bud'] = need['revenue'] / need['budget']

need['rev/bud'] = need['rev/bud'].round(2)

need['genres'] = need['genres'].str.split('/').str.get(0)
need['cast'] = need['cast'].str.split('/').str.get(0)
need['crew'] = need['crew'].str.split('/').str.get(0)
need['production_companies'] = need['production_companies'].str.split('/').str.get(0)
def make_pie(count_series):
    pie_series = pd.Series()
    pie_series.loc['热门公司占比'] = count_series[count_series > 50].sum()
    pie_series.loc['其他公司占比'] = count_series[count_series < 50].sum()
    print(pie_series)
    pie_series.name = ''
    pie_series.plot(kind='pie', autopct='%1.1f%%', legend=False)
    plt.title('公司统计')
    plt.show()

# 亏的
deficit = need[need['rev/bud'] < 1].copy()
gain = need[need['rev/bud'] > 1].copy()
max_gain = need[need['rev/bud'] > 2].copy()
max_small_gain = need[need['rev/bud'] > 10].copy()
max_big_gain = need[need['rev/bud'] > 50].copy()

max_gain_by_revenue = need[need['revenue'] > 100000000].copy()
deficit['rev/bud'] = deficit['rev/bud'].round(2)
gain['rev/bud'] = np.ceil(gain['rev/bud'])
# 亏的764部，赚的2420部

# 按性价比来分析
# 高收益，低投资的是剧情类，喜剧类，恐怖类电影
# 这三类电影在投资低的情况下有可能能获得丰收的回报
# 没有一部预算超千万，但是得到了超过50倍的回报
# max_big_gain = need[need['rev/bud'] > 50].copy()
# plt.figure(figsize=(10, 7))
# g = max_big_gain.groupby('genres')['id'].count()
# plt.title('投入性价比最好的电影类型')
# g.plot(kind='pie')
# plt.show()

# 按数字来分析
# 1亿票房以上的赚钱的电影里，动作片，喜剧片，冒险片最多

#print(max_gain_by_revenue[['genres', 'budget', 'revenue', 'rev/bud']].sort_values(by='revenue'))



#  1：针对员工进行的分析

# 对某些属性分开排序，发现有一定关联
# 导演和演员
# gain_director = max_gain['crew'].value_counts()
# gain_actor = max_gain['cast'].value_counts()
# make_pie(gain_actor)
#-------------------

# # 尝试不同的组合：导演 + 类型 ； 演员 + 类型 ； 导演 + 演员 + 类型
# actor_plus_genre = max_gain.groupby(['cast'])['id'].count()
# director_plus_genre = max_gain.groupby(['crew']).size()
#
#
# actor_plus_director_plus_genre = gain.groupby(['cast', 'crew'])['id'].count()




# 2：针对公司进行的分析

company_group = gain.groupby(['production_companies'])['id'].count()
company_plus_genres = company_group.sort_values()
company_group = max_gain['production_companies'].value_counts()

make_pie(company_group)

# # 3：针对关键词进行的分析,（没啥规律）
#
# keywords_all = gain['keywords'].copy()
# keywords_all.dropna(inplace=True)
# keywords_dict = {}
#
# for row in keywords_all:
#     row_list = row.split('/')
#     for keyword in row_list:
#         if keyword in keywords_dict:
#             keywords_dict[keyword] += 1
#         else:
#             keywords_dict[keyword] = 1
#
# keywords_dict = sorted(keywords_dict.items(), key=lambda item: item[1],reverse=True)
#
#

# 4 针对电影时长的分析
# 电影时长分布图(直方图)
# runtime = max_gain['runtime']
# runtime = runtime.dropna().astype(np.int64)
# plt.hist(runtime, bins=14, range=(50, 200), color='steelblue',edgecolor='k')
# plt.xticks(np.arange(50, 200, 10))
# plt.tick_params(top='off', right='off')
# plt.title('电影时长分布')
# plt.xlabel('时长(分钟)')
# plt.ylabel('电影数')
# plt.savefig('电影时长分布')
# plt.show()

