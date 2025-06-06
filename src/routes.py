from flask import Flask, request, jsonify, render_template
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('caminhos.json', indent=4)
Caminho = Query()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_caminho', methods=['POST'])
def cadastrar_caminho():
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 415
    
    dados = request.get_json()
    if not all(k in dados for k in ["x", "y", "z"]):
        return jsonify({"error": "Campos x, y e z são obrigatórios"}), 400

    caminho_id = db.insert(dados)
    return jsonify({"message": "Caminho cadastrado com sucesso!", "id": caminho_id})

@app.route('/consultar_caminho', methods=['GET'])
def consultar_caminho():
    caminho_id = request.args.get("caminho_id")
    
    if not caminho_id or not caminho_id.isdigit():
        return jsonify({"error": "ID inválido"}), 400
    
    caminho_id = int(caminho_id)
    caminho = db.get(doc_id=caminho_id)
    
    if caminho:
        return jsonify({"id": caminho_id, **caminho})
    return jsonify({"error": "Caminho não encontrado"}), 404

@app.route('/atualizar_caminho/<int:caminho_id>', methods=['PUT'])
def atualizar_caminho(caminho_id):
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 415

    dados = request.get_json()
    if not all(k in dados for k in ["x", "y", "z"]):
        return jsonify({"error": "Campos x, y e z são obrigatórios"}), 400

    caminho = db.get(doc_id=caminho_id)

    if caminho:
        db.update(dados, doc_ids=[caminho_id])
        return jsonify({"message": "Caminho atualizado com sucesso!", "id": caminho_id})
    
    return jsonify({"error": "Caminho não encontrado"}), 404

@app.route('/deletar_caminho/<int:caminho_id>', methods=['DELETE'])
def deletar_caminho(caminho_id):
    caminho = db.get(doc_id=caminho_id)

    if caminho:
        db.remove(doc_ids=[caminho_id])
        return jsonify({"message": "Caminho deletado com sucesso!", "id": caminho_id})
    
    return jsonify({"error": "Caminho não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
