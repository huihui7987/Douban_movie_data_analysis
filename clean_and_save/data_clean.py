import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
# 传入一个dataframe，做以下处理：
# 1 删除重复的电影
# 2 删除多余属性
# 3 过滤掉参考价值不大的电影
# 4 缺失值处理
    # 文本属性：查询正确值，填补
    # 数值属性：使用中位数或平均数填补
# 5 属性处理
    # 去除冗余字符，转换为正确的数据类型(整数或浮点数)

def clean_data(df):
    # 1 删除重复电影
    df.drop_duplicates(inplace=True)
    # 2 删除url
    df.drop(['movie_url'], axis=1, inplace=True)
    # 3 删除没有评分人数，没有年份,没有时间的电影
    df.dropna(axis=0, subset=['rating_people', 'year','movietime'], inplace=True)

    # 4 改变年份和评分人数的类型为整型
    df['year'] = df['year'].astype(np.int64)
    df['rating_people'] = df['rating_people'].astype(np.int64)
    df['movietime'] = df['movietime'].astype(np.int64)

    # 5 电影时间，年份多余字符去掉
    # df['movietime'] = df['movietime'].str.extract('(\d+)')
    # df['year'] = df['year'].str.extract('(\d+)')


    # 6 把评分人数小于1000的电影删除
    df = df[df['rating_people'] > 1000]

    return df

if __name__ == '__main__':
    df = pd.read_csv('txtdata/1959-2019copy.txt')
    df = clean_data(df)
    df.to_csv('txtdata/1959-2019copy.txt', index=False)


