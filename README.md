# Douban_movie_data_analysis

介绍
-------
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

getdata/get_douban.py + getdata/get_movie_info.py  
从豆瓣后台API获取电影名以及详情页链接，进入详情页，使用BeautifulSoup和正则表达式获取每部电影的导演，演员，类型，评分，年份，国家，语言等信息，生成原始电影数据集 
getdata/txtdata：获取的电影数据  
clean_and_save/data_clean.py：使用pandas获取电影数据集，做一系列的数据清洗处理  
clean_and_save/data_clean.py：保存当前数据集或从数据库里读取数据集  
analyze_data/plot1,plot2,plot3,tmdb5000,：使用matplotlib库对感兴趣的问题进行分析并生成图像  
clean_and_save/image： 生成的图像  
machine_learning/choose_model：对数据集进行机器学习前的预处理，然后使用多个模型评估准确性  
machine_learning/plot_model：画出每个模型训练集和测试集数据的散点图  



