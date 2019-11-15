# 得到了数据，开始机器学习方面的处理
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import Imputer,LabelEncoder,OrdinalEncoder,CategoricalEncoder,LabelBinarizer,OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

df = pd.read_csv('1959-2019.txt')


# 一共12个属性，其中名字不要，就是11个属性
# rate，rating_people,year,movietime   一共4个属于数值属性
# main_country ，main_language  ，main_genre  ，second_genre
# director，main_actor ，second_actor ，一共7个属于文本属性

# 数值属性只需要标准化
# 文本属性只需要编码
def display_scores(scores):
    print('---------------------')
    print('scores:', scores)
    print('mean:', scores.mean())
    print('Standard Deviation:', scores.std())
    print('---------------------')

def make_train_text(movie):
    # 第一步，分出训练集和测试集
    # 分层依据：评分
    # 先把10分制改成五分制，减少分层数量
    movie['rate_cat'] = np.ceil(movie['rate'] / 2)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=58)
    for train_index, test_index in split.split(movie, movie["rate_cat"]):
        strat_train_set = movie.loc[train_index]
        strat_test_set = movie.loc[test_index]
    return strat_train_set, strat_test_set

def score_the_module(model):
    # 验证模型
    scores = cross_val_score(model, movie_prepared, movie_labels,
                             scoring='neg_mean_squared_error', cv=10)
    rmse_scores = np.sqrt(-scores)
    display_scores(rmse_scores)


# 第二步：数值数据标准化，文本数据编码

# 演员和导演太多，用普通编码
# 类型，国家
strat_train_set, strat_test_set = make_train_text(df)

movie = strat_train_set.drop(['rate', 'rate_cat'], axis=1)
movie_labels = strat_train_set['rate'].copy()

num_attribs = ['rating_people', 'year', 'movietime']
cat_attribs_all = ['director', 'main_country', 'main_language',
                   'main_genre', 'second_genre',
                   'main_actor', 'second_actor']
# 搞一个值比较少的文本
cat_attribs_simple = ['main_country',
                        'main_genre', 'second_genre']



# 数值型数据管道
num_pipeline = Pipeline([
    ('imputer', Imputer(strategy='median')),
    ('std_scalar', StandardScaler()),
])

# 管道结合

full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        #('cat_all', OrdinalEncoder(), cat_attribs_all),
        #('cat_simple', OrdinalEncoder(), cat_attribs_simple),
        ("cat_one_hot", OneHotEncoder(), cat_attribs_simple),
    ])


movie_prepared = full_pipeline.fit_transform(movie)
print(movie_prepared.shape)

# 建立线性回归模型
lin_reg = LinearRegression()

lin_reg.fit(movie_prepared, movie_labels)

# 决策树
tree_reg = DecisionTreeRegressor()
tree_reg.fit(movie_prepared, movie_labels)

# 更换第三个模型：随机森林模型
forest_reg = RandomForestRegressor()
forest_reg.fit(movie_prepared, movie_labels)


# 第四个模型：K近邻
kmeans_reg = KNeighborsRegressor()
kmeans_reg.fit(movie_prepared, movie_labels)
#
# # 第五个模型：岭回归（官方教程推荐SVR和岭回归）
# ridge_reg = Ridge(alpha=1.0)
# ridge_reg.fit(movie_prepared, movie_labels)

#第六个模型：线性SVR
# svr_reg = SVR(kernel='linear')
# svr_reg.fit(movie_prepared, movie_labels)
# svr_reg = joblib.load('my_svr_lin.pkl')
# score_the_module(svr_reg)
# movie_predictions = svr_reg.predict(movie_prepared)
# svr_mse = mean_squared_error(movie_labels, movie_predictions)
# svr_rmse = np.sqrt(svr_mse)
# print(svr_rmse)
#joblib.dump(svr_reg, 'my_svr_lin.pkl')


# 第七个模型： rbf SVR
# svr_rbf_reg = SVR(kernel='rbf')
# svr_rbf_reg.fit(movie_prepared, movie_labels)
# svr_rbf_reg = joblib.load('my_svr_rbf.pkl')
# score_the_module(svr_rbf_reg)
# movie_predictions = svr_rbf_reg.predict(movie_prepared)
# svr_rbf_mse = mean_squared_error(movie_labels, movie_predictions)
# svr_rbf_rmse = np.sqrt(svr_rbf_mse)
# print(svr_rbf_rmse)
#joblib.dump(svr_rbf_reg, 'my_svr_rbf.pkl')

# 验证线性模型
score_the_module(lin_reg)
# 验证决策树模型
score_the_module(tree_reg)
#验证随机森林模型
score_the_module(forest_reg)
# 验证K近邻模型
score_the_module(kmeans_reg)
# # 验证岭回归模型
# score_the_module(ridge_reg)
# 验证线性SVR
#score_the_module(svr_reg)
# 验证kbf SVR
#score_the_module(svr_rbf_reg)



# # 保存模型
# joblib.dump(lin_reg, 'my_lin_reg.pkl')
# joblib.dump(tree_reg, 'my_tree_reg.pkl')
# joblib.dump(forest_reg, 'my_forest_reg.pkl')
# joblib.dump(kmeans_reg, 'my_kmeans_reg.pkl')

# 使用测试集检测模型准确程度
# x_test_prepared = full_pipeline.transform(x_test)
# y_predict = forest_reg.predict(x_test_prepared)
# final_mse = mean_squared_error(y_test, y_predict)
# final_rmse = np.sqrt(final_mse)
# print(final_rmse)

# -----------------------------