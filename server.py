import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'src/users_input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    folder_name = data.get('text', '') 

    if folder_name:
        folder_path = os.path.join('users_input', folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    

@app.route('/create-block-folder-user', methods=["POST"]) # Creación de carpetas para los bloques de preguntas de los usuarios
def create_block_folder_user():
    data = request.get_json()  
    user_name = data.get('text', '')
    block_name = data.get('block_name', '')
    block_name = "block_" + block_name
    if user_name:
        route = 'users_input/' + user_name + "/"
        folder_path = os.path.join(route, block_name)
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    
@app.route('/create-block-folder-admin', methods=["POST"]) # Creación de carpetas para los bloques de preguntas de los admins
def create_block_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '') 
    if block_name:
        route = 'data/blocks/'
        folder_path = os.path.join(route, block_name)
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    
@app.route('/create-question-block-folder-admin', methods=["POST"]) # Creación de carpetas para las preguntas de los bloques de los admins
def create_question_block_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '')
    question_name = data.get('question_name', '')
    if block_name and question_name:
        route = 'data/blocks/'
        direcction_to_question = block_name + "/" + question_name
        folder_path = os.path.join(route, direcction_to_question)
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    

    
@app.route('/delete-last-block-folder-admin', methods=["POST"])
def delete_last_block_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '') 
    block_dir = "block_" + block_name
    if block_name:
        route = 'data/blocks/'
        folder_path = os.path.join(route, block_dir)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # Eliminar carpeta
        return jsonify({'message': f'Carpeta eliminada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede eliminar carpeta'}), 400


@app.route('/upload-file-user', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No se envió ningún archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'El archivo no tiene nombre'}), 400
    
    user_name = request.form.get('userNameData', '') 


    if file:
        folder_path = "users_input/" + user_name + "/" + "borrar" # Carpeta del usuario (CAMBIAR RUTA)
        os.makedirs(folder_path, exist_ok=True)  # Crea el directorio si no existe
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)
        return jsonify({'message': f'Archivo {file.filename} subido con éxito'}), 200
    
@app.route('/reset-users', methods=['POST'])
def reset_users():
    folder_path = 'users_input'
    try:
        # Elimina todos los archivos y subcarpetas en la carpeta especificada
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Eliminar archivo o enlace
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Eliminar carpeta
        return jsonify({'message': 'Usuarios eliminados con éxito'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al eliminar contenido: {str(e)}'}), 500
    
@app.route('/reset-blocks-data', methods=['POST'])
def reset_blocks_data():
    folder_path = 'data/blocks'
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Eliminar archivo o enlace
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Eliminar carpeta
        return jsonify({'message': 'Información de bloques eliminada con éxito'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al eliminar contenido: {str(e)}'}), 500

@app.route('/reset-users-registered-data', methods=['POST'])
def reset_users_registered_data():
    folder_path = 'data/users_registered'
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Eliminar archivo o enlace
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Eliminar carpeta
        return jsonify({'message': 'Información de usuarios registrados eliminada con éxito'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al eliminar contenido: {str(e)}'}), 500

@app.route('/add-new-user', methods=['POST'])
def add_new_user():
    data = request.get_json()  
    text = data.get('text', '')  
    if text:
        with open('data/users_registered/info_users.csv', 'a') as file: # Si le pongo la opción 'w' sobreescribe con 'a' añado
            file.write(text + '\n')
        return jsonify({'message': 'Usuario registrado con éxito'}), 200
    else:
        return jsonify({'message': 'Texto vacío'}), 400

@app.route('/remove-last-user', methods=['POST'])
def remove_last_user():
    file_path = 'data/users_registered/info_users.csv'    
    with open(file_path, 'r') as file: # Leer todas las líneas del archivo
        lines = file.readlines()
    if len(lines) <= 1: # Verificar que haya más de una línea
        # print("No se puede eliminar al administrador por defecto")
        return
    with open(file_path, 'w') as file: # Escribir las líneas excepto la última de vuelta al archivo
        file.writelines(lines[:-1])  # Todas las líneas excepto la última
    return jsonify({'message': 'Usuario eliminado con éxito'}), 200


if __name__ == '__main__':
    app.run(debug=True)
