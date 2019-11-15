# 只针对随机森林模型
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.preprocessing import Imputer,LabelEncoder,OrdinalEncoder,CategoricalEncoder,LabelBinarizer,OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV


df = pd.read_csv('txtdata/1959-2019.txt')

plt.rcParams['font.sans-serif'] = ['SimHei']

plt.rcParams['axes.unicode_minus'] = False

def display_scores(scores):
    print('---------------------')
    print('scores:', scores)
    print('mean:', scores.mean())
    print('Standard Deviation:', scores.std())
    print('---------------------')

def score_the_module_rmse(model):
    # 验证模型
    scores = cross_val_score(model, movie_prepared, movie_labels,
                             scoring='neg_mean_squared_error', cv=10)
    rmse_scores = np.sqrt(-scores)
    display_scores(rmse_scores)

def score_the_module_r2(model):
    # 验证模型
    scores = cross_val_score(model, movie_prepared, movie_labels,
                             scoring='r2', cv=10)
    display_scores(scores)

def make_train_text_by_year(movie):
    movie['year_cat'] = movie['year']
    movie['year_cat'].where(movie['year_cat'] < 2010, 2020, inplace=True)
    movie['year_cat'].where((movie['year_cat'] == 2020) | (movie['year_cat'] < 2000), 2010, inplace=True)
    movie['year_cat'].where(movie['year_cat'] > 2000, 2000, inplace=True)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=35)
    for train_index, test_index in split.split(movie, movie["year_cat"]):
       strat_train_set = movie.loc[train_index]
       strat_test_set = movie.loc[test_index]
    return strat_train_set,strat_test_set

def make_train_text_by_rate(movie):
    # 第一步，分出训练集和测试集
    # 分层依据：评分
    # 先把10分制改成五分制，减少分层数量
    movie['rate_cat'] = np.ceil(movie['rate'] / 1)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=58)
    for train_index, test_index in split.split(movie, movie["rate_cat"]):
        strat_train_set = movie.loc[train_index]
        strat_test_set = movie.loc[test_index]
    return strat_train_set, strat_test_set



strat_train_set, strat_test_set = make_train_text_by_rate(df)

movie = strat_train_set.drop(['rate', 'rate_cat'], axis=1)
movie_labels = strat_train_set['rate'].copy()

num_attribs = ['rating_people', 'year', 'movietime']
cat_attribs_all = ['director', 'main_country', 'main_language',
                   'main_genre', 'second_genre',
                   'main_actor', 'second_actor']
cat_attribs_simple = ['main_country',
                        'main_genre', 'second_genre']

num_pipeline = Pipeline([
    ('imputer', Imputer(strategy='median')),
    ('std_scalar', StandardScaler()),
])


full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        #('cat_all', OrdinalEncoder(), cat_attribs_all),
        #('cat_simple', OrdinalEncoder(), cat_attribs_simple),
        ("cat_one_hot", OneHotEncoder(), cat_attribs_simple),
    ])

movie_prepared = full_pipeline.fit_transform(movie)
print(movie_prepared.shape)

# forest_reg = RandomForestRegressor()
# param_grid = [
#     {"n_estimators": [3, 10, 30], 'max_features':[2, 4, 6]},
#     {'bootstrap': [False], 'n_estimators':[3, 30], 'max_features':[2, 3, 4]},
# ]
#
# grid_search = GridSearchCV(forest_reg, param_grid, cv=5, scoring='neg_mean_squared_error')
#
# grid_search.fit(movie_prepared, movie_labels)
#
# final_reg = grid_search.best_estimator_

forest_reg = joblib.load('model/my_final_reg.pkl')
score_the_module_rmse(forest_reg)
score_the_module_r2(forest_reg)
# score_the_module(final_reg)
# joblib.dump(final_reg, 'my_forest_final_reg.pkl')

# 画散点图
# # 准备画图数据
# x_test = strat_test_set.drop('rate', axis=1)
# y_test = strat_test_set['rate'].copy()
# x_test_prepared = full_pipeline.transform(x_test)
# test_predict = forest_reg.predict(x_test_prepared)
#
# #画散点图观察模型性能
# plt.figure(figsize=(7, 7))
# train_predict = forest_reg.predict(movie_prepared)
# plt.xlabel('预测值')
# plt.ylabel('预测值与真实值之差')
# plt.scatter(train_predict, train_predict, c='g', s=35, alpha=0.5, marker='o', label='训练集数据')
# plt.scatter(test_predict, test_predict, c='b', s=35, alpha=0.5, marker='v', label='测试集数据')
# plt.legend()
# plt.show()

#----------以下是检验模型
# movie_test = df2[:10]
# x_test = movie_test.drop('rate', axis=1)
# y_test = movie_test['rate'].copy()
# x_test_prepared = full_pipeline.transform(x_test)
# y_predict = forest_reg.predict(x_test_prepared)
# print(y_test.values)
# print(y_predict)

# final_mse = mean_squared_error(y_test, y_predict)
# final_rmse = np.sqrt(final_mse)
# print(final_rmse)


# 画散点图观察模型性能
# rate_predict = forest_reg.predict(movie_prepared)
# plt.scatter(rate_predict, movie_labels-rate_predict, c='b', s=35, alpha=0.5)
# plt.show()

# -----------------------------