#include <iostream>

bool is_pair(int number) {
  if (number % 2 == 0) {
    return true;
  } else {
    return false;
  }
}

int main() {
  std::cout << is_pair(5) << std::endl; // Imprime 0 (falso)
}