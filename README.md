# Douban_movie_data_analysis


Introduction
-------
Graduation Project in Spring 2019  
My first Data Science Project  
  
Movie Data Collection, Cleaning, Visualization,  Prediction Machine learning Model

Special Thanks
------
Thanks to Mr. Honlan's [fullstack-data-engineer](https://github.com/Honlan/fullstack-data-engineer)  
[Honlan's Github](https://github.com/Honlan)

Development Environment
----
Anaconda  
PyCharm   
WAMPserver  

Dataset
----
Douban Movie Dataset（By Web Crawler）   
TMDB 5000  （IMDB movie dataset）  

Technologies Used
----
Collection：Request , BeautifulSoup , Regular Expression  
Cleaning：NumPy , Pandas   
Storage： MySql , WAMPServer  
Visualization：Pandas , Matplotlib , WordCloud  
Prediction Model：Scikit-Learn  


Files Description
----

`getdata/get_douban.py `  
`getdata/get_movie_info.py ` 
Obtained the movie name and details page link from Douban API  
Used BeautifulSoup and regular expression to get the director, actor, genre, rating, year, country, language and other information of each movie to generate the original movie data set  
  
`getdata/txtdata`  Already collected movie data  
  
`clean_and_save/data_clean.py` Used Pandas to get the data and started data cleaning processing  
  
`clean_and_save/data_clean.py` Saved the current data set or read the data set from the database  
  
`analyze_data/plot1.py,plot2.py,plot3.py,tmdb5000.py` Used matplotlib to analyze and generate charts 
  
`clean_and_save/image` Already generate charts   
  
`machine_learning/choose_model.py`Machine Learning Preprocessing , Applied Machine Learning models , Assess accuracy  
  
`machine_learning/plot_model.py` Draw the scatter plots of the training and test data for each model  
  









背景
-------
2019年春毕业设计  
作为我数据科学的入门级项目  
希望以后有机会去学习更深级别的机器学习，深度学习的理论知识和具体应用  

功能介绍
--------
电影数据获取，数据清洗，生成图像，生成电影评分预测模型  

致谢
------
感谢张洪伦先生的[《全栈数据工程师养成攻略》](https://study.163.com/course/introduction.htm?courseId=1003520028&_trace_c_p_k2_=8b69b2c7cb8d4907ab91750cfb537e9b)  
[这是他的github](https://github.com/Honlan)

所需环境
----
anaconda  

pycharm  

WAMPserver

数据集
----
豆瓣电影数据集（爬虫获取）   
TMDB 5000  （IMDB电影数据集）  

所用技术
----
数据获取：request + BeautifulSoup + 正则表达式  
数据清洗：numpy + pandas   
数据存储： mysql + WAMP   
生成图像：pandas + matplotlib + 词云  
机器学习预测模型：scikit-learn  


文件介绍
----

`getdata/get_douban.py `  
`getdata/get_movie_info.py ` 
从豆瓣后台API获取电影名以及详情页链接，进入详情页，使用BeautifulSoup和正则表达式获取每部电影的导演，演员，类型，评分，年份，国家，语言等信息，生成原始电影数据集 
`getdata/txtdata.py`获取的电影数据  
`clean_and_save/data_clean.py`使用pandas获取电影数据集，做一系列的数据清洗处理  
`clean_and_save/data_clean.py`保存当前数据集或从数据库里读取数据集  
`analyze_data/plot1.py,plot2.py,plot3.py,tmdb5000.py`使用matplotlib库对感兴趣的问题进行分析并生成图像  
`clean_and_save/image` 生成的图像  
`machine_learning/choose_model.py`对数据集进行机器学习前的预处理，然后使用多个模型评估准确性  
`machine_learning/plot_model.py`画出每个模型训练集和测试集数据的散点图  



