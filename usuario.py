from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados simulado de usuários
usuarios = [
    {"id": 1, "nome": "João", "email": "joao@example.com"},
    {"id": 2, "nome": "Maria", "email": "maria@example.com"},
    {"id": 3, "nome": "Pedro", "email": "pedro@example.com"},
]

# Rota para obter todos os usuários
@app.route("/usuarios", methods=["GET"])
def obter_usuarios():
    """
    Retorna uma lista de todos os usuários.
    """
    return jsonify(usuarios)

# Rota para obter um usuário específico por ID
@app.route("/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):
    """
    Retorna um usuário específico com base no ID.

    :param id: O ID do usuário a ser recuperado.
    :type id: int
    :returns: Um JSON contendo os dados do usuário ou uma mensagem de erro se o usuário não for encontrado.
    """
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        return jsonify(usuario)
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

# Rota para criar um novo usuário
@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    """
    Cria um novo usuário e o adiciona à lista de usuários.
    Espera um JSON com os campos 'nome' e 'email'.
    """
    novo_usuario = request.get_json()
    if not novo_usuario or "nome" not in novo_usuario or "email" not in novo_usuario:
        return jsonify({"mensagem": "Requisição inválida. Certifique-se de fornecer 'nome' e 'email'."}), 400
    novo_usuario["id"] = len(usuarios) + 1
    usuarios.append(novo_usuario)
    return jsonify(novo_usuario), 201

if __name__ == "__main__":
    app.run(port=5001, debug=True) # Iniciando na porta 5001