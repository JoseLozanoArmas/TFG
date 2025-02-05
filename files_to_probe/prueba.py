import os
import re
import subprocess


# Función que ejecuta el código en la ruta que se le pasa
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
            print("La extensión del archivo no está permitida") # MANDAR MENSJAE DE ERROR
    else: # En caso de que el fichero no exista mandamos aviso
        print(f"El archivo en la ruta '{route}' no existe.") # MODIFICAR ESTO PARA QUE MANDE UN ERROR Y NO UN PRINT
                
file_path_js = "test_factorial.test.js"
file_path_python = "test_factorial.py"
file_path_c_plus = "factorial.cc"
file_path_c = "factorial.c"
file_path_ruby = "factorial.rb"
file_path_ejecutable = "a.out"

check_if_the_code_pass_the_test(file_path_python)
