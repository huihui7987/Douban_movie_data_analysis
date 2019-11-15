import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import LabelEncoder
# 这个文件主要用于深层的数据清洗，清洗后的数据可以直接用于机器学习
# 在清洗前，用df.info()查看一下缺失值缺失情况




def machine_preprocessing(df):

    # 工作1：
    # 把评分人数小于1000的电影删除
    # 电影时长小于40分钟的删除
    df = df[df['rating_people'] > 1000]
    df = df[df['movietime'] > 40]



    df['director'].fillna(value='无',inplace=True)
    #-----------------------

    # 工作2
    # 除演员外，一切多值文本转单值文本
    # 演员留下三个，类型留两个，国家留一个
    # 数量太少的不要

    # 演员，类型，国家处理 --------------------------------------------
    # 如果没有第二演员，就用第一演员来填充
    actor_stats = df['actor'].str.split('/', expand=True)
    actor_stats = actor_stats[[0, 1]]
    actor_stats.columns = ['main_actor', 'second_actor']
    actor_stats['second_actor'].fillna(actor_stats['main_actor'], inplace=True)

    # 如果没有第二类型，就用第一类型来填充
    genre_stats = df['genre'].str.split('/', expand=True)
    genre_stats = genre_stats[[0, 1]]
    genre_stats.columns = ['main_genre', 'second_genre']
    genre_stats['second_genre'].fillna(genre_stats['main_genre'], inplace=True)


    df.dropna(axis=0, inplace=True, subset=['director'])

    # 国家，语言只留下一个
    df['main_country'] = df['place'].str.split('/').str.get(0)
    df['main_language'] = df['language'].str.split('/').str.get(0)

    df[['main_genre', 'second_genre']] = genre_stats
    df[['main_actor', 'second_actor']] = actor_stats
    df.drop(['movie_url', 'writer', 'actor', 'place', 'language', 'genre'], axis=1,inplace=True)

    # -------------------------
    df['movietime'] = df['movietime'].astype(np.int64)
    return df


df = pd.read_csv('txtdata\movie_timeout.txt')
df = machine_preprocessing(df)
df.to_csv('txtdata\movie_timeout.txt', index=False)







