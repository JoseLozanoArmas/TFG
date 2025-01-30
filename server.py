import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'src/users_input'
ALLOWED_EXTENSIONS = {'py', 'c', 'cc', 'rb', 'js'} 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

route_to_data_json_block_and_question = "future_json_structures/data_information_app.json" # RUTA AL JSON QUE REGISTRA LOS BLOQUES Y PREGUNTAS

# Funciones de ayuda
def allowed_file(filename): # Función para comprobar que los ficheros tienen la extensión permitida
    if not filename or not '.' in filename:
        return False
    extension = filename.rsplit('.', 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS: 
        return False
    return True

# Funciones que se deberían borrar una vez comprobadas
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


# Funciones de usuario    
@app.route('/save-user-name', methods=['POST']) # Crear una carpeta con el nombre del estudiante
def save_user_name():
    data = request.get_json()  
    folder_name = data.get('text', '') 
    if folder_name:
        route_to_folder = os.path.join('users_input', folder_name)
        os.makedirs(route_to_folder, exist_ok = True)
        return jsonify({'message': f'Carpeta creada con éxito en {route_to_folder}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    

@app.route('/create-block-folder-user', methods=["POST"]) # Creación de carpetas para los bloques de preguntas de los estudiantes
def create_block_folder_user():
    data = request.get_json()  
    user_name = data.get('text', '')
    block_name = data.get('block_name', '')
    block_name = "block_" + block_name
    if user_name:
        route = 'users_input/' + user_name + "/"
        folder_path = os.path.join(route, block_name)
        os.makedirs(folder_path, exist_ok = True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    
@app.route('/create-question-folder-user', methods=["POST"])
def create_question_folder_user():
    data = request.get_json()  
    user_name = data.get('text', '')
    block_name = data.get('block_name', '')
    block_name = "block_" + block_name
    question_name = data.get('question_name', '')
    if user_name:
        route = 'users_input/' + user_name + "/" + block_name
        folder_path = os.path.join(route, question_name)
        os.makedirs(folder_path, exist_ok = True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400

    
@app.route('/upload-file-user', methods=['POST']) # Función para que un estudiante pueda subir su código a una pregunta
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No se envió ningún archivo'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'El archivo no tiene nombre'}), 400
    
    user_name = request.form.get('userName', '')
    block_name = request.form.get('blockName', '')
    question_name = request.form.get('questionName', '') 

    if file and allowed_file(file.filename):
        folder_path = "users_input/" + user_name + "/" + block_name + "/" + question_name # Carpeta del usuario (CAMBIAR RUTA)
        os.makedirs(folder_path, exist_ok = True)  # Crea el directorio si no existe
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)
        return jsonify({'message': f'Archivo {file.filename} subido con éxito'}), 200
    else:
        return jsonify({'message': f'El archivo o no se subió correctamente o no tenía la extensión apropiada'}), 200


# Funciones de admin
@app.route('/create-block-folder-admin', methods=["POST"]) # Creación de carpetas para los bloques de preguntas de los administradores/monitores
def create_block_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '') 
    if block_name:
        route = 'data/blocks/'
        folder_path = os.path.join(route, block_name)
        os.makedirs(folder_path, exist_ok = True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    
@app.route('/regist-block-admin', methods=["POST"])
def regist_block_admin():
    data = request.get_json()
    block_id = data.get('text', '')
    route_default_img = "      \"img\": \"src/img/logo_ull.png\"\n"
    end_block = "    }\n"
    end_doc = "}"
    content_block = ""
    # Comprobar si el archivo existe
    if os.path.exists(route_to_data_json_block_and_question):  # Comprueba si el archivo existe en la ruta
        with open(route_to_data_json_block_and_question, 'r') as file:  
            lines = file.readlines()
            if lines:
                lines = lines[:-2]
            if block_id == 1:
                content_block = "{\n    \"block_" + str(block_id) + "\": {\n"
            else:   
                content_block = "    },\n    \"block_" + str(block_id) + "\": {\n"
            with open(route_to_data_json_block_and_question, 'w') as file:
                file.writelines(lines)
                file.write(content_block)
                file.write(route_default_img)
                file.write(end_block)
                file.write(end_doc)
            return jsonify({'message': f'Información actualizada'}), 200
    else:
        # Crear el archivo si no existe
        with open(route_to_data_json_block_and_question, 'w') as file:
            content_block = "{\n    \"block_" + str(block_id) + "\": {\n"
            with open(route_to_data_json_block_and_question, 'w') as file:
                file.write(content_block)
                file.write(route_default_img)
                file.write(end_block)
                file.write(end_doc)
        return jsonify({'message': f'Archivo de registro creado'}), 200
    
@app.route('/create-question-block-folder-admin', methods=["POST"]) # Creación de carpetas para las preguntas de los bloques de los administradores/monitores
def create_question_block_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '')
    question_name = data.get('question_name', '')
    if block_name and question_name:
        route = 'data/blocks/'
        direcction_to_question = block_name + "/" + question_name
        folder_path = os.path.join(route, direcction_to_question)
        os.makedirs(folder_path, exist_ok = True)
        return jsonify({'message': f'Carpeta creada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400
    
@app.route('/regist-question-admin', methods=["POST"])
def regist_question_admin():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    tittle = data.get('tittle', '')
    description = data.get('description','')
    search_current_block_and_img = r"\"block_" + str(block_id) + r"\"\s*:\s*{(.|\n)*?\"img\"\s*:\s*\".*\"" # funciona
    search_last_question = r"\"block_" + str(block_id) + r"\":\s*{\s*\n*.*\n*(.|\n)*?\"question.*" + str(question_id) + "\"(.|\n)*?}"
    upgrade = int(question_id)
    upgrade += 1
    new_question = ",\n      \"question_" + str(upgrade) + "\": {\n"
    current_question = ",\n      \"question_" + str(question_id) + "\": {\n"
    new_tittle = "        \"tittle\": \"" + tittle + "\",\n"
    new_description = "        \"description\": \"" + description + "\"\n"
    end_question = "      }"
    new_content = new_question + new_tittle + new_description + end_question
    first_content = current_question + new_tittle + new_description + end_question
    first_midle_json = ""
    second_midle_json = ""
    final_json = ""

    if os.path.exists(route_to_data_json_block_and_question):  # Comprueba si el archivo existe en la ruta
        with open(route_to_data_json_block_and_question, 'r') as file: # Guardamos y leemos el archivo
            lines = file.readlines()
            content = ''.join(lines)
            if lines: 
                find_last_question = re.search(search_last_question, content) # Comprobamos que en el bloque que buscamos haya al menos una pregunta
                if find_last_question:
                    first_midle_json = content[:find_last_question.end()]
                    second_midle_json = content[find_last_question.end():]
                    final_json = first_midle_json + new_content + second_midle_json
                else:
                    find_current_block = re.search(search_current_block_and_img, content)
                    if find_current_block:
                        first_midle_json = content[:find_current_block.end()]
                        second_midle_json = content[find_current_block.end():]
                        final_json = first_midle_json + first_content + second_midle_json
                    else:
                        return jsonify({'message': 'Texto vacío, no se puede registrar la pregunta'}), 400
        with open(route_to_data_json_block_and_question, 'w') as file:
            file.write(final_json)
            return jsonify({'message': f'Pregunta registrada con éxito'}), 200
    else:
        # Crear el archivo si no existe
        return jsonify({'message': 'Error, no se pudo encontrar el fichero de registro debido'}), 400

@app.route('/update-current-question', methods=["POST"])
def update_current_question():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    tittle = data.get('tittle', '')
    description = data.get('description','')
    search_block_and_last_question = r"\"block_" + str(block_id) + r"\":\s*{\s*\n*.*\n*(.|\n)*?\"question.*" + str(question_id) + r"\"(.|\n)*?}"
    search_current_block_and_img = r"\"block_" + str(block_id) + r"\"\s*:\s*{(.|\n)*?\"img\"\s*:\s*\".*\""
    current_question = ",\n      \"question_" + str(question_id) + "\": {\n"
    new_tittle = "        \"tittle\": \"" + tittle + "\",\n"
    new_description = "        \"description\": \"" + description + "\"\n"
    end_question = "      }"
    new_content = current_question + new_tittle + new_description + end_question

    first_midle_json = ""
    second_midle_json = ""
    final_json = ""

    if os.path.exists(route_to_data_json_block_and_question):  # Comprueba si el archivo existe en la ruta
        with open(route_to_data_json_block_and_question, 'r') as file: # Guardamos y leemos el archivo
            lines = file.readlines()
            content = ''.join(lines)
            if lines: 
                find_cuestion_to_change = re.search(search_block_and_last_question, content)
                find_route_to_img = re.search(search_current_block_and_img, content)
                if find_cuestion_to_change and find_route_to_img:
                    first_midle_json = content[:find_route_to_img.end()]
                    second_midle_json = content[find_cuestion_to_change.end():]
                    final_json = first_midle_json + new_content + second_midle_json
                else:
                    return jsonify({'message': 'Error. No se encontró la ruta a la pregunta'}), 400
        with open(route_to_data_json_block_and_question, 'w') as file:
           file.write(final_json)
        return jsonify({'message': f'Pregunta actualizada con éxito'}), 200
    else:
        return jsonify({'message': 'Error, no se pudo encontrar el fichero de registro debido'}), 400

@app.route('/upload-admin-test-to-question-folder', methods=["POST"]) # Permitir subir pruebas a una pregunta a los administradores/monitores
def upload_admin_test_to_question_folder():
    block_name = request.form.get('text', '')
    question_name = request.form.get('question_name', '')
    if block_name and question_name:
        route = 'data/blocks/'
        direcction_to_question = block_name + "/" + question_name
        folder_path = os.path.join(route, direcction_to_question)
        os.makedirs(folder_path, exist_ok = True)
        files = request.files.getlist('files') 
        if not files:
            return jsonify({'message': 'No se mandó ningún archivo'}), 400
        saved_files = []
        for file in files:
            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            saved_files.append(file.filename)
        return jsonify({'message': f'Pruebas enviadas con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400

@app.route('/delete-selected-test', methods=["POST"]) # Eliminar una prueba en concreto de una pregunta de los administradores/monitores
def delete_selected_test(): # AÑADIR FUNCIONALIDAD EN LA PARTE NO SERVIDOR
    data = request.get_json()
    block_name = data.get('text', '')
    question_name = data.get('question_name', '')
    test_name = data.get('test_name', '')
    if block_name and question_name and test_name:
        route = 'data/blocks/'
        direcction_to_question = block_name + "/" + question_name + "/" + test_name
        file_path = os.path.join(route, direcction_to_question)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path) 
            return jsonify({'message': f'Prueba \"{test_name}\" eliminada con éxito'}), 200
    else:
        return jsonify({'message': f'No se pudo eliminar la prueba {test_name}'}), 400


    
@app.route('/delete-last-block-folder-admin', methods=["POST"]) # Eliminar la carpeta del último bloque de preguntas de los administradores/monitores
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

@app.route('/delete-last-block-json', methods=["POST"])
def delete_last_block_json():
    data = request.get_json()  
    block_id = data.get('text', '') 
    search_block = r"\s*\"block_" + str(block_id) + r"\":\s*{(.|\n)*"
    before_deleted_part = ""
    final_content = ""

    # Comprobar si el archivo existe
    if os.path.exists(route_to_data_json_block_and_question):  # Comprueba si el archivo existe en la ruta
        with open(route_to_data_json_block_and_question, 'r') as file:  
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_last_block = re.search(search_block, content)
                if find_last_block:
                    before_deleted_part = content[:find_last_block.start() - 1]
                    final_content = before_deleted_part + "\n}"
                    if final_content == "\n}":
                        final_content = "{" + final_content
            with open(route_to_data_json_block_and_question, 'w') as file:
                file.write(final_content)
        return jsonify({'message': f'Último bloque eliminado del JSON de registro'}), 200
    else:
        return jsonify({'message': f'Error al eliminar el último bloque del JSON de registro'}), 400

@app.route('/delete-question-folder-admin', methods=["POST"]) # Eliminar la carpeta de la última pregunta de los administradores/monitores
def delete_question_folder_admin():
    data = request.get_json()  
    block_name = data.get('text', '')
    question_name = data.get('question_name', '')
    if block_name and question_name:
        route = 'data/blocks/'
        direcction_to_question = block_name + "/" + question_name
        folder_path = os.path.join(route, direcction_to_question)
        try:
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path) 
            return jsonify({'message': f'Carpeta de pregunta {question_name} eliminada con éxito'}), 200
        except Exception as e:
            return jsonify({'message': f'Error al eliminar contenido: {str(e)}'}), 500

@app.route('/delete-last-question-admin', methods=["POST"])
def delete_last_question_admin():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_name', '')
    search_block_and_last_question = r"\"block_" + str(block_id) + r"\":\s*{\s*\n*.*\n*(.|\n)*?\"question.*" + str(question_id) + r"\"(.|\n)*?}"
    search_only_last_question = r"\"question_" + str(question_id) + r"\"(.|\n)*?}"
    if os.path.exists(route_to_data_json_block_and_question):  # Comprueba si el archivo existe en la ruta
        with open(route_to_data_json_block_and_question, 'r') as file: # Guardamos y leemos el archivo
            lines = file.readlines()
            content = ''.join(lines)
            if lines: 
                find_last_question = re.search(search_block_and_last_question, content)
                if find_last_question:
                    content_before_remove_question = content[:find_last_question.end()]
                    rest_file = content[find_last_question.end():]
                    find_only_last_question = re.search(search_only_last_question, content_before_remove_question) # Localizamos la pregunta en si y calculamos el recorte
                    cut_lenght = find_only_last_question.end() - find_only_last_question.start()
                    cut_last_question = content_before_remove_question[:-cut_lenght]
                    final_json = cut_last_question + rest_file # Juntamos todo
        with open(route_to_data_json_block_and_question, 'w') as file:
            file.write(final_json)
        return jsonify({'message': f'Última pregunta del bloque block_{block_id} eliminada del JSON de registro'}), 200
    else:
        return jsonify({'message': f'Error, no se pudo encontrar el fichero de registro debido'}), 500
     
@app.route('/update-route-img', methods=["POST"])
def uptdate_route_img():
    data = request.get_json()  
    block_id = data.get('text', '')
    route_img = data.get('route_img', '')
    search_current_block_and_img = r"\"block_" + str(block_id) + r"\":\s*{(.|\n)*?\"img\":\s*\".*?\",?" # funciona
    search_only_img = r"\"img\":.*"
    new_img = "\"img\": " + route_img
    content_before_change_old_img = ""
    final_json = ""
    if os.path.exists(route_to_data_json_block_and_question):
        with open(route_to_data_json_block_and_question, 'r') as file: # Guardamos y leemos el archivo
            lines = file.readlines()
            content = ''.join(lines)
            if lines: 
                find_old_img = re.search(search_current_block_and_img, content) # Comprobamos que en el bloque que buscamos haya al menos una pregunta
                if find_old_img:
                    content_before_change_old_img = content[:find_old_img.end()] # Recortar hasta encontrar la ruta de la img
                    save_possible_comma = content_before_change_old_img[-1] # Comprobamos si tiene o no ","
                    rest_file = content[find_old_img.end():] # Guardamos el resto del fichero antes de la img
                    find_only_img_route = re.search(search_only_img, content_before_change_old_img) # Localizamos en si la img y calculamos cuanto mide para sustituir por la nueva
                    cut_lenght = find_only_img_route.end() - find_only_img_route.start()
                    cut_old_route = content_before_change_old_img[:-cut_lenght]
                    if (save_possible_comma == ","): # En caso de haber coma se la añadimos a la ruta nueva
                        new_img = new_img + ","
                    final_json = cut_old_route + new_img + rest_file # Juntamos todo
                else:
                    return jsonify({'message': f'Error, no se pudo encontrar la imagen'}), 500
        with open(route_to_data_json_block_and_question, 'w') as file:
            file.write(final_json)
        return jsonify({'message': f'Imágen actualizada con éxito'}), 200
    else:
        return jsonify({'message': f'Error, no se pudo encontrar el fichero de registro debido'}), 500

# Funciones de settings
@app.route('/reset-users', methods=['POST']) # Eliminar todos los registros de los estudiantes (administrador)
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
    
@app.route('/reset-blocks-data', methods=['POST']) # Eliminar todos los registros de los bloques de preguntas (administrador)
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

@app.route('/reset-users-registered-data', methods=['POST']) # Eliminar todos los usuarios registrados, ya sean administradores o monitores
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

@app.route('/add-new-user', methods=['POST']) # Añadir un nuevo usuario ya sea administrador o monitor
def add_new_user():
    data = request.get_json()  
    text = data.get('text', '')  
    if text:
        with open('data/users_registered/info_users.csv', 'a') as file: # Si le pongo la opción 'w' sobreescribe con 'a' añado
            file.write(text + '\n')
        return jsonify({'message': 'Usuario registrado con éxito'}), 200
    else:
        return jsonify({'message': 'Texto vacío'}), 400

@app.route('/remove-last-user', methods=['POST']) # Eliminar el último usuario ya sea administrador o monitor
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
