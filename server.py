import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil
import re
import subprocess
from datetime import date, time, datetime

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'py', 'c', 'cc', 'rb', 'js'} 

# Rutas a los ficheros de registro de información
route_to_data_json_block_and_question = "data/app_data/data_information_app.json" # RUTA AL JSON QUE REGISTRA LOS BLOQUES Y PREGUNTAS (INFO)
route_to_json_buttons_blocks = "data/app_data/data_blocks_buttons.json" # RUTA AL JSON QUE REGISTRA LA INFO DE LOS BOTONES DE BLOQUES
route_to_json_buttons_questions = "data/app_data/data_questions_buttons.json" # RUTA AL JSON QUE REGISTRA LA INFO DE LOS BOTONES DE QUESTIONS
route_to_info_users_json = "data/users_registered/info_users.json" # RUTA AL JSON QUE GESTIONA LOS USUARIOS
route_to_puntuations = "data/puntuations" # RUTA AL JSON QUE GESTIONA LAS PUNTUACIONES
route_to_student_register = "data/student_register" # RUTA al registro del tiempo de los usuarios
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

@app.route('/create-register-folder-user', methods=["POST"]) # Función que crea la carpeta de registro del usuario
def create_register_folder_user():
    data = request.get_json()
    block_name = data.get('block_name', '')
    block_name = "block_" + block_name
    create_route = route_to_student_register + "/" + block_name
    if os.path.exists(create_route):
        return jsonify({'message': 'Carpeta de registro creada'}), 200
    else:
        route = route_to_student_register
        folder_path = os.path.join(route, block_name)
        os.makedirs(folder_path, exist_ok = True)
        return jsonify({'message': 'Carpeta de registro creada'}), 200

@app.route('/regist-user', methods=["POST"]) # Función que permite registrar al usuario en el registro de un bloque
def regist_user(): 
    data = request.get_json()
    username = data.get('text', '')
    block_name = data.get('block_name', '')
    block_name = "block_" + block_name
    create_route = route_to_student_register + "/" + block_name + "/" + "student_register.json"
    search_user = r"\"username\":.*?\"" + username + "\""
    begin_doc = "[\n"
    begin_new_entry = "  {\n"
    line_user = "    \"username\": \"" + username + "\"\n"
    end_entry = "  }\n"
    end_new_entry = "},\n"
    end_doc = "]"
    if os.path.exists(create_route):  # Comprueba si el archivo existe en la ruta
        with open(create_route, "r") as file:
            lines = file.read()
            content = ''.join(lines)
            content = content[:-3]
            find_user = re.search(search_user, content)
            if find_user: # Para evitar duplicados en caso estar el estudiante registrado se evita continuar
                return jsonify({'message': f'El usuario volvió a entrar'}), 500
            with open(create_route, "w") as file:
                file.write(content)
                file.write(end_new_entry)
                file.write(begin_new_entry)
                file.write(line_user)
                file.write(end_entry)
                file.write(end_doc)
            return jsonify({'message': f'Documento actualizado con éxito'}), 200
    else: 
        with open(create_route, "w") as file:
            file.write(begin_doc)
            file.write(begin_new_entry)
            file.write(line_user)
            file.write(end_entry)
            file.write(end_doc)
            return jsonify({'message': f'Carpeta creada con éxito en {create_route}'}), 200
    
@app.route('/create-question-folder-user', methods=["POST"]) # Función para crear la carpeta de preguntas del usuario
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

        if (os.listdir(folder_path)): # En caso de que el usuario suba más de un código se borra el que ya estaba ahí
            save_name = os.listdir(folder_path)[0]
            temporal_path = folder_path + "/" + save_name
            os.unlink(temporal_path)

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
     
@app.route('/create-block-folder-admin-for-puntuations', methods=["POST"]) # Creación de la carpeta de puntuaciones
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
    
@app.route('/regist-block-admin', methods=["POST"]) # Función para registrar un bloque
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

@app.route('/regist-block-button', methods=["POST"]) # Función para registrar el botón de un bloque
def regist_block_button():
    data = request.get_json()
    button_id = data.get('text', '')
    positionX = data.get('positionX', '')
    positionY = data.get('positionY', '')
    type = data.get('type', '')
    block_name = data.get('block_name', '')
    default_image = data.get('default_image', '')

    begin_document = "[\n"
    begin_entry = "    {\n"
    line_id = f"        \"id\": {button_id},\n"
    line_positionX = f"        \"positionX\": {positionX},\n"
    line_positionY = f"        \"positionY\": {positionY},\n"
    line_type = f"        \"type\": \"{type}\",\n"
    line_block_name = f"        \"block_name\": \"{block_name}\",\n"
    line_default_image = f"        \"default_image\": \"{default_image}\"\n"
    end_entry = "    }"
    end_document = "\n]"
    content = begin_entry + line_id + line_positionX + line_positionY + line_type + line_block_name + line_default_image + end_entry
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
    
@app.route('/regist-question-admin', methods=["POST"]) # Función para registrar una pregunta
def regist_question_admin():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    tittle = data.get('tittle', '')
    description = data.get('description','')
    search_block = r"(.|\n)*\"block_" + str(block_id) + r"(.|\n)*?}"
    search_question = r"(.|\n)*\"block_" + str(block_id) + r"(.|\n)*?\"question_" + str(question_id) + r"(.|\n)*?}"
    previous_id = int(question_id) - 1
    search_question_before = r"(.|\n)*\"block_" + str(block_id) + r"(.|\n)*?\"question_" + str(previous_id) + r"(.|\n)*?}"
    search_block_and_img = r"(.|\n)*\"block_" + str(block_id) + r"(.|\n)*?\"img\":.*"
    question_line = "      \"question_" + str(question_id) + "\": {\n"
    tittle_line = "        \"tittle\": \"" + tittle + "\",\n"
    description_line = "        \"description\": \"" + description + "\"\n"
    end_question = "      }\n"
    end_updated_question = "      }"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_data_json_block_and_question):
        with open(route_to_data_json_block_and_question, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_question = re.search(search_question, content)
                if find_question: # Opción para actualizar la pregunta
                    find_previous_question = re.search(search_question_before, content)
                    if find_previous_question: # Existe al menos una pregunta
                        first_middle = content[:find_previous_question.end()]
                        new_content = ",\n" + question_line + tittle_line + description_line + end_updated_question
                        second_middle = content[find_question.end():]
                        final_json = first_middle + new_content + second_middle
                        with open(route_to_data_json_block_and_question, "w") as file:
                            file.write(final_json)
                        return jsonify({'message':'Pregunta actualizada'}), 200
                    else: # Es la primera pregunta
                        find_block = re.search(search_block, content)
                        find_block_img = re.search(search_block_and_img, content)
                        if find_block and find_block_img:
                            first_middle = content[:find_block_img.end()]
                            new_content = "\n" + question_line + tittle_line + description_line + end_updated_question
                            second_middle = content[find_block.end():]
                            final_json = first_middle + new_content + second_middle
                            with open(route_to_data_json_block_and_question, "w") as file:
                                file.write(final_json)
                            return jsonify({'message':'Pregunta actualizada'}), 200
                        else:
                            return jsonify({'message':'Error, hubo un problema al intentar acceder a los contenidos del bloque'}), 400
                else: # Opción de añadir la pregunta
                    find_previous_question = re.search(search_question_before, content)
                    if find_previous_question: # Existe al menos una pregunta
                        first_middle = content[:find_previous_question.end()]
                        new_content = ",\n" + question_line + tittle_line + description_line + end_question
                        second_middle = content[find_previous_question.end() + 1:]
                        final_json = first_middle + new_content + second_middle
                        with open(route_to_data_json_block_and_question, "w") as file:
                            file.write(final_json)
                        return jsonify({'message':'Pregunta añadida'}), 200
                    else: # Primera pregunta
                        find_block_img = re.search(search_block_and_img, content)
                        if find_block_img:
                            first_middle = content[:find_block_img.end()]
                            new_content = ",\n" + question_line + tittle_line + description_line + end_question
                            second_middle = content[find_block_img.end() + 1:]
                            final_json = first_middle + new_content + second_middle
                            with open(route_to_data_json_block_and_question, "w") as file:
                                file.write(final_json)
                            return jsonify({'message':'Pregunta añadida'}), 200
                        else:
                            return jsonify({'message':'Error, al intentar añadir nueva entrada'}), 400
    else:
        return jsonify({'message':'Error, no se encontró el documento'}), 400
    

@app.route('/regist-question-button', methods=["POST"]) # Función para registrar un botón de pregunta
def regist_question_button():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    label = data.get('label', '')
    name = data.get('name', '')
    search_block = r"\"block_" + str(block_id) + r"(.|\n)*?}(\s|\n)*?}"
    search_only_block = r"(.|\n)*?\"block_" + str(block_id) + r"(.|\n)*?}"
    previous_id = int(question_id) - 1
    search_previous_question = r"(.|\n)*?\"block_" + str(block_id) + r"(.|\n)*?\"question_" + str(previous_id) + r"\"(.|\n)*?}"
    begin_doc = "{\n"
    begin_block = "  \"block_" + str(block_id) + "\": {\n"
    begin_question = "    \"question_" + str(question_id) + "\": {\n"
    id_line = "      \"id\": " + str(question_id) + ",\n"
    label_line = "      \"label\": \"" + label + "\",\n"
    name_line = "      \"name\": \"" + name + "\"\n" 
    end_question = "    }\n"
    end_block = "  }\n"
    end_doc = "}"
    first_midle = ""
    second_midle = ""
    final_json = ""
    if os.path.exists(route_to_json_buttons_questions):
        with open(route_to_json_buttons_questions, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_block = re.search(search_block, content)
                if find_block:
                    find_previous_question = re.search(search_previous_question, content)
                    if find_previous_question:
                        first_midle = content[:find_previous_question.end()]
                        new_content = ",\n" + begin_question + id_line + label_line + name_line + end_question
                        second_midle = content[find_previous_question.end() + 1:]
                        final_json = first_midle + new_content + second_midle
                        with open(route_to_json_buttons_questions, "w") as file:
                           file.write(final_json)
                        return jsonify({'message': f'Botón registrado'}), 200
                    else:
                        find_only_block = re.search(search_only_block, content)
                        first_midle = content[:find_only_block.end() - 3]
                        new_content = begin_question + id_line + label_line + name_line + end_question
                        second_midle = content[find_only_block.end() - 3:]
                        final_json = first_midle + new_content + second_midle
                        with open(route_to_json_buttons_questions, "w") as file:
                           file.write(final_json)
                        return jsonify({'message': f'Botón registrado'}), 200
                else:
                    if content == "{\n}":
                        content = content[:-2]
                        new_content = content + "\n" + begin_block + begin_question + id_line + label_line + name_line + end_question + end_block + end_doc
                        with open(route_to_json_buttons_questions, "w") as file:
                            file.write(new_content)
                        return jsonify({'message': f'Botón registrado'}), 200
                    else:
                        content = content[:-2]
                        new_content = content + ",\n" + begin_block + begin_question + id_line + label_line + name_line + end_question + end_block + end_doc
                        with open(route_to_json_buttons_questions, "w") as file:
                            file.write(new_content)
                        return jsonify({'message': f'Botón registrado'}), 200
    else:
        new_content = begin_doc + begin_block + begin_question + id_line + label_line + name_line + end_question + end_block + end_doc
        with open(route_to_json_buttons_questions, "w") as file:
            file.write(new_content)
        return jsonify({'message': f'Archivo creado'}), 200
 
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
        enter_file = f"    \"enter_file\": \"data/blocks/{block_name}/{question_name}/{input_files[index].filename}\",\n"
        result_file = f"    \"result_file\": \"data/blocks/{block_name}/{question_name}/{result_files[index].filename}\",\n"
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
def delete_selected_test(): 
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
            shutil.rmtree(folder_path)
            remove_block_folder_from_users(block_dir) 
        return jsonify({'message': f'Carpeta eliminada con éxito en {folder_path}'}), 200
    else:
        return jsonify({'message': 'Texto vacío, no se puede eliminar carpeta'}), 400

def remove_block_folder_from_users(block_name): # Función que elimina la carpeta de ese mismo bloque de todos los usuarios
    save_route_users = os.listdir(route_to_users_input)
    for i in range(len(save_route_users)):
        create_route = route_to_users_input + "/" + save_route_users[i] + "/" + block_name
        if os.path.exists(create_route):
            shutil.rmtree(create_route)
     
@app.route('/delete-last-student-register', methods=["POST"]) # Eliminar la carpeta del último bloque de preguntas del registro de estudiantes
def delete_last_student_register():
    data = request.get_json()  
    block_name = data.get('text', '') 
    block_dir = "block_" + block_name
    if block_name:
        route = 'data/student_register/'
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
                remove_question_folder_from_users(block_name, question_name)
            return jsonify({'message': f'Carpeta de pregunta {question_name} eliminada con éxito'}), 200
        except Exception as e:
            return jsonify({'message': f'Error al eliminar contenido: {str(e)}'}), 500
        
def remove_question_folder_from_users(block_name, question_name):
    save_route_users = os.listdir(route_to_users_input)
    for i in range(len(save_route_users)):
        create_route = route_to_users_input + "/" + save_route_users[i] + "/" + block_name + "/" + question_name
        if os.path.exists(create_route):
            shutil.rmtree(create_route)

@app.route('/delete-question-regist-admin', methods=["POST"])
def delete_question_regist_admin():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    search_block = r"(.|\n)*?\"block_" + str(block_id) + r"\"(.|\n)*?}(\n|\s)*?}"
    previous_id = int(question_id) - 1
    search_question = r"(.|\n)*?\"block_" + str(block_id) + r"\"(.|\n)*?\"question_" + str(question_id) + r"(.|\n)*?}"
    search_question_before = r"(.|\n)*?\"block_" + str(block_id) + r"\"(.|\n)*?\"question_" + str(previous_id) + r"(.|\n)*?}"
    search_img = r"(.|\n)*?\"block_" + str(block_id) + r"\"(.|\n)*?\"img\".*?,"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_data_json_block_and_question):
        with open(route_to_data_json_block_and_question, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_block = re.search(search_block, content)
                if find_block:
                    find_question = re.search(search_question, content)
                    if not find_question:
                        return jsonify({'message': f'Error, no se encontró la pregunta a borrar'}), 500
                    question_id = int(question_id)
                    if question_id != 1:
                        find_question_before = re.search(search_question_before, content)
                        first_middle = content[:find_question_before.end()]
                        new_end = "\n    }"
                        second_middle = content[find_block.end():]
                        final_json = first_middle + new_end + second_middle
                        with open(route_to_data_json_block_and_question, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': f'Última pregunta eliminada del JSON de registro'}), 200
                    else:
                        find_img = re.search(search_img, content)
                        first_middle = content[:find_img.end() - 1]
                        new_end = "\n    }"
                        second_middle = content[find_block.end():]
                        final_json = first_middle + new_end + second_middle
                        with open(route_to_data_json_block_and_question, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': f'Última pregunta eliminada del JSON de registro'}), 200
                else:
                    return jsonify({'message': f'Error, no encontró el bloque'}), 400
    else:
        return jsonify({'message': f'Error, no encontró el fichero de registro'}), 400
 
@app.route('/delete-question-button-json', methods=["POST"])
def delete_question_button_json():
    data = request.get_json()  
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    search_block = r"(.|\n)*?\"block_" + str(block_id) + r"(.|\n)*?}(\s|\n)*?}"
    search_begin_block = r"(.|\n)*?\"block_" + str(block_id) + r"(.|\n)*?{"
    previous_id = int(question_id) - 1
    search_previous_question = r"(.|\n)*?\"block_" + str(block_id) + r"(.|\n)*?\"question_" + str(previous_id) + r"\"(.|\n)*?}"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_json_buttons_questions):
        with open(route_to_json_buttons_questions, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_block = re.search(search_block, content)
                if find_block:
                    find_previous_question = re.search(search_previous_question, content)
                    if find_previous_question:
                        first_middle = content[:find_previous_question.end()]
                        second_middle = content[find_block.end() - 4:]
                        final_json = first_middle + second_middle
                        with open(route_to_json_buttons_questions, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': f'Botón eliminado'}), 200
                    else:
                        find_begin_block = re.search(search_begin_block, content)
                        if find_begin_block:
                            first_middle = content[:find_begin_block.end()]
                            second_middle = content[find_block.end() - 4:]
                            final_json = first_middle + second_middle
                            with open(route_to_json_buttons_questions, "w") as file:
                                file.write(final_json)
                            return jsonify({'message': f'Botón eliminado'}), 200
                        else:
                            return jsonify({'message': f'Error al intentar localizar el bloque'}), 400
                else:
                    return jsonify({'message': f'Error, no se encontró el bloque de donde eliminar'}), 400
    else:
        return jsonify({'message': f'Error, no se encontró el archivo de registro'}), 400

@app.route('/delete-block-in-question-button-json', methods=["POST"])
def delete_block_in_question_button_json():
    data = request.get_json()  
    block_id = data.get('text', '')
    search_block = r"\"block_" + str(block_id) + r"\"(.|\n)*?}(\s|\n)*?},?"
    search_empty_block = r"\"block_" + str(block_id) + r"\".*?{(\s|\n)*?},?"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_json_buttons_questions):
        with open(route_to_json_buttons_questions, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_empty_block = re.search(search_empty_block, content)
                if find_empty_block:
                    first_middle = content[:find_empty_block.start() - 3]
                    second_middle = content[find_empty_block.end():]
                    final_json = first_middle + second_middle
                    save_final = final_json[-3:]
                    if save_final == ",\n}":
                        final_json = final_json[:-3]
                        final_json += "\n}"
                    with open(route_to_json_buttons_questions, "w") as file:
                        file.write(final_json)
                    return jsonify({'message': f'Bloque eliminado del registro de botones de pregunta'}), 200
                else:
                    find_block = re.search(search_block, content)
                    if find_block:
                        first_middle = content[:find_block.start() - 3]
                        second_middle = content[find_block.end():]
                        final_json = first_middle + second_middle
                        save_final = final_json[-3:]
                        if save_final == ",\n}":
                            final_json = final_json[:-3]
                            final_json += "\n}"
                        with open(route_to_json_buttons_questions, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': f'Bloque eliminado del registro de botones de pregunta'}), 200
                    else:
                        return jsonify({'message': f'Error, no se encontró el bloque a eliminar'}), 500
    else:
        return jsonify({'message': f'Error, no se encontró el archivo de registro'}), 400

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
    folder_path = 'data/users_registered/info_users.json'
    default_begin_doc = "[\n    {\n"
    default_username = "      \"username\": \"admin\",\n"
    default_password = "      \"password\": \"1234\",\n"
    default_rol = "      \"rol\": \"ADMIN\",\n"
    default_id = "      \"id\": 0,\n"
    default_position_x = "      \"positionX\": 0,\n"
    default_position_y = "      \"positionY\": 0\n"
    default_end_doc = "    }\n]"

    if os.path.exists(folder_path):
        with open(folder_path, "w") as file:
            file.write(default_begin_doc)
            file.write(default_username)
            file.write(default_password)
            file.write(default_rol)
            file.write(default_id)
            file.write(default_position_x)
            file.write(default_position_y)
            file.write(default_end_doc)
        return jsonify({'message': 'Información de usuarios registrados eliminada con éxito'}), 200
    else:
        return jsonify({'message': 'No se localizó el archivo de registro de usuarios'}), 500

@app.route('/add-new-user', methods=['POST']) # Añadir un nuevo usuario ya sea administrador o monitor
def add_new_user():
    data = request.get_json()  
    username = data.get('text', '')  
    password = data.get('password', '')
    rol = data.get('rol', '')
    offsetX = data.get('offsetX', '')
    offsetY = data.get('offsetY', '')
    limit_position = data.get('limit_position', '')
    begin_doc = "[\n"
    first_line = ",\n"
    username_line = "    {\n      \"username\": \"" + username + "\",\n"
    password_line = "      \"password\": \"" + password + "\",\n"
    rol_line = "      \"rol\": \"" + rol + "\",\n"
    end_line = "    }\n]"
    search_user = r"\"username\":\s*\"" + username + r"\""
    search_if_is_the_user_admin = r"admin"
    search_last_enter = r"{(.|\n)*?}"
    search_enter = r"{\n\s*?\"username\": \"" + username + r"\"(.|\n)*?}"
    search_positionX = r"\"positionX.*"
    search_positionY = r"\"positionY.*"
    search_id = r"\"id.*"
    search_rol = r"\"rol.*"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(route_to_info_users_json):
        with open(route_to_info_users_json, 'r') as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_if_user_exist = re.search(search_user, content)
                if find_if_user_exist:
                    save_user = find_if_user_exist.group()
                    find_if_is_admin_user = re.search(search_if_is_the_user_admin, save_user)
                    if find_if_is_admin_user:
                        find_enter = re.search(search_enter, content)
                        save_enter = find_enter.group()
                        find_rol = re.search(search_rol, save_enter)
                        save_rol = find_rol.group()[:-1].split(": ")[1].split('"')[1]
                        if rol != save_rol:
                            return jsonify({'message': "Por motivos de seguridad no se podrá modificar el rol de este usuario"}), 400
                        find_id = re.search(search_id, find_enter.group())
                        find_position_X = re.search(search_positionX, find_enter.group())
                        find_position_Y = re.search(search_positionY, find_enter.group())
                        new_line_id = "      " + find_id.group() + "\n"
                        new_line_positionX = "      " + find_position_X.group() + "\n"
                        new_line_positionY = "      " + find_position_Y.group() + "\n    }"
                        first_middle = content[:find_enter.start() - 4]
                        new_content = username_line + password_line + rol_line + new_line_id + new_line_positionX + new_line_positionY
                        second_middle = content[find_enter.end():]
                        final_json = first_middle + new_content + second_middle
                        with open(route_to_info_users_json, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': "Usuario actualizado"}), 200
                    else:
                        find_enter = re.search(search_enter, content)
                        find_id = re.search(search_id, find_enter.group())
                        find_position_X = re.search(search_positionX, find_enter.group())
                        find_position_Y = re.search(search_positionY, find_enter.group())
                        new_line_id = "      " + find_id.group() + "\n"
                        new_line_positionX = "      " + find_position_X.group() + "\n"
                        new_line_positionY = "      " + find_position_Y.group() + "\n    }"
                        first_middle = content[:find_enter.start() - 4]
                        new_content = username_line + password_line + rol_line + new_line_id + new_line_positionX + new_line_positionY
                        second_middle = content[find_enter.end():]
                        final_json = first_middle + new_content + second_middle
                        with open(route_to_info_users_json, "w") as file:
                            file.write(final_json)
                        return jsonify({'message': "Usuario actualizado"}), 200
                else: 
                    find_last_enter = re.search(search_last_enter, content)
                    if find_last_enter:
                        save_last_enter = ""
                        for match in re.finditer(search_last_enter, content):
                            save_last_enter = match.group()
                        find_positionX = re.search(search_positionX, save_last_enter)
                        save_position_X = find_positionX.group()
                        save_position_X = int(save_position_X[:-1].split(": ")[1])
                        find_positionY = re.search(search_positionY, save_last_enter)
                        save_position_Y = find_positionY.group()
                        save_position_Y = int(save_position_Y.split(": ")[1])
                        find_id = re.search(search_id, save_last_enter)
                        save_id = find_id.group()
                        save_id = int(save_id[:-1].split(": ")[1])
                        save_id += 1
                        if (save_position_X + offsetX) > limit_position:
                            save_position_X = 0
                            save_position_Y += offsetY
                        else:
                            save_position_X += offsetX
                        id_line = "      \"id\": " + str(save_id) + ",\n"
                        position_x_line = "      \"positionX\": " + str(save_position_X) + ",\n"
                        position_y_line = "      \"positionY\": " + str(save_position_Y) + "\n"
                        content = content[:-2]
                        with open(route_to_info_users_json, 'w') as file:
                            file.write(content)  # Escribimos las líneas originales menos las 2 últimas
                            file.write(first_line)  # Añadimos el comienzo del objeto
                            file.write(username_line)
                            file.write(password_line)
                            file.write(rol_line)
                            file.write(id_line)
                            file.write(position_x_line)
                            file.write(position_y_line)
                            file.write(end_line)  # Añadimos el final del documento
                        return jsonify({'message': "Usuario registrado con éxito"}), 200
                    else:
                        return jsonify({'message': "Error inesperado"}), 400
            else:
                return jsonify({'message': "Error, documento vacío"}), 400
    else:
        id_line = "      \"id\": 0,\n"
        position_x_line = "      \"positionX\": 0,\n"
        position_y_line = "      \"positionY\": 0\n"
        with open(route_to_info_users_json, 'w') as file:
            file.write(begin_doc)  # Añadimos el comienzo del objeto
            file.write(username_line)
            file.write(password_line)
            file.write(rol_line)
            file.write(id_line)
            file.write(position_x_line)
            file.write(position_y_line)
            file.write(end_line)  # Añadimos el final del documento
            return jsonify({'message': "Archivo de registro de usuarios creado"}), 200
 
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

def get_user_file(user_name, block_id, question_name): # Función que devuelve el archivo del usuario
    users_file = ""
    create_route_files = route_to_users_input + "/" + user_name + "/" + block_id + "/" + question_name # Comprobamos que la dirección del usuario existe
    if os.path.exists(create_route_files): 
        users_file = os.listdir(create_route_files)[0]
        users_file = create_route_files + "/" + users_file
    else:
        return jsonify({'message': 'Hubo un error durante el procesado de los datos, vuelva a intentarlo'}), 400     
    return users_file

@app.route('/localize-all-questions-server', methods=["POST"]) # Función para localizar todas las preguntas creadas
def localize_all_questions_server():
    data = request.get_json()
    block_name = data.get('text', '')
    final_json = "[\n"
    all_questions = []
    route_to_tests = route_to_admins_and_monitors_tests + "/" + block_name # Guardamos la dirección a los tests
    if os.path.exists(route_to_tests): 
        save_route_to_questions = os.listdir(route_to_tests)
        for i in range(len(save_route_to_questions)):
            all_questions.append(save_route_to_questions[i])
        all_questions.sort()
        for i in range(len(all_questions)):
            new_entrance = "  {\n    \"question_id\": \"Pregunta " + str(all_questions[i][-1]) + "\"\n  },\n"
            final_json += new_entrance  
        final_json = final_json[:-2]
        final_json += "\n]" 
        return jsonify({'data': final_json}), 200    
    else:
        return jsonify({'message': "No se han creado preguntas para este ranking"}), 500

def read_puntuations_regist(block_id, question_id): # Función para leer las puntuaciones de un bloque
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

def procesate_object(string_to_procesate): # Función para procesar la información de un objeto
    string_to_procesate = string_to_procesate[:-1]
    string_to_procesate = string_to_procesate.split(":")
    second_half = string_to_procesate[1]
    second_half = second_half[1:]
    if second_half.isalpha():
        second_half = float(second_half)
    return second_half

@app.route('/correct-user-enter', methods=["POST"]) # Función para corregir la entrada de un usuario
def correct_user_enter():
    data = request.get_json()  
    username = data.get('text', '')
    block_name = data.get('block_name', '')
    question_id = data.get('question_id', '')
    question_name = data.get('question_name', '')
    total_points = 0
    users_file = get_user_file(username, block_name, question_name)
    if len(users_file) == 0:
        return jsonify({'message': "Error, no se encontró la entrada del usuario"}), 400
    save_tests_current_question = read_puntuations_regist(block_name, question_name)
    if len(save_tests_current_question) == 0:
        return jsonify({'message': "Error, no se encontraron pruebas"}), 400
    for i in range(len(save_tests_current_question)):
        temporal_save_enter_file = save_tests_current_question[i]["enter_file"].split('"')[1]
        temporal_save_result_file = save_tests_current_question[i]["result_file"].split('"')[1]
        temporal_save_points = save_tests_current_question[i]["puntuation"]
        total_points += temporal_save_points
        if check_if_the_code_pass_the_test(users_file, temporal_save_enter_file, temporal_save_result_file) == False:
            regist_question_correct_time(block_name, question_id, username, total_points, False)
            sort_users_questions_by_points_and_time(block_name)
            return jsonify({'data': False}), 200
    regist_question_correct_time(block_name, question_id, username, total_points, True)
    sort_users_questions_by_points_and_time(block_name)
    return jsonify({'data': True}), 200

def regist_question_correct_time(block_id, question_id, user, points, question_is_correct): # Función para registrar la información de un usuario en el "student_register"
    create_route = route_to_student_register + "/" + block_id + "/" + "student_register.json"
    search_user = r"(.|\n)*?{\n\s*\"username\": \"" + user + r".*"
    search_not_questions = r"(.|\n)*?{\n\s*\"username\": \"" + user + r".*(\s|\n)*?}"
    search_question = r"(.|\n)*?{\n\s*\"username\": \"" + user + r"\"(.|\n)*?\"question_" + str(question_id) + r"\"(.|\n)*?}"
    search_beggining_question = r"(.|\n)*?{\n\s*\"username\": \"" + user + r"\"(.|\n)*?\"question_" + str(question_id) + r"\"(.|\n)*?{"
    search_last_question_user = r"(.|\n)*?{\n\s*\"username\": \"" + user + r"\"(.|\n)*?\"question_(.|\n)*?}(\s|\n)*?}"
    first_middle = ""
    second_middle = ""
    final_json = ""
    if os.path.exists(create_route): # Comprobamos que el fichero existe
        with open(create_route, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines: # En caso de tener el contenido verificamos que el usuario existe
                find_user = re.search(search_user, content)
                if find_user: # El usuario existe
                    find_not_question = re.search(search_not_questions, content) # buscamos que no haya registros del usuario para añadir el primero
                    if find_not_question: # añadir la primera entrada
                        if question_is_correct:
                            time = str(datetime.now())
                            first_middle = content[:find_not_question.end() - 4]
                            new_question = ",\n    \"question_" + str(question_id) + "\": {\n"
                            new_points = "      \"points\": " + str(points) + ",\n"
                            new_time = "      \"time\": \"" + time + "\"\n"
                            new_end_question = "    }"
                            second_middle = content[find_not_question.end() - 4:]
                            final_json = first_middle + new_question + new_points + new_time + new_end_question + second_middle
                            with open(create_route, "w") as file:
                                file.write(final_json)
                        else:
                            time = str(datetime(9000, 12, 31, 23, 59, 59))
                            first_middle = content[:find_not_question.end() - 4]
                            new_question = ",\n    \"question_" + str(question_id) + "\": {\n"
                            new_points = "      \"points\": " + str(points) + ",\n"
                            new_time = "      \"time\": \"" + time + "\"\n"
                            new_end_question = "    }"
                            second_middle = content[find_not_question.end() - 4:]
                            final_json = first_middle + new_question + new_points + new_time + new_end_question + second_middle
                            with open(create_route, "w") as file:
                                file.write(final_json)
                    else: # Actualizar o añadir más entradas
                        find_last_question = re.search(search_last_question_user, content)
                        save_content = find_last_question.group()
                        find_question = re.search(search_question, save_content)
                        if find_question: # Actualizar
                            find_only_beggining = re.search(search_beggining_question, content)
                            if question_is_correct:
                                time = str(datetime.now())
                                first_middle = content[:find_only_beggining.end()]
                                new_points = "\n      \"points\": " + str(points) + ",\n"
                                new_time = "      \"time\": \"" + time + "\"\n"
                                new_end_question = "    }"
                                second_middle = content[find_question.end():]
                                final_json = first_middle + new_points + new_time + new_end_question + second_middle
                                with open(create_route, "w") as file:
                                    file.write(final_json)
                            else:
                                time = str(datetime(9000, 12, 31, 23, 59, 59))
                                first_middle = content[:find_only_beggining.end()]
                                new_points = "\n      \"points\": " + str(points) + ",\n"
                                new_time = "      \"time\": \"" + time + "\"\n"
                                new_end_question = "    }"
                                second_middle = content[find_question.end():]
                                final_json = first_middle + new_points + new_time + new_end_question + second_middle
                                with open(create_route, "w") as file:
                                    file.write(final_json)
                        else: # Añadir
                            if find_last_question: # Se busca la última pregunta y se añade la misma
                                if question_is_correct:
                                    time = str(datetime.now())
                                    first_middle = content[:find_last_question.end() - 4]
                                    new_question = ",\n    \"question_" + str(question_id) + "\": {\n"
                                    new_points = "      \"points\": " + str(points) + ",\n"
                                    new_time = "      \"time\": \"" + time + "\"\n"
                                    new_end_question = "    }"
                                    second_middle = content[find_last_question.end() - 4:]
                                    final_json = first_middle + new_question + new_points + new_time + new_end_question + second_middle
                                    with open(create_route, "w") as file:
                                        file.write(final_json)
                                else:
                                    time = str(datetime(9000, 12, 31, 23, 59, 59))
                                    first_middle = content[:find_user.end() - 4]
                                    new_question = ",\n    \"question_" + str(question_id) + "\": {\n"
                                    new_points = "      \"points\": " + str(points) + ",\n"
                                    new_time = "      \"time\": \"" + time + "\"\n"
                                    new_end_question = "    }"
                                    second_middle = content[find_user.end() - 4:]
                                    final_json = first_middle + new_question + new_points + new_time + new_end_question + second_middle
                                    with open(create_route, "w") as file:
                                        file.write(final_json)
                            else:
                                return jsonify({'message': "Error inesperado"}), 400
                else:
                    return jsonify({'message': "Error, no se encontró al usuario"}), 400
    else:
        return jsonify({'message': "Error, no se encontró el archivo de registro"}), 400

def sort_users_questions_by_points_and_time(block_name): # Función para ordenar las preguntas de un JSON de registro
    create_route = route_to_student_register + "/" + block_name + "/" + "student_register.json"
    search_only_user_enter = r"{(\s|\n)*?\"username\":.*(\s|\n)*?}" # busca bien cuando solo hay un nombre
    search_complete_enters = r"{(\s|\n)*?\"username\"(.|\n)*?}(\s|\n)*?}" # busca bien cuando es la entrada completa
    search_points = r"\"points\".*"
    search_time = r"\"time\".*"
    procesate_non_info_users = []
    regist_to_order = []
    ordered_json = "[\n"
    if os.path.exists(create_route):
        with open(create_route, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                for enter in re.finditer(search_only_user_enter, content): # guardamos los usuarios que no tengan info registrada
                    save_enter = enter.group()
                    procesate_non_info_users.append(save_enter)
                for enter in re.finditer(search_complete_enters, content): # Localizamos cada entrada de los usuarios con info registrada
                    save_enter = enter.group()
                    aux_points = 0
                    minimun_time = None
                    save_time = ""
                    for points in re.finditer(search_points, save_enter): # Calculamos el total de puntos
                        get_points = points.group()
                        get_points = get_points[:-1].split(": ")[1]
                        aux_points += int(get_points)
                    for time in re.finditer(search_time, save_enter): # Calculamos el total de puntos
                        get_time = time.group()
                        get_time = get_time.split(": ")[1]
                        get_time = get_time[1:].split(".")[0] # quitamos los microsegundos y las "" iniciales
                        if get_time[-1] == "\"":
                            get_time = get_time[:-1]
                        save_time = datetime.strptime(get_time, '%Y-%m-%d %H:%M:%S')
                        if minimun_time is None or save_time < minimun_time:
                            minimun_time = save_time
                    regist_to_order.append([save_enter, aux_points, minimun_time])
        regist_to_order.sort(key=lambda x: (-x[1], x[2])) # Ordenamos en base a los mismos

        for i in range(len(regist_to_order)):
            ordered_json += "  " + regist_to_order[i][0] + ",\n"

        if len(procesate_non_info_users) == 0: # En caso de no haber, se establece el final del JSON
            ordered_json = ordered_json[:-2]
            ordered_json += "\n]"
        else: # si si hay se procesa toda la información
            for i in range(len(procesate_non_info_users)):
                if i != len(procesate_non_info_users) - 1:
                    ordered_json += "  " + procesate_non_info_users[i] + ",\n"
                else:
                    ordered_json += "  " + procesate_non_info_users[i] + "\n]"
        with open(create_route, "w") as file: # registramos la información final ordenada por puntos
            file.write(ordered_json)
    else:
        return jsonify({'message': "Error, no se localizó el archivo"}), 400

def check_if_the_code_pass_the_test(user_file, admin_enter, admin_result): # Función que ejecuta las entradas de los usuarios para comprobar si son correctas
    save_result = ""
    with open(admin_result, "r") as file:
        save_result = file.readlines()
        save_result = ''.join(save_result)
    result = ""
    if os.path.exists(user_file): # Comprobamos que el fichero existe
        files_pattern = r".*\.(py|cc?|rb|js)" # Con esta expresión regular gestionamos los ficheros
        if re.match(files_pattern, user_file): # En caso de que coincida se procede a evaluar las distintas opciones con las que se haya hecho match
            extension = re.findall(files_pattern, user_file)[0]  
            if extension == "py": # Funciona
                result = subprocess.run(["python3", user_file, admin_enter], capture_output = True, text = True)
                result = result.stdout
                result = result[:-1] # Eliminamos el salto de línea que se genera por defect
            elif extension == "rb": # Funciona
                result = subprocess.run(["ruby", user_file, admin_enter], capture_output = True, text = True)
                result = result.stdout
                result = result[:-1] # Eliminamos el salto de línea que se genera por defect
            elif extension == "js": # Funciona
                result = subprocess.run(["node", user_file, admin_enter], capture_output = True, text = True)
                result = result.stdout
                result = result[:-1] # Eliminamos el salto de línea que se genera por defect
            elif extension == "c": # Funciona
                delete_file_name = user_file.split("/")[:-1]
                executable_name = '/'.join(delete_file_name) + "/a.out"
                correct_compilation = subprocess.run(["g++", user_file, "-o", executable_name], capture_output = True)
                if correct_compilation.returncode == 0: # En caso de que se haya podido compilar ejecutamos el resultado
                    result = subprocess.run([f"./{executable_name}", admin_enter], capture_output = True, text = True)
                    result = result.stdout
                    result = result[:-1] # Eliminamos el salto de línea que se genera por defecto
                    os.unlink(executable_name) # Eliminamos el ejecutable resultante
                else:
                    return False
            elif extension == "cc": # Funciona
                delete_file_name = user_file.split("/")[:-1]
                executable_name = '/'.join(delete_file_name) + "/a.out"
                correct_compilation = subprocess.run(["g++", user_file, "-o", executable_name], capture_output = True)
                if correct_compilation.returncode == 0: # En caso de que se haya podido compilar ejecutamos el resultado
                    result = subprocess.run([f"./{executable_name}", admin_enter], capture_output = True, text = True)
                    result = result.stdout
                    result = result[:-1]
                    os.unlink(executable_name) # Eliminamos el ejecutable resultante
                else:
                    return False
        else: # Si no coincide se retorna como falso (no está admitido)
            return False

        if result == save_result:
            return True
        else:
            return False
    else: # En caso de que el fichero no exista mandamos aviso
        return jsonify({'message': "Error inesperado"}), 400

 
# Lecturas de JSON
@app.route('/get-data-blocks-buttons-json', methods=["GET"]) # Recuperamos la información del archivo de registro de los botones de bloque
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

@app.route('/get-info-users-json', methods=["GET"]) # Recuperamos la información del archivo de registro de usuarios
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
 

@app.route('/get-info-student-register', methods=["POST"]) # Recuperamos los JSONs de registro de los rankings
def get_info_student_register():
    data = request.get_json()
    block_name = data.get('text', '')
    create_route = route_to_student_register + "/" + block_name + "/" + "student_register.json"
    if os.path.exists(create_route):
        with open(create_route, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                return jsonify({'data': content}), 200
            else:
                return jsonify({'message': "Error, el archivo está vacío"}), 400
    else:
        return jsonify({'message': f"Error, no se encontró la información de los rankins del {block_name}"}), 500

@app.route('/get-user-information', methods=["POST"]) # Función para recibir la información de un usuario
def get_user_information():
    data = request.get_json()
    id = data.get('text', '')
    search_enter = r"{(.|\n)*?}"
    search_id = r"\"id\": " + str(id)
    search_name = r"\"username\".*"
    search_password = r"\"password\".*"
    search_rol = r"\"rol\".*"
    line_begin_info = "{\n"
    empty_user_line = "  \"username\": \"\",\n"
    empty_password_line = "  \"password\": \"\",\n"
    empty_rol_line = "  \"rol\": \"\""
    line_end_info = "\n}"
    if os.path.exists(route_to_info_users_json):
        with open(route_to_info_users_json, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                for enter in re.finditer(search_enter, content):
                    save_enter = enter.group()
                    find_id = re.search(search_id, save_enter)
                    find_name = re.search(search_name, save_enter)
                    find_password = re.search(search_password, save_enter)
                    find_rol = re.search(search_rol, save_enter)
                    if find_id:
                        save_name = find_name.group()
                        save_password = find_password.group()
                        save_rol = find_rol.group()
                        save_rol = save_rol[:-1]
                        object_info = line_begin_info + "  " + save_name + "\n  " + save_password + "\n  " + save_rol + line_end_info
                        return jsonify({'data': object_info}), 200
                object_info = line_begin_info + empty_user_line + empty_password_line + empty_rol_line + line_end_info 
                return jsonify({'data': object_info}), 200
    else:
        return jsonify({'message': 'Error, no se encontró el archivo de registro'}), 400

@app.route('/get-tittle-and-description', methods=["POST"]) # Función para recibir el título y descripción de una pregunta
def get_tittle_and_description(): 
    data = request.get_json()
    block_id = data.get('text', '')
    question_id = data.get('question_id', '')
    search_block = r"\"block_" + str(block_id) + r"\"(.|\n)*?}(\n|\s)*?}"
    search_question = r"\"question_" + str(question_id) + r"\"(.|\n)*?}"
    search_tittle = r"\"tittle\":.*"
    search_description = r"\"description\":.*"
    begin_object = "{\n"
    end_object = "}"
    if os.path.exists(route_to_data_json_block_and_question):
        with open(route_to_data_json_block_and_question, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_block = re.search(search_block, content)
                if find_block:
                    find_question = re.search(search_question, find_block.group())
                    if find_question:
                        find_tittle = re.search(search_tittle, find_question.group())
                        find_tittle = find_tittle.group()
                        find_tittle = find_tittle.split(": ")[1]
                        find_tittle = find_tittle[:-1]
                        find_description = re.search(search_description, find_question.group())
                        find_description = find_description.group()
                        find_description = find_description.split(": ")[1]
                        save_tittle = find_tittle.split('"')[1]
                        save_description = find_description.split('"')[1]
                        tittle_line = "  \"tittle\": \"" + save_tittle + "\",\n"
                        description_line = "  \"description\": \"" + save_description + "\"\n"
                        info_question = begin_object + tittle_line + description_line + end_object
                        return jsonify({'data': info_question}), 200
                        # meter condición para titulo y pregunta vacía?
                    else:
                        return jsonify({'message': "No se encontraron registros"}), 500
                else:
                    return jsonify({'message': 'Error, no se localizó el bloque'}), 400
    else:
        return jsonify({'message': 'Error, no se encontró el fichero del que tomar la información'}), 400

@app.route('/get-questions-of-internal-block', methods=["POST"]) # Función para recibir todas las preguntas asociadas a un bloque
def get_questions_of_internal_block():
    data = request.get_json()
    block_id = data.get('text', '')
    search_begin_block = r"\"block_" + str(block_id) + r"\".*?{"
    search_block = r"\"block_" + str(block_id) + r"\"(.|\n)*?}(\s|\n)*?}"
    search_empty_block = r"\"block_" + str(block_id) + r"\".*?{(\s|\n)*?}"
    if os.path.exists(route_to_json_buttons_questions):
        with open(route_to_json_buttons_questions, "r") as file:
            lines = file.readlines()
            content = ''.join(lines)
            if lines:
                find_empty_block = re.search(search_empty_block, content)
                if find_empty_block:
                    return jsonify({'message': "No se encontró información del bloque"}), 500
                else:
                    find_block = re.search(search_block, content)
                    if find_block:
                        save_block_content = find_block.group()
                        find_begin_block = re.search(search_begin_block, save_block_content)
                        object_info = save_block_content[find_begin_block.end():]
                        object_info = procesate_object_info(object_info)
                        return jsonify({'data': object_info}), 200
                    else:
                        return jsonify({'message': "No se encontró información del bloque"}), 500
    else:
        return jsonify({'message': "Error, no se encontró el archivo de registro"}), 400

def procesate_object_info(object_info): # Función para procesar la información obtenida de la pregunta
    procesate_object = "[\n"
    counter = 1
    search_begin_question = r"\"question_" + str(counter) + r"\".*?{"
    search_total_question = r"\"question_" + str(counter) + r"\"(.|\n)*?}"
    while(re.search(search_begin_question, object_info)):
        search_begin_question = r"\"question_" + str(counter) + r"\".*?{"
        search_total_question = r"\"question_" + str(counter) + r"\"(.|\n)*?}"
        find_begin_question = re.search(search_begin_question, object_info)
        if find_begin_question:
            find_question = re.search(search_total_question, object_info)
            if find_question:
                procesate_object += "    {\n"
                procesate_object += object_info[find_begin_question.end() + 1:find_question.end()]
                procesate_object += ",\n"
        counter += 1
    procesate_object = procesate_object[:-2]
    procesate_object += "\n]"
    return procesate_object

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)