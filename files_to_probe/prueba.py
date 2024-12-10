import os
import re

# Función que ejecuta el código en la ruta que se le pasa
def ejecute_code(route):
    if os.path.exists(route): # Comprobamos que el archivo existe
        files_pattern = r".*\.(py|cc?|rb)"
        if re.match(files_pattern, route): # En caso de que de el archivo tenga una extensión permitida
            extension = re.findall(files_pattern, route)[0] # buscamos la extensión del archivo
            if extension == "py": # En el caso de ser un código python
                with open(route, "r") as file:
                    # Guardamos y ejecutamos lo leído
                    code = file.read()
                    exec(code)
            
        else:
            print("la extensión del archivo no está permitida")
    else:
        print(f"El archivo en la ruta '{route}' no existe.")
                

file_path_python = "print_hello_world.py"
file_path_c_plus = "print_hello_world.cc"
file_path_c = "print_hello_world.c"
file_path_ruby = "print_hello_world.rb"
file_path_ejecutable = "a.out"
ejecute_code(file_path_python)
