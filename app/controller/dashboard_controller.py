from flask import Blueprint, json, request, jsonify
from extra.tipo_usuario import TipoUsuario
from extra.utils import Util
from db.mysql_connection import Mysql


dashboard_bp  = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
class DashboardController:
    
    def __init__(self, app):
        app.register_blueprint(dashboard_bp)
    
    @dashboard_bp.route('', methods=['GET'])
    def buscar_infomacoes_geral():
        user_info_cookie = request.cookies.get('user-info')
        
        if user_info_cookie is None:
            return jsonify({"erro": "Usuário não informado está tentando acessar o sistema"}), 403
        
        try:
            user_info = json.loads(user_info_cookie)
        except:
            return jsonify({"erro": "Cookie inválido"}), 400
        
        if not Util.validSession(user_info):
            return jsonify({"erro": "Sessão expirada ou inválida"}), 401

        resumos = Mysql.execute("SELECT * FROM usuarios WHERE id = %s", (user_info.get('id'),))
        
        if not resumos:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        usuario_acessando = resumos[0]
        
        if usuario_acessando.get('tipo') != TipoUsuario.GESTOR.value:
            dados = Mysql.execute("SELECT * FROM epis")
            return jsonify(dados), 200
        
        if usuario_acessando.get('tipo') == TipoUsuario.FUNCIONARIO.value:
            return jsonify(usuario_acessando), 200

        return jsonify({"mensagem": "Dados de gestor"}), 200