import os
import re

def ejecute_code(route):
    si = r".*\.(py|cc?|rb)"
    # Comprobamos que el archivo existe
    print(route)
    if os.path.exists(route):
        # Si existe lo leemos
        with open(route, "r") as file:
            # Guardamos y ejecutamos lo leído
            code = file.read()
            exec(code)
    else:
        print(f"El archivo en la ruta '{route}' no existe.")

file_path_python = "../files_to_probe/print_hello_world.py"
file_path_c_plus = "../files_to_probe/print_hello_world.cc"
file_path_c = "../files_to_probe/print_hello_world.c"
file_path_ruby = "../files_to_probe/print_hello_world.rb"
file_path_ejecutable = "../files_to_probe/a.out"
ejecute_code(file_path_ejecutable)
