from flask import Blueprint, json, request, jsonify, make_response
from model.usuario import Usuario
from db.mongo_connection import Connection
from extra.utils import Util
from db.mysql_connection import Mysql

usuario_bp = Blueprint('usuario', __name__, url_prefix='/api/usuarios')
db = Connection()


class UsuarioController:
    
    def __init__(self, app):
        app.register_blueprint(usuario_bp)
    
    @usuario_bp.route('', methods=['POST'])
    def criar_usuario():
        try:
            
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"})
            
            dados = request.get_json()
            nome_completo = dados.get('nome', '').strip()
            
            if not nome_completo:
                return jsonify({'erro': 'Nome é obrigatório'}), 400
            
            partes_nome = nome_completo.split()
            if len(partes_nome) < 2:
                return jsonify({'erro': 'Forneça pelo menos primeiro e último nome'}), 400
            
            primeiro_nome = partes_nome[0].lower()
            ultimo_nome = partes_nome[-1].lower()
            nome_usuario = f"{primeiro_nome}.{ultimo_nome}"
            
            db.get_connection().find(nome_completo)
            
            usuario = Usuario(
                nome=nome_completo,
                usuario=nome_usuario,
                email=dados.get('email'),
                senha=dados.get('senha'),
                telefone=dados.get('telefone'),
                status=True,
                tipo=dados.get('tipo')
            )
            
            resultado = db.inserir('usuarios', usuario.__dict__)
            return jsonify({'mensagem': 'Usuário criado', 'id': str(resultado)}), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('', methods=['GET'])
    def listar_usuarios():
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"})
            
            usuarios = db.buscar_todos("usuarios") # Mysql.execute("SELECT id_usuario, nome, email, telefone, status, usuario FROM usuarios")
            # print(usuarios)
            return jsonify(usuarios), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('/<id>', methods=['GET'])
    def obter_usuario(id):
        try:
            
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"})
            
            usuario = db.buscar_por_id('usuarios', id)
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            return jsonify(usuario), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('/<id>', methods=['PUT'])
    def atualizar_usuario(id):
        try:
            
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"})
            
            dados = request.get_json()
            resultado = db.atualizar('usuarios', id, dados)
            if resultado.modified_count == 0:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            return jsonify({'mensagem': 'Usuário atualizado'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('/<id>', methods=['DELETE'])
    def deletar_usuario(id):
        try:
            
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"})
            
            resultado = db.deletar('usuarios', id)
            if resultado.deleted_count == 0:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            return jsonify({'mensagem': 'Usuário deletado'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('/login', methods = ['POST'])
    def login():
        try:
            credenciais = request.get_json()
            
            if not credenciais.get('nome_usuario', '').strip():
                return jsonify({"aviso": "Usuário deve ser informado"})
            
            if not credenciais.get('senha_usuario', '').strip():
                return jsonify({"aviso": "Senha deve ser informada"})
            
            usuario_encontrado = db.get_connection().find_one({"_usuario": credenciais.get('nome_usuario', '').strip()})
            
            if not usuario_encontrado:
                return jsonify({"erro": "Usuário inválido"})
            else:
                if usuario_encontrado.get('_senha') == credenciais.get('senha_usuario', '').strip():
                    id_sessao = Util.registerSessionInDatabase(usuario_encontrado.get('_id'))
                    usuario_cookie = {
                        "id": str(id_sessao),
                        "nome": usuario_encontrado.get('_nome'),
                        "tipo": usuario_encontrado.get('_tipo')  # gestor ou funcionario
                    }

                    resp = make_response({"mensagem": "Login realizado com sucesso"})
                    
                    resp.set_cookie(
                        'user-info',
                        json.dumps(usuario_cookie),  # transforma em string
                        httponly=True,               # mais seguro (não acessível via JS)
                        secure=False,               # True se usar HTTPS
                        samesite='Lax' 
                    )

                    return resp
                else:
                    return jsonify({"erro": "Senha inválida"})
            
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
        
        
    @usuario_bp.route('/validar', methods = ['GET'])
    def validaSessao():
        if not Util.validSession(Util.getUserSession(request)):
            return jsonify({"erro": "Sessão inválida"}), 403
        else:
            return jsonify({"sucesso": "Sessão válida"}),200