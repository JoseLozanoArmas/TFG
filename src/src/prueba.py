import os

# Ruta del archivo
file_path = "../files_to_probe/probando_posibles_fallos.py"

# Comprobamos que el archivo existe
if os.path.exists(file_path):
    # Si existe lo leemos
    with open(file_path, "r") as file:
        # Guardamos y ejecutamos lo leido
        code = file.read()
        exec(code)
else:
    print(f"El archivo en la ruta '{file_path}' no existe.")
