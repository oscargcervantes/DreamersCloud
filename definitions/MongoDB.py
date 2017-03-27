# -*- coding: utf-8 -*-
from pymongo import MongoClient
import urllib
        
def connect(server,port,user,password,db,collection_name):
    uri = "mongodb://" + str(user) + ":" + urllib.quote(password) + "@" + str(server) + "/" + str(db)
    mongoClient = MongoClient(uri)
    #mongoClient = MongoClient(server,port)
    db = mongoClient[str(db)]
    collection = db[str(collection_name)]
    return collection
