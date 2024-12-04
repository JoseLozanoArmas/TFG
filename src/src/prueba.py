import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.get_json()  
    text = data.get('text', '')  
    if text:
        with open('src/users_input/entrada.py', 'w') as file: # Si le pongo la opción 'w' sobreescribe con 'a' añado
            file.write(text + '\n')
        return jsonify({'message': 'Texto guardado con éxito'}), 200
    else:
        return jsonify({'message': 'Texto vacío'}), 400
    
@app.route('/save-user-name', methods=['POST'])
def save_user_name():
    data = request.get_json()  
    folder_name = data.get('text', '')  # Nombre de la carpeta basado en la variable `text`

    if folder_name:
        folder_path = os.path.join('src/users_input', folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400

if __name__ == '__main__':
    app.run(debug=True)
