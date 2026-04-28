from flask import json, make_response, jsonify
from datetime import datetime, timedelta, timezone
from db.mysql_connection import Mysql

class Util:
    
    @staticmethod
    def getUserSession(request):
        cookie_content = request.cookies.get('user-info')
        if not cookie_content:
            return None
        try:
            return json.loads(cookie_content)
        except (json.JSONDecodeError, TypeError):
            return None
    
    @staticmethod
    def validSession(session):
        if not session or "id" not in session:
            return False
        
        sql = "SELECT expiracao FROM sessao WHERE id = %s"
        resumos = Mysql.execute(sql, (session.get("id"),))
        
        if not resumos:
            return False
            
        sessao_usuario = resumos[0]
        data_expiracao = sessao_usuario.get("expiracao")
        
        # O MySQL Connector costuma retornar objetos datetime
        # Se vier como string, precisará de um strptime
        agora = datetime.now() 
        
        if data_expiracao and agora > data_expiracao:
            return False
        
        return True 
    
    @staticmethod
    def registerSessionInDatabase(user_id):
        expiracao = datetime.now() + timedelta(minutes=90)
        sql = "INSERT INTO sessao (id_usuario, expiracao) VALUES (%s, %s)"
        return Mysql.execute(sql, (user_id, expiracao))
        
    @staticmethod
    def destroySession():
        resp = make_response(jsonify({"mensagem": "Logout realizado"}))
        resp.delete_cookie('user-info')
        return resp