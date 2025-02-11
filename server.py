import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil
import re
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'src/users_input'
ALLOWED_EXTENSIONS = {'py', 'c', 'cc', 'rb', 'js'} 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rutas a los ficheros de registro de información
route_to_data_json_block_and_question = "future_json_structures/data_information_app.json" # RUTA AL JSON QUE REGISTRA LOS BLOQUES Y PREGUNTAS (INFO)
route_to_json_buttons_blocks = "future_json_structures/data_blocks_buttons.json" # RUTA AL JSON QUE REGISTRA LA INFO DE LOS BOTONES DE BLOQUES
route_to_json_buttons_questions = "future_json_structures/data_questions_buttons.json" # RUTA AL JSON QUE REGISTRA LA INFO DE LOS BOTONES DE QUESTIONS
route_to_info_users_json = "future_json_structures/info_users.json" # RUTA AL JSON QUE GESTIONA LOS USUARIOS
route_to_rankings_info = "data/rankings_info"
route_to_puntuations = "data/puntuations"
# Rutas a las carpetas donde se subiran los códigos
route_to_users_input = "users_input"
route_to_admins_and_monitors_tests = "data/blocks"

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
     
@app.route('/create-block-folder-admin-for-puntuations', methods=["POST"])
def create_block_folder_admin_for_puntuations():
    data = request.get_json()  
    block_name = data.get('text', '') 
    if block_name:
        route = 'data/puntuations'
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

@app.route('/regist-block-button', methods=["POST"])
def regist_block_button():
    data = request.get_json()
    button_id = data.get('text', '')
    positionX = data.get('positionX', '')
    positionY = data.get('positionY', '')
    type = data.get('type', '')
    block_name = data.get('block_name', '')

    begin_document = "[\n"
    begin_entry = "    {\n"
    line_id = f"        \"id\": {button_id},\n"
    line_positionX = f"        \"positionX\": {positionX},\n"
    line_positionY = f"        \"positionY\": {positionY},\n"
    line_type = f"        \"type\": \"{type}\",\n"
    line_block_name = f"        \"block_name\": \"{block_name}\"\n"
    end_entry = "    }"
    end_document = "\n]"
    content = begin_entry + line_id + line_positionX + line_positionY + line_type + line_block_name + end_entry
    if os.path.exists(route_to_json_buttons_blocks):  # Comprueba si el archivo existe en la ruta
        with open(route_to_json_buttons_blocks, 'r') as file:
            lines = file.readlines()
        if lines:
            lines = lines[:-2]
        if button_id == 1:
            content = begin_document + content + end_document
        else:   
            content = end_entry + ",\n" + content + end_document
        with open(route_to_json_buttons_blocks, 'w') as file:
            file.writelines(lines)
            file.write(content)
        return jsonify({'message': 'Archivo actualizado'}), 200
    else:
        # Crear el archivo si no existe
        with open(route_to_json_buttons_blocks, 'w') as file:
            content = begin_document + content + end_document
            file.write(content)
        return jsonify({'message': 'Archivo creado'}), 200

    
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

@app.route('/regist-question-button', methods=["POST"])
def regist_question_button():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    label = data.get('label', '')
    name = data.get('name', '')
    begin_document = "{\n"
    line_block_id = f"    \"block_{block_id}\"" + ": {\n"
    line_question_id = f"      \"question_" + str(question_id) + "\": {\n" + "        \"id\": " + str(question_id) + ",\n"
    line_label = f"        \"label\": \"{label}\",\n"
    line_name = f"        \"name\": \"{name}\"\n"
    end_entry = "      }\n    }"
    end_question = "      }"
    end_document = "\n}"
    content = line_block_id + line_question_id + line_label + line_name + end_entry
    search_block = r"\"block_" + str(block_id) + r"\"\s*:\s*{"
    search_question = r"\"block_" + str(block_id) + "\"(.|\n)*?\"question_" + str(question_id - 1) + "\"(.|\n)*?}"

    first_middle = ""
    second_middle = ""
    final_json = ""

    if os.path.exists(route_to_json_buttons_questions):  # Comprueba si el archivo existe en la ruta
        with open(route_to_json_buttons_questions, 'r') as file:  
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_current_block = re.search(search_block, content)
                if find_current_block:
                    find_current_question = re.search(search_question, content)
                    if find_current_question:
                        first_middle = content[:find_current_question.end()]
                        new_content = "\n" + line_question_id + line_label + line_name + end_question
                        second_middle = content[find_current_question.end():]
                        final_json = first_middle + "," + new_content + second_middle
                        with open(route_to_json_buttons_questions, 'w') as file:
                            file.write(final_json)
                    else:
                        new_content = content[:-3]
                        new_question_line = f"  \"question_" + str(question_id) + "\": {\n" + "        \"id\": " + str(question_id) + ",\n"
                        new_end_doc = "\n    }\n}"
                        new_content += new_question_line + line_label + line_name + end_question + new_end_doc
                        with open(route_to_json_buttons_questions, 'w') as file:
                            file.write(new_content)
                else:
                    content = content[:-3]
                    new_content = "\n" + line_question_id + line_label + line_name + end_question
                    content += "},\n    \"block_" + str(block_id) + "\": {" + new_content + "\n    }\n}"
                    with open(route_to_json_buttons_questions, 'w') as file:
                        file.write(content)
                return jsonify({'message': f'Registro de botones de preguntas actualizado'}), 200
    else:
        with open(route_to_json_buttons_questions, 'w') as file:
            new_content = begin_document + content + end_document
            file.write(new_content)
        return jsonify({'message': f'Archivo de botones de preguntas creado'}), 200

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

@app.route('/regist-question-test-information', methods=["POST"])
def regist_question_test_information():
    block_name = request.form.get('text', '')
    question_name = request.form.get('question_name', '')
    input_files = request.files.getlist('files')
    result_files = request.files.getlist('resultFiles')
    points = request.values.getlist('points')
    create_route = route_to_puntuations + "/" + block_name + "/" + question_name + "_puntuations.json"
    begin_doc = "[\n"
    with open(create_route, 'w') as file:
        file.write(begin_doc) 
    new_test = "" 
    for index in range (len(input_files)): 
        begin = "  {\n"
        enter_file = f"    \"enter_file\": \"{input_files[index].filename}\",\n"
        result_file = f"    \"result_file\": \"{result_files[index].filename}\",\n"
        puntuation = f"    \"puntuation\": {points[index]}\n"
        end = "  },\n"
        if index == len(input_files) - 1:
            end = "  }\n]"
        new_test = begin + enter_file + result_file + puntuation + end
        with open(create_route, 'a') as file:
            file.write(new_test)
    return jsonify({'message': f'Pruebas de la pregunta {question_name} registradas con éxito'}), 200
    
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
        resultFiles = request.files.getlist('resultFiles')
        if not files or not resultFiles:
            return jsonify({'message': 'No se mandó ningún archivo'}), 400
        saved_files = []
        for file in files:
            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            saved_files.append(file.filename)

        saved_result_files = []
        for file in resultFiles:
            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            saved_result_files.append(file.filename)
        return jsonify({'message': f'Pruebas enviadas con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede crear carpeta'}), 400

@app.route('/delete-selected-test', methods=["POST"]) # Eliminar una prueba en concreto de una pregunta de los administradores/monitores
def delete_selected_test(): # AÑADIR FUNCIONALIDAD EN LA PARTE NO SERVIDOR
    data = request.get_json()
    block_name = data.get('text', '')
    question_name = data.get('question_name', '')
    enter_test_name = data.get('enter_test_name', '')
    result_test_name = data.get('result_test_name', '')

    if block_name and question_name and enter_test_name and result_test_name:
        route = 'data/blocks/'
        direcction_to_enter_test_name = block_name + "/" + question_name + "/" + enter_test_name
        direcction_to_result_test_name = block_name + "/" + question_name + "/" + result_test_name
        file_path_to_enter_test = os.path.join(route, direcction_to_enter_test_name)
        if os.path.isfile(file_path_to_enter_test) or os.path.islink(file_path_to_enter_test):
            os.unlink(file_path_to_enter_test)
        file_path_to_result_test = os.path.join(route, direcction_to_result_test_name)
        if os.path.isfile(file_path_to_result_test) or os.path.islink(file_path_to_result_test):
            os.unlink(file_path_to_result_test)  
        return jsonify({'message': f'Prueba eliminada con éxito'}), 200
    else:
        return jsonify({'message': f'No se pudo eliminar la prueba {enter_test_name}'}), 400


    
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

 
@app.route('/delete-last-block-folder-admin-for-puntuations', methods=["POST"]) # Eliminar la carpeta del último bloque de preguntas de los administradores/monitores
def delete_last_block_folder_admin_for_puntuations():
    data = request.get_json()  
    block_name = data.get('text', '') 
    block_dir = "block_" + block_name
    if block_name:
        route = 'data/puntuations/'
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
    
@app.route('/delete-last-block-button-of-json', methods=["POST"])
def delete_last_block_button_of_json():
    data = request.get_json()
    button_id = data.get('text', '')
    search_block = r",?\s*{\n*\s*\"id\":\s*" + str(button_id) + r"(.|\n)*?}"
    if os.path.exists(route_to_json_buttons_blocks):  # Comprueba si el archivo existe en la ruta
        with open(route_to_json_buttons_blocks, 'r') as file:  
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_last_block = re.search(search_block, content)
                if find_last_block:
                    content = content[:find_last_block.start()]
                    content += "\n]"
                else:
                    return jsonify({'message': f'Error. No se encontró el bloque'}), 400
        with open(route_to_json_buttons_blocks, 'w') as file:
            file.write(content)
        return jsonify({'message': f'Último bloque eliminado'}), 200
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
 
@app.route('/delete-question-button-json', methods=["POST"])
def delete_question_button_json():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')

    print(block_id)
    print(question_id)

    search_block = r"\"" + block_id + r"\"\s*:\s*{"
    search_question = r"\"" + block_id + r"\"(.|\n)*?\"question_" + str(question_id) + r"\"(.|\n)*?}"
    search_question_in_cut = r",?\s*\"question_" + str(question_id) + r"\"(.|\n)*?}"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_json_buttons_questions):  # Comprueba si el archivo existe en la ruta
        with open(route_to_json_buttons_questions, 'r') as file:  
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_current_block = re.search(search_block, content)
                if find_current_block:
                    find_current_question = re.search(search_question, content)
                    if find_current_question:
                        first_middle = content[:find_current_question.end()]
                        second_middle = content[find_current_question.end():]
                        save_block_and_cuestion = find_current_question.group()
                        find_question_in_cut = re.search(search_question_in_cut, save_block_and_cuestion)
                        if find_question_in_cut:
                            first_middle = first_middle[:-len(find_question_in_cut.group())]
                            final_json = first_middle + second_middle
                            with open(route_to_json_buttons_questions, 'w') as file:
                                file.write(final_json)
                            return jsonify({'message': f'Botón de la pregunta \"question_{question_id}\" del bloque \"{block_id}\" eliminado'}), 200
                        else:
                            return jsonify({'message': f'Error inesperado al localizar la pregunta a eliminar'}), 400
                    else:
                        return jsonify({'message': f'Error, no se encontró la pregunta a eliminar'}), 400
                else:
                    return jsonify({'message': f'Error, no se encontró el bloque de la pregunta a eliminar'}), 400
            else:
                return jsonify({'message': f'Error, no se encontró contenido a eliminar'}), 400
    else:
        return jsonify({'message': f'Error, no se encontró el archivo de registro'}), 400

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
    username = data.get('text', '')  
    password = data.get('password', '')
    rol = data.get('rol', '')
    begin_doc = "[\n"
    first_line = "    },\n"
    username_line = "    {\n      \"username\": \"" + username + "\",\n"
    password_line = "      \"password\": \"" + password + "\",\n"
    rol_line = "      \"rol\": \"" + rol + "\"\n"
    end_line = "    }\n]"
    search_user = r"\"username\":\s*\"" + username + r"\""
    if os.path.exists(route_to_info_users_json):
        with open(route_to_info_users_json, 'r') as file:
            lines = file.readlines()
            lines = lines[:-2]
            content = ''.join(lines)
            if lines:
                find_if_user_exist = re.search(search_user, content)
                if find_if_user_exist:
                    return jsonify({'message': 'El usuario ya estaba registrado'}), 400
                else:     
                    with open(route_to_info_users_json, 'w') as file:
                        file.write(content)  # Escribimos las líneas originales menos las 2 últimas
                        file.write(first_line)  # Añadimos el comienzo del objeto
                        file.write(username_line)
                        file.write(password_line)
                        file.write(rol_line)
                        file.write(end_line)  # Añadimos el final del documento
                        return jsonify({'message': 'Usuario registrado con éxito'}), 200
            else:
                return jsonify({'message': 'Texto vacío'}), 400
    else:
        with open(route_to_info_users_json, 'w') as file:
            file.write(begin_doc)  # Añadimos el comienzo del objeto
            file.write(username_line)
            file.write(password_line)
            file.write(rol_line)
            file.write(end_line)  # Añadimos el final del documento
            return jsonify({'message': 'Archivo de registro de usuarios creado'}), 200
 
@app.route('/remove-last-user', methods=['POST']) # Eliminar el último usuario ya sea administrador o monitor
def remove_last_user():
    search_users_enters = r"{(.|\n)*?}"
    if os.path.exists(route_to_info_users_json): 
        with open(route_to_info_users_json, 'r') as file:
            lines = file.readlines()
            content = "".join(lines)
            if lines:
                find_users = re.findall(search_users_enters, content)
                if len(find_users) > 1:
                    save_the_last = ""
                    for search in re.finditer(search_users_enters, content):
                        save_the_last = search
                    content = content[:save_the_last.start() - 7] # Eliminamos los espacios y las comas
                    content += "}\n]"
                    with open(route_to_info_users_json, 'w') as file:
                        file.write(content)
                else:
                    pass
    else:
        return jsonify({'message': "Error, no se encontró el fichero de registro de usuarios"}), 400
    return jsonify({'message': 'Usuario eliminado con éxito'}), 200


# Funciones de corrección de código

# FALTA ADAPTARLAS CON EL RESTO DE FUNCIONES
# P3 
@app.route('/check_is_possible_to_correct', methods = ["POST"])
def check_is_possible_to_correct():
    data = request.get_json()  
    user_name = data.get('text', '')  
    block_id = data.get('block_id', '')
    create_route_to_tests = route_to_admins_and_monitors_tests + "/" + block_id # Guardamos las rutas a donde las pruebas y entradas
    create_route_to_user_inputs = route_to_users_input + "/" + user_name + "/" + block_id
    if os.path.exists(create_route_to_tests) and os.path.exists(create_route_to_user_inputs): # En caso de que ambas existan procedemos
        save_total_questions = os.listdir(create_route_to_tests)
        save_total_user_inputs = os.listdir(create_route_to_user_inputs)
        if len(save_total_questions) == len(save_total_user_inputs): # Si no hay el mismo numero de pruebas que las del usuario y los admins se retorna false
            for i in range(len(save_total_user_inputs)): # Si hay el mismo, se comprueba que NO esten vacias
                aux_route = create_route_to_user_inputs + "/" + save_total_user_inputs[i]
                if len(os.listdir(aux_route)) == 0: # En caso de estarlo se retorna Falso
                    return jsonify({'data': False})
            return jsonify({'data': True}) # Si se llega aquí quiere decir que el usuario a respondido a todo y se puede evaluar
        else:
            return jsonify({'data': False})
    else:
        # METER CONDICIÓN DE ERROR?????
        return jsonify({'data': False})


# P4
def save_all_user_routes_files(user_name, block_id): 
    users_files = []
    create_route_files = route_to_users_input + "/" + user_name + "/" + block_id # Comprobamos que la dirección del usuario existe
    if os.path.exists(create_route_files): 
        save_route_to_questions = os.listdir(create_route_files)
        for i in range(len(save_route_to_questions)):
            route_to_file = create_route_files + "/" + save_route_to_questions[i]
            save_route_to_file = os.listdir(route_to_file)
            for j in range(len(save_route_to_file)):
                aux_route = create_route_files + "/" + save_route_to_questions[i] + "/" + save_route_to_file[j]
                users_files.append(aux_route)      
    else:
        return jsonify({'message': 'Hubo un error durante el procesado de los datos, vuelva a intentarlo'}), 400     
    users_files.sort()
    return users_files

# P5
def localize_all_questions(block_id):
    all_questions = []
    route_to_tests = route_to_admins_and_monitors_tests + "/" + block_id # Guardamos la dirección a los tests
    if os.path.exists(route_to_tests): 
        save_route_to_questions = os.listdir(route_to_tests)
        for i in range(len(save_route_to_questions)):
            all_questions.append(save_route_to_questions[i])    
    else:
        return jsonify({'message': "Error, no se pudo localizar las preguntas"}), 400    
    all_questions.sort()
    return all_questions

def filter_routes_to_tests_for_questions(block_id, question_id, user_file):
    route_to_test = route_to_admins_and_monitors_tests + "/" + block_id + "/" + question_id + "/"
    save_route_to_test = os.listdir(route_to_test)
    save_users_code_extension = os.path.splitext(user_file)
    save_users_code_extension = save_users_code_extension[1]
    tests_to_use = []
    for i in range(len(save_route_to_test)):
        aux_extension = os.path.splitext(save_route_to_test[i])
        if aux_extension[1] == save_users_code_extension:
            tests_to_use.append(save_route_to_test[i])
    return tests_to_use

# P6
def check_if_the_code_pass_the_test(route):
    if os.path.exists(route): # Comprobamos que el fichero existe
        files_pattern = r".*\.(py|cc?|rb|js)" # Con esta expresión regular gestionamos los ficheros
        if re.match(files_pattern, route): # En caso de que coincida se procede a evaluar las distintas opciones con las que se haya hecho match
            extension = re.findall(files_pattern, route)[0]  
            if extension == "py": 
                result = subprocess.run(["python3", route], capture_output=True, text=True)
                if result.returncode == 0:
                    return True
                else:
                    return False
            elif extension == "rb":
                result = subprocess.run(["ruby", route], capture_output=True, text=True)
                print(result.stdout)
            elif extension == "js": # Llamamos a los test de JEST y si el returncode es 0 es que ha pasado el test en caso contrario retornamos false
                result = subprocess.run(["jest", route], capture_output=True, text=True)
                if result.returncode == 0:
                    return True
                else:
                    return False
            elif extension == "c" or extension == "cc":
                executable_name = "a.out"
                result = subprocess.run(["g++", route, "-o", executable_name], capture_output=True, text=True)
                if result.returncode == 0: # En caso de que se haya podido compilar ejecutamos el resultado
                    execution_result = subprocess.run([f"./{executable_name}"], capture_output=True, text=True)
                    print(execution_result.stdout)
                else:
                    print("Error de compilación:")
                    print(result.stderr)
        else: # Si no coincide se manda mensaje de error
            return jsonify({'message': "Error, la extensión del archivo no está permitida"}), 400    
    else: # En caso de que el fichero no exista mandamos aviso
        return jsonify({'message': f"Error, El archivo en la ruta \"{route}\" no existe."}), 400

def read_puntuations_regist(block_id, question_id): 
    create_route_to_file = "data/puntuations/" + block_id + "/" + question_id + "_puntuations.json"
    search_enters = r"{(.|\n)*?}"
    search_enter_files = r"\"enter_file\":.*"
    search_result_files = r"\"result_file\":.*"
    search_puntuation = r"\"puntuation\":.*"
    save_enter = ""
    save_objects = []
    if os.path.exists(create_route_to_file): 
        with open(create_route_to_file, 'r') as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                for search in re.finditer(search_enters, content):
                    new_object = {}
                    save_enter_file = ""
                    save_result_file = ""
                    save_puntuation = ""
                    save_enter = search.group()
                    find_enter_file = re.search(search_enter_files, save_enter)
                    find_result_file = re.search(search_result_files, save_enter)
                    find_puntuation = re.search(search_puntuation, save_enter)
                    if find_enter_file:
                        save_enter_file = find_enter_file.group()
                        save_enter_file = save_enter_file[:-1]
                        save_enter_file = save_enter_file.split(": ")[1]
                        new_object["enter_file"] = save_enter_file
                    else:
                        return jsonify({'message': "Error inesperado"}), 400
                    if find_result_file:
                        save_result_file = find_result_file.group()
                        save_result_file = save_result_file[:-1]
                        save_result_file = save_result_file.split(": ")[1]
                        new_object["result_file"] = save_result_file
                    else:
                        return jsonify({'message': "Error inesperado"}), 400
                    if find_puntuation:
                        save_puntuation = find_puntuation.group()
                        save_puntuation = save_puntuation[:-1]
                        save_puntuation = int(save_puntuation.split(": ")[1])
                        new_object["puntuation"] = save_puntuation
                    else:
                        return jsonify({'message': "Error inesperado"}), 400
                    save_objects.append(new_object)
            else:
                return jsonify({'message': "El fichero está vacío"}), 400
    else:
        return jsonify({'message': "No se encontró el fichero"}), 400
    return save_objects

def calculate_puntuation_for_user(username, block_id):
    users_files = save_all_user_routes_files(username, block_id) # P4 # Guardamos todas las entradas del usuario
    all_questions_created = localize_all_questions(block_id) # P5 # Guardamos cuantas preguntas se han creado
    if len(all_questions_created) != len(users_files):
        return jsonify({'message': "Error, hay más entradas por parte del usuario, que preguntas creadas"}), 400
    # APARTIR DE AQUI REVISAR POR QUE NO LO HE PROBADO TODAVÍA
    for i in range(len(all_questions_created)): 
        save_tests_current_questions = read_puntuations_regist(block_id, all_questions_created[i])
        print(save_tests_current_questions)
    """
    for i in range(len(all_questions_created)): # A continuación guardaremos para cada pregunta, todas las pruebas disponibles en base a la entrada
        save_all_test.append(filter_routes_to_tests_for_questions(block_id, all_questions_created[i], users_files[i]))
    save_tests_extension = ""
    for i in range(len(save_all_test)): # Cómo todo los tests tendrán la misma extensión filtro por el primero de ellos
        save_tests_extension = os.path.splitext(save_all_test[i][0])
        save_tests_extension = save_tests_extension[1]
        print(save_tests_extension)
    """


# P7
def regist_user_puntuation(block_id, username, puntuation, time):
    create_route = route_to_rankings_info + block_id + ".json" 
    begin_doc = "[\n"
    username_line = "    {\n        " + "\"username\": \"" + username + "\",\n"
    puntuation_line = "        \"puntuation\": " + str(puntuation) + ",\n" 
    time_line = "        \"time\": " + str(time) + "\n    }"
    new_enter = "},\n"
    end_doc = "\n]" 
    if os.path.exists(create_route):
        with open(create_route, 'r') as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                content = content[:-3]
                with open(create_route, 'w') as file:
                    file.write(content)
                    file.write(new_enter)
                    file.write(username_line)
                    file.write(puntuation_line)
                    file.write(time_line)
                    file.write(end_doc)
            else:
                print(f"Hubo un error inesperado con el fichero de registro de {create_route}") 
    else:
        with open(create_route, 'w') as file:
            file.write(begin_doc)
            file.write(username_line)
            file.write(puntuation_line)
            file.write(time_line)
            file.write(end_doc)

# P8
def procesate_object(string_to_procesate):
    string_to_procesate = string_to_procesate[:-1]
    string_to_procesate = string_to_procesate.split(":")
    second_half = string_to_procesate[1]
    second_half = second_half[1:]
    if second_half.isalpha():
        second_half = float(second_half)
    return second_half

def sort_users_puntuations_file(block_id): # REVISAR???
    create_route = route_to_rankings_info + block_id + ".json"
    search_entrace = r"{(.|\n)*?}"
    search_user = r"\"username\".*?,"
    search_puntuation = r"\"puntuation\".*?,"
    search_time = r"\"time\".*?\n"
    save_objects_users = []
    if os.path.exists(create_route): 
        with open(create_route, 'r') as file:  
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                for entrance in re.finditer(search_entrace, content):
                    save_entrance = entrance.group()
                    find_user = re.search(search_user, save_entrance)
                    save_user = find_user.group()
                    save_user = procesate_object(save_user)
                    find_puntuation = re.search(search_puntuation, save_entrance)
                    save_puntuation = find_puntuation.group()
                    save_puntuation = procesate_object(save_puntuation)
                    find_time = re.search(search_time, save_entrance)
                    save_time = find_time.group()
                    save_time = procesate_object(save_time)
                    new_object = {
                        "username" : save_user,
                        "puntuation": float(save_puntuation),
                        "time": float(save_time)
                    }
                    save_objects_users.append(new_object)
        save_objects_users.sort(key = lambda x: (-x["puntuation"], x["time"]))
        begin_doc = "[\n"
        end_doc = "]"
        with open(create_route, 'w') as file:
                file.write(begin_doc)
                for i in range(len(save_objects_users)):
                    aux_user_name = save_objects_users[i]["username"]
                    aux_puntuation = save_objects_users[i]["puntuation"]
                    aux_time = save_objects_users[i]["time"]
                    file.write("    {\n")
                    file.write(f"        \"username\": {aux_user_name},\n")
                    file.write(f"        \"puntuation\": {aux_puntuation},\n")
                    file.write(f"        \"time\": {aux_time}\n")
                    if i == len(save_objects_users) - 1:
                        file.write("    }\n")
                    else:
                        file.write("    },\n")
                file.write(end_doc)
    else:
        return jsonify({'message': "Error, no se encontró el documento"}), 400
 
# Lecturas de JSON

@app.route('/get-data-blocks-buttons-json', methods=["GET"])
def get_data_blocks_buttons_json():
    if os.path.exists(route_to_json_buttons_blocks): 
        with open(route_to_json_buttons_blocks, 'r') as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                return jsonify({'data': content}), 200
            else:
                pass
    else:
        pass

@app.route('/get-info-users-json', methods=["GET"])
def get_info_users_json():
    if os.path.exists(route_to_info_users_json): 
        with open(route_to_info_users_json, 'r') as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                return jsonify({'data': content}), 200
            else:
                pass
    else:
        pass



if __name__ == '__main__':
    app.run(debug=True)
