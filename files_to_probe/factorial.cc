#include <iostream>

int factorial(int number) {
  int result = 1;
  for (int i = 1; i <= number; ++i) {
    result *= i;
  }
  return result;
}

int main() {
  std::cout << factorial(5) << std::endl;
}