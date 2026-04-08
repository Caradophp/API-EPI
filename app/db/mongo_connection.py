import pymongo
from bson import ObjectId

class Connection:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]

    def get_collection(self, nome_collection):
        return self.db[nome_collection]

    def inserir(self, nome_collection, documento):
        collection = self.get_collection(nome_collection)
        return collection.insert_one(documento).inserted_id

    def deletar(self, nome_collection, id):
        collection = self.get_collection(nome_collection)
        return collection.delete_one({"_id": ObjectId(id)}).deleted_count

    def buscar_todos(self, nome_collection):
        collection = self.get_collection(nome_collection)
        dados = list(collection.find())

        for d in dados:
            d["_id"] = str(d["_id"])

        return dados

    def buscar_por_id(self, nome_collection, id):
        collection = self.get_collection(nome_collection)
        dado = collection.find_one({"_id": ObjectId(id)})

        if dado:
            dado["_id"] = str(dado["_id"])

        return dado

    def atualizar(self, nome_collection, id, documento):
        collection = self.get_collection(nome_collection)
        return collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": documento}
        ).modified_count
    
    def get_connection(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["mydatabase"]
        mycol = mydb["usuarios"]
        return mycol