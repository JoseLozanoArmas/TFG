import os
import re
import subprocess

# Función que ejecuta el código en la ruta que se le pasa
def ejecute_code(route):
    if os.path.exists(route): # Comprobamos que el fichero existe
        files_pattern = r".*\.(py|cc?|rb|js)" # Con esta expresión regular gestionamos los ficheros
        if re.match(files_pattern, route): # En caso de que coincida se procede a evaluar las distintas opciones con las que se haya hecho match
            extension = re.findall(files_pattern, route)[0]  
            if extension == "py": 
                with open(route, "r") as file: # Leemos y ejecutamos el fichero directamente
                    code = file.read()
                    exec(code)
            elif extension == "rb":
                result = subprocess.run(["ruby", route], capture_output=True, text=True)
                print(result.stdout)
            elif extension == "js":
                result = subprocess.run(["node", route], capture_output=True, text=True)
                print(result.stdout)
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
            print("La extensión del archivo no está permitida")
    else: # En caso de que el fichero no exista mandamos aviso
        print(f"El archivo en la ruta '{route}' no existe.") # MODIFICAR ESTO PARA QUE MANDE UN ERROR Y NO UN PRINT
                
file_path_js = "factorial.js"
file_path_python = "factorial.py"
file_path_c_plus = "factorial.cc"
file_path_c = "factorial.c"
file_path_ruby = "factorial.rb"
file_path_ejecutable = "a.out"
ejecute_code(file_path_js)
