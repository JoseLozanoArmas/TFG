#include <stdio.h>
#include <stdlib.h>

int factorial(int number) {
    int result = 1;
    for (int i = 1; i <= number; ++i) {
        result *= i;
    }
    return result;
}

void processFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error: No se pudo abrir el archivo.\n");
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        int number = atoi(line); // Convertir la línea a entero
        if (number < 0) {
            fprintf(stderr, "Error: el número debe ser positivo.\n");
        } else {
            printf("%d\n", factorial(number));
        }
    }

    fclose(file);
}

int main(int argc, char* argv[]) {
    if (argc != 2) { // Verifica que se pase un archivo como argumento
        fprintf(stderr, "Uso: %s <archivo>\n", argv[0]);
        return 1;
    }

    processFile(argv[1]);
    return 0;
}
