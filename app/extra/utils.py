import pymongo
from flask import json
from datetime import datetime, timedelta, timezone
from model.sessao import Sessao
from bson import ObjectId

class Util:
    
    @staticmethod
    def getUserSession(request):
        return json.loads(request.cookies.get('user-info'))
    
    @staticmethod
    def validSession(session):
        print(session)
        dbAccess = Util._getDbAccessOnSessionCollection()
        sessao_usuario = dbAccess.find_one({"_id": ObjectId(session.get("id"))})
       
        print(sessao_usuario)
       
        if not sessao_usuario:
            return False  
        
        data_expiracao = sessao_usuario.get("expiracao")
        
        agora = datetime.now(tz=timezone.utc)
        
        if data_expiracao and agora > data_expiracao:
            return False
        
        return True 
    
    @staticmethod
    def registerSessionInDatabase(user_id):
        dbAccess = Util._getDbAccessOnSessionCollection()
        return dbAccess.insert_one(Sessao(user_id, datetime.now(tz=timezone.utc) + timedelta(minutes=90)).__dict__).inserted_id
        
 
    @staticmethod
    def _getDbAccessOnSessionCollection():
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["mydatabase"]
        mycol = mydb["sessao"]
        return mycol