from flask import Blueprint, json, request, jsonify
from db.mongo_connection import Connection
from extra.tipo_usuario import TipoUsuario


dashboard_bp  = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
db = Connection()

class DashboardController:
    
    def __init__(self, app):
        app.register_blueprint(dashboard_bp)
    
    @dashboard_bp.route('', methods = ['GET'])
    def buscar_infomacoes_geral():
        user_info = request.cookies.get('user-info')
        
        if user_info == None:
            return jsonify({"erro": "Usuário não informado está tentando acessar o sistema"}), 403
        
        try:
            user_info = json.loads(user_info)
        except:
            return jsonify({"erro": "Cookie inválido"}), 400
        
        usuario_acessando = db.buscar_por_id('usuarios', user_info.get('id'))
        
        if usuario_acessando.get('tipo') != TipoUsuario.GESTOR.value:
            if usuario_acessando.get('tipo') == TipoUsuario.FUNCIONARIO.value:
                return jsonify(usuario_acessando), 200
            
        dados = db.buscar_todos('usuarios')
        return jsonify(dados), 200