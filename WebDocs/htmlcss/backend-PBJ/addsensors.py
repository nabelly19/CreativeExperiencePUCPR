from flask import Flask, request, jsonify

app = Flask(__name__)

# Dicionário para armazenar os sensores e atuadores
devices = {}

# Rota para cadastrar um novo sensor
@app.route('/register_sensor', methods=['POST'])
def register_sensor():
    data = request.get_json()
    if 'sensor_id' not in data or 'location' not in data:
        return jsonify({"error": "ID do sensor e localização são necessários"}), 400
    
    sensor_id = data['sensor_id']
    location = data['location']
    
    if sensor_id in devices:
        return jsonify({"error": "Sensor já cadastrado"}), 400
    
    # Adiciona o novo sensor ao dicionário de dispositivos
    devices[sensor_id] = {"type": "sensor", "location": location}
    
    return jsonify({"message": "Sensor cadastrado com sucesso"}), 201

# Rota para cadastrar um novo atuador
@app.route('/register_actuator', methods=['POST'])
def register_actuator():
    data = request.get_json()
    if 'actuator_id' not in data or 'location' not in data:
        return jsonify({"error": "ID do atuador e localização são necessários"}), 400
    
    actuator_id = data['actuator_id']
    location = data['location']
    
    if actuator_id in devices:
        return jsonify({"error": "Atuador já cadastrado"}), 400
    
    # Adiciona o novo atuador ao dicionário de dispositivos
    devices[actuator_id] = {"type": "actuator", "location": location}
    
    return jsonify({"message": "Atuador cadastrado com sucesso"}), 201

if __name__ == '__main__':
    app.run(debug=True)
