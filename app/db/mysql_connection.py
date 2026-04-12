from mysql import connector

class Mysql:
    
    @staticmethod
    def _getCon():
        return connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="epis"
        )
        
    @staticmethod
    def execute(sql):
        cursor = Mysql._getCon().cursor(dictionary=True)
        cursor.execute(sql)
        dados = cursor.fetchall()
        cursor.close()
        return dados
    
    @staticmethod
    def execute(sql, params):
        cursor = Mysql._getCon().cursor(dictionary=True)
        cursor.execute(sql, params)
        dados = cursor.fetchall()
        cursor.close()
        return dados