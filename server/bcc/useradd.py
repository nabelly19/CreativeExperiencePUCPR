from flask import Flask, request, jsonify
from login import login

app = Flask(__name__)

# Dados de exemplo de usuários
users = {}

# Rota para cadastrar um novo usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Usuário e senha são necessários"}), 400
    
    username = data['username']
    password = data['password']
    
    if username in users:
        return jsonify({"error": "Usuário já existe"}), 400
    
    # Adiciona o novo usuário à lista de usuários
    users[username] = {"password": password}
    
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

if __name__ == '__main__':
    app.run(debug=True)
