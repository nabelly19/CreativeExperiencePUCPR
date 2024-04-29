from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados de exemplo de usuários
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}

# Rota para editar dados de um usuário existente
@app.route('/edit_user/<username>', methods=['PUT'])
def edit_user(username):
    data = request.get_json()
    if 'password' not in data:
        return jsonify({"error": "Senha é necessária"}), 400
    
    if username not in users:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Atualiza a senha do usuário
    users[username]['password'] = data['password']
    
    return jsonify({"message": "Dados do usuário atualizados com sucesso"}), 200

# Rota para remover um usuário existente
@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    if username not in users:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Remove o usuário da lista de usuários
    del users[username]
    
    return jsonify({"message": "Usuário removido com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)
