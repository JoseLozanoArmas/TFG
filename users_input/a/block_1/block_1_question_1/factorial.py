import sys

def factorial(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

def process_file(filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    num = int(line.strip())  # Convertir cada línea a entero
                    print(factorial(num))
                except ValueError:
                    print(f"Error: '{line.strip()}' no es un número entero válido.")
    except FileNotFoundError:
        print("Error: El archivo no existe.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])  # Leer números desde el archivo
    else:
        print("Error: Debes proporcionar un archivo como argumento.")
