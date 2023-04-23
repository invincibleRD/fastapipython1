from pymongo import MongoClient


uri = "mongodb+srv://admin:Dikush@cluster0.nnh08zd.mongodb.net/?retryWrites=true&w=majority"
urilocal = "http//:localhost:27017"

client = MongoClient(uri)
