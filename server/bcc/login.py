from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados de exemplo de usuário
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}

# Rota para validar o usuário
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Usuário e senha são necessários"}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users or users[username]['password'] != password:
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    return jsonify({"message": "Login bem sucedido"}), 200

if __name__ == '__main__':
    app.run(debug=True)
