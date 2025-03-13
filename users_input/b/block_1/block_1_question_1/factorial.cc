#include <iostream>
#include <fstream>
#include <cstdlib> // Para std::atoi

int factorial(int number) {
    int result = 1;
    for (int i = 1; i <= number; ++i) {
        result *= i;
    }
    return result;
}

void processFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        std::cerr << "Error: No se pudo abrir el archivo.\n";
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        try {
            int number = std::stoi(line);
            if (number < 0) {
                std::cerr << "Error: el número debe ser positivo.\n";
            } else {
                std::cout << factorial(number) << '\n';
            }
        } catch (...) {
            std::cerr << "Error: '" << line << "' no es un número válido.\n";
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) { // Verifica que se pase un archivo como argumento
        std::cerr << "Uso: " << argv[0] << " <archivo>\n";
        return 1;
    }

    processFile(argv[1]);
    return 0;
}
