from flask import Blueprint, json, request, jsonify, make_response
from model.usuario import Usuario
from extra.utils import Util
from db.mysql_connection import Mysql
from extra.email_service import Email
import uuid

usuario_bp = Blueprint('usuario', __name__, url_prefix='/api/usuarios')

class UsuarioController:
    
    def __init__(self, app):
        app.register_blueprint(usuario_bp)
    
    @usuario_bp.route('', methods=['POST'])
    def criar_usuario():
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"}), 401
            
            dados = request.get_json()
            nome_completo = dados.get('nome', '').strip()
            
            if not nome_completo:
                return jsonify({'erro': 'Nome é obrigatório'}), 400
            
            partes_nome = nome_completo.split()
            if len(partes_nome) < 2:
                return jsonify({'erro': 'Forneça pelo menos primeiro e último nome'}), 400
            
            nome_usuario = f"{partes_nome[0].lower()}.{partes_nome[-1].lower()}"
            senha_gerada = uuid.uuid4().hex
            
            sql = """
                INSERT INTO usuarios (nome, usuario, email, senha, telefone, status, tipo, primeiro_acesso) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                nome_completo,
                nome_usuario,
                dados.get('email'),
                senha_gerada,
                dados.get('telefone'),
                True,
                dados.get('tipo'),
                True
            )
            
            id_gerado = Mysql.execute(sql, params)
            Email.enviar_email_acesso(nome_completo, nome_usuario, senha_gerada, dados.get('email'))
            
            return jsonify({'mensagem': 'Usuário criado', 'id': id_gerado}), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @usuario_bp.route('', methods=['GET'])
    def listar_usuarios():
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"}), 401
            
            usuarios = Mysql.execute("SELECT id, nome, email, telefone, status, usuario, tipo FROM usuarios")
            return jsonify(usuarios), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @usuario_bp.route('/<id>', methods=['GET'])
    def obter_usuario(id):
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"}), 401
            
            resultado = Mysql.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            if not resultado:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
                
            return jsonify(resultado[0]), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @usuario_bp.route('/<id>', methods=['PUT'])
    def atualizar_usuario(id):
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"}), 401
            
            dados = request.get_json()
            colunas = ", ".join([f"{k} = %s" for k in dados.keys()])
            valores = list(dados.values())
            valores.append(id)
            
            sql = f"UPDATE usuarios SET {colunas} WHERE id = %s"
            Mysql.execute(sql, tuple(valores))
            
            return jsonify({'mensagem': 'Usuário atualizado'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @usuario_bp.route('/<id>', methods=['DELETE'])
    def deletar_usuario(id):
        try:
            if not Util.validSession(Util.getUserSession(request)):
                return jsonify({"erro": "Usuário não logado"}), 401
            
            Mysql.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            return jsonify({'mensagem': 'Usuário deletado'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @usuario_bp.route('/login', methods=['POST'])
    def login():
        try:
            credenciais = request.get_json()
            
            nome_usuario = credenciais.get('nome_usuario', '').strip()
            senha_usuario = credenciais.get('senha_usuario', '').strip()

            if not nome_usuario:
                return jsonify({"erro": "Usuário deve ser informado"}), 400
            
            if not senha_usuario:
                return jsonify({"erro": "Senha deve ser informada"}), 400
            
            sql = "SELECT * FROM usuarios WHERE usuario = %s"
            resultados = Mysql.execute(sql, (nome_usuario,))
            
            if not resultados:
                return jsonify({"erro": "Usuário inválido"}), 401
                
            usuario_encontrado = resultados[0]
            
            if usuario_encontrado.get('senha') == senha_usuario:
                
                id_sessao = Util.registerSessionInDatabase(usuario_encontrado.get('id'))
                
                usuario_cookie = {
                    "id": str(id_sessao),
                    "nome": usuario_encontrado.get('nome'),
                    "tipo": usuario_encontrado.get('tipo')
                }

                if usuario_encontrado.get('primeiro_acesso'):
                    return jsonify({
                        "aviso": "Primeiro acesso, altere a senha por segurança",
                        "id_usuario": usuario_encontrado.get('id')
                    }), 200
                
                resp = make_response(jsonify({"mensagem": "Login realizado com sucesso"}))
                
                resp.set_cookie(
                    'user-info',
                    json.dumps(usuario_cookie),
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )

                return resp
            else:
                return jsonify({"erro": "Senha inválida"}), 401
            
        except Exception as e:
            print(f"Erro no login: {e}")
            return jsonify({'erro': "Erro interno no servidor"}), 500
        
    
    @usuario_bp.route('/alterar-senha', methods=['POST'])
    def alterar_senha():
        dados_troca = request.get_json()
        
        try:
            sql = "UPDATE usuarios SET senha = %s, primeiro_acesso = %s WHERE usuario = %s"
            Mysql.execute(sql, (
                dados_troca.get("senha_nova"),
                False,
                dados_troca.get("usuario")
            ))
            
            return jsonify({'sucesso': 'Senha alterada com sucesso'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @usuario_bp.route('/validar', methods=['GET'])
    def valida_sessao():
        session_data = Util.getUserSession(request)
        
        if session_data is None:
            return jsonify({"erro": "Nenhuma sessão encontrada"}), 401

        if not Util.validSession(session_data):
            return jsonify({"erro": "Sessão inválida ou expirada"}), 403
        
        return jsonify({"sucesso": "Sessão válida"}), 200

    @usuario_bp.route('/logout', methods=['GET'])
    def do_logout():
        
        session_data = Util.getUserSession(request)
        
        Mysql.execute("DELETE FROM sessao WHERE id = %s", (session_data.get("id"),))
        
        return Util.destroySession()