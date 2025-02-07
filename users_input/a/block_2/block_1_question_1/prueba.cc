#include <iostream>
#include <iomanip>  // Para setw

int main() {
    int result = 1;
    int base = 2;
    int potence = 5;
    for (int i = 0; i < potence; ++i) {
        result *= base;
    }
    std::cout << result << std::endl;

    return 0;
}