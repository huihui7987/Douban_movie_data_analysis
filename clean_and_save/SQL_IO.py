import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine


#把txt文件里的数据写进SQL里
def movie_to_sql(tablename, filename):
    # 数据库读写：---------------------
    df = pd.read_csv(filename)

    # conn = pymysql.connect(host='localhost', user='root', database='douban', use_unicode=True)

    # df1 = pd.read_sql(sql='select * from movies_data', con=conn)

    engine = create_engine('mysql+pymysql://root@localhost:3306/douban')

    df.to_sql(name=tablename, con=engine, index=True, if_exists='replace')

    # ---------------------

if __name__ == '__main__':
    movie_to_sql('movie_with_box', 'txtdata/movie_with_box.txt')
