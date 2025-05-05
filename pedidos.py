from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Banco de dados simulado de pedidos
pedidos = [
    {"id": 1, "usuario_id": 1, "produto_id": 2, "quantidade": 3},
    {"id": 2, "usuario_id": 2, "produto_id": 1, "quantidade": 1},
]

# Endereços dos outros microsserviços
USUARIOS_SERVICE_URL = "http://localhost:5001/usuarios"
PRODUTOS_SERVICE_URL = "http://localhost:5002/produtos"

# Rota para obter todos os pedidos
@app.route("/pedidos", methods=["GET"])
def obter_pedidos():
    """
    Retorna uma lista de todos os pedidos.
    Enriquece os dados do pedido com informações de usuário e produto dos outros microsserviços.
    """
    pedidos_detalhados = []
    for pedido in pedidos:
        try:
            # Obtém o usuário do serviço de usuários
            usuario_response = requests.get(f"{USUARIOS_SERVICE_URL}/{pedido['usuario_id']}")
            usuario_data = usuario_response.json()
            if usuario_response.status_code != 200:
                return jsonify({"mensagem": f"Erro ao obter usuário: {usuario_data['mensagem']}"}), 500

            # Obtém o produto do serviço de produtos
            produto_response = requests.get(f"{PRODUTOS_SERVICE_URL}/{pedido['produto_id']}")
            produto_data = produto_response.json()
            if produto_response.status_code != 200:
                return jsonify({"mensagem": f"Erro ao obter produto: {produto_data['mensagem']}"}), 500

            # Combina os dados
            pedido_detalhado = {
                "id": pedido["id"],
                "usuario": usuario_data,
                "produto": produto_data,
                "quantidade": pedido["quantidade"],
                "total": pedido["quantidade"] * produto_data["preco"],
            }
            pedidos_detalhados.append(pedido_detalhado)
        except requests.exceptions.ConnectionError as e:
            return jsonify({"mensagem": f"Erro ao comunicar com outros serviços: {e}"}), 500
    return jsonify(pedidos_detalhados)

# Rota para criar um novo pedido
@app.route("/pedidos", methods=["POST"])
def criar_pedido():
    """
    Cria um novo pedido. Espera um JSON com os campos 'usuario_id', 'produto_id' e 'quantidade'.
    Valida a existência do usuário e do produto nos respectivos microsserviços.
    """
    novo_pedido = request.get_json()
    if not novo_pedido or "usuario_id" not in novo_pedido or "produto_id" not in novo_pedido or "quantidade" not in novo_pedido:
        return jsonify({"mensagem": "Requisição inválida. Certifique-se de fornecer 'usuario_id', 'produto_id' e 'quantidade'."}), 400

    try:
        # Valida o usuário no serviço de usuários
        usuario_response = requests.get(f"{USUARIOS_SERVICE_URL}/{novo_pedido['usuario_id']}")
        if usuario_response.status_code != 200:
            return jsonify({"mensagem": "Usuário não encontrado"}), 400

        # Valida o produto no serviço de produtos
        produto_response = requests.get(f"{PRODUTOS_SERVICE_URL}/{novo_pedido['produto_id']}")
        if produto_response.status_code != 200:
            return jsonify({"mensagem": "Produto não encontrado"}), 400
    except requests.exceptions.ConnectionError as e:
        return jsonify({"mensagem": f"Erro ao comunicar com outros serviços: {e}"}), 500

    novo_pedido["id"] = len(pedidos) + 1
    pedidos.append(novo_pedido)
    return jsonify(novo_pedido), 201

if __name__ == "__main__":
    app.run(port=5003, debug=True) # Iniciando na porta 5003
