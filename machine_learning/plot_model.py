# 机器学习的画图
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
plt.style.use('ggplot')

def make_train_text_by_rate(movie):
    # 第一步，分出训练集和测试集
    # 分层依据：评分
    # 先把10分制改成五分制，减少分层数量
    movie['rate_cat'] = np.ceil(movie['rate'] / 2)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=58)
    for train_index, test_index in split.split(movie, movie["rate_cat"]):
        strat_train_set = movie.loc[train_index]
        strat_test_set = movie.loc[test_index]
    return strat_train_set, strat_test_set

def display_scores(scores):
    print('---------------------')
    print('scores:', scores)
    print('mean:', scores.mean())
    print('Standard Deviation:', scores.std())
    print('---------------------')

def score_the_module(model):
    # 验证模型
    scores = cross_val_score(model, movie_prepared, movie_labels,
                             scoring='neg_mean_squared_error', cv=10)
    rmse_scores = np.sqrt(-scores)
    display_scores(rmse_scores)



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
        ('cat_all', OrdinalEncoder(), cat_attribs_all),
        #('cat_simple', OrdinalEncoder(), cat_attribs_simple),
        #("cat_one_hot", OneHotEncoder(), cat_attribs_simple),
    ])

movie_prepared = full_pipeline.fit_transform(movie)
print(movie_prepared.shape)

def plot_picture(model,ax,title):
    # 准备画图数据
    train_real = strat_train_set['rate'].copy()

    test_x = strat_test_set.drop('rate', axis=1)
    test_real = strat_test_set['rate'].copy()
    test_x_prepared = full_pipeline.transform(test_x)
    test_predict = model.predict(test_x_prepared)

    #画散点图观察模型性能
    #plt.figure(figsize=(7, 7))
    train_predict = model.predict(movie_prepared)
    ax.set_xlabel('真实值')
    ax.set_ylabel('预测值')
    ax.scatter(train_real, train_predict, c='g', s=35, alpha=0.5, marker='o', label='训练集数据')
    ax.scatter(test_real, test_predict, c='b', s=35, alpha=0.5, marker='v', label='测试集数据')
    ax.set_title(title)
    ax.legend()
    #plt.show()


# 导入模型
# lin_reg = joblib.load('my_lin_reg.pkl')
# tree_reg = joblib.load('my_tree_reg.pkl')
# forest_reg = joblib.load('my_forest_reg.pkl')
# kmeans_reg = joblib.load('my_kmeans_reg.pkl')

#forest_final_reg = joblib.load('my_forest_final_reg.pkl')

forest_reg = RandomForestRegressor()
param_grid = [
    {"n_estimators": [3, 10, 30], 'max_features':[2, 4, 6]},
    {'bootstrap': [False], 'n_estimators':[3, 30], 'max_features':[2, 3, 4]},
]

grid_search = GridSearchCV(forest_reg, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(movie_prepared, movie_labels)

final_reg_ordi = grid_search.best_estimator_
score_the_module(final_reg_ordi)
joblib.dump(final_reg_ordi, 'my_forest_final_reg_odi.pkl')

#----------以下是检验模型
# movie_test = pd.read_csv('txtdata/movie_test.txt')
# x_test = movie_test.drop('rate', axis=1)
# y_test = movie_test['rate'].copy()
# x_test_prepared = full_pipeline.transform(x_test)
# y_predict = final_reg_ordi.predict(x_test_prepared)
# print(y_test.values)
# print(y_predict)
# score_the_module(forest_reg)
# score_the_module(final_reg_ordi)

# ---------------------------------------

# fig, ax = plt.subplots(2,2,figsize=(10,10))
#
# plot_picture(lin_reg, ax[0][0], '线性回归模型')
# plot_picture(tree_reg, ax[0][1], '决策树模型')
# plot_picture(kmeans_reg, ax[1][0], 'K均值聚类模型')
# plot_picture(forest_reg, ax[1][1], '随机森林模型')

# fig, ax = plt.subplots(figsize=(5,5))
# plot_picture(forest_final_reg, ax, '随机森林模型（参数调整后）')
# plt.show()


