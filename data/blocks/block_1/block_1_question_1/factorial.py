import sys

def factorial(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:  # Verifica si se proporcionó un argumento
        try:
            num = int(sys.argv[1])  # Convierte el argumento a entero
            print(factorial(num))
        except ValueError:
            print("Error: Ingresa un número entero válido.")
    else:
        print("Error: Debes ingresar un número como argumento.")
