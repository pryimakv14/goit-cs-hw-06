import pymongo
from datetime import datetime


collection_name = "user_message"
uri = "mongodb://mongo:example@mongo"
db_name = "mydb"


class MongoDBManager:
    def __init__(self):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

    def add_record(self, record) -> bool:
        collection = self.db[collection_name]

        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)

        record['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        result = None
        try:
            result = collection.insert_one(record)
        except:
            return False 

        return True if result.inserted_id else False
    

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://mongo:example@mongo")
    db = client['mydb']

    collection = db[collection_name]

    documents = collection.find()
    print("Виведення всіх документів колекції:")
    for document in documents:
        print(document)
