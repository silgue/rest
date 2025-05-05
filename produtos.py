from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados simulado de produtos
produtos = [
    {"id": 1, "nome": "Produto A", "preco": 10.99},
    {"id": 2, "nome": "Produto B", "preco": 19.99},
    {"id": 3, "nome": "Produto C", "preco": 5.99},
]

# Rota para obter todos os produtos
@app.route("/produtos", methods=["GET"])
def obter_produtos():
    """
    Retorna uma lista de todos os produtos.
    """
    return jsonify(produtos)

# Rota para obter um produto específico por ID
@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """
    Retorna um produto específico com base no ID.

    :param id: O ID do produto a ser recuperado.
    :type id: int
    :returns: Um JSON contendo os dados do produto ou uma mensagem de erro se o produto não for encontrado.
    """
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"mensagem": "Produto não encontrado"}), 404

# Rota para criar um novo produto
@app.route("/produtos", methods=["POST"])
def criar_produto():
    """
    Cria um novo produto e o adiciona à lista de produtos.
    Espera um JSON com os campos 'nome' e 'preco'.
    """
    novo_produto = request.get_json()
    if not novo_produto or "nome" not in novo_produto or "preco" not in novo_produto:
        return jsonify({"mensagem": "Requisição inválida. Certifique-se de fornecer 'nome' e 'preco'."}), 400
    novo_produto["id"] = len(produtos) + 1
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

if __name__ == "__main__":
    app.run(port=5002, debug=True) # Iniciando na porta 5002