import pymongo



link_To_db=pymongo.MongoClient("mongodb://admin:123456@203.64.128.65:27017/")

use_db=link_To_db['admin']
use_col=use_db['Drip_service']
x = use_col.insert_one({"test":"123"})
