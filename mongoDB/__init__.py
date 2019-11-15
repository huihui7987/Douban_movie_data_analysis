import pymongo

#和数据库连接
client = pymongo.MongoClient(host='localhost', port=27017)

#访问“test”数据库
db = client.test
print(db)

# 访问‘movie’ 集合
collection = db.movie

# 插入一条数据
item = {
    'name': 'abc',
    'actor': 'zhang san',
}

#result = collection.insert_one(item)
#返回一个独一无二的ID值
#print(result)

items =[{

    'name': 'abcd',
    'actor': 'li si',
},
    {

        'name': 'abcde',
        'actor': 'wang wu',
    },
]

# result = collection.insert_many(items)
# print(result)

#寻找数据
print(collection.find_one())
print(collection.find_one({'actor':'wang wu'}))