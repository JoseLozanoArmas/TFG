#include <stdio.h>
#include <stdbool.h>

bool is_pair(int number) {
  if (number % 2 == 0) {
    return true;
  } else {
    return false;
  }
}

int main() {
  printf("%d\n", is_pair(5)); // Imprime 0 (falso)
  return 0;
}
