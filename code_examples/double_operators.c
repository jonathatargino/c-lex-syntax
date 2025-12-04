#include <stdio.h>

int main() {
    int x = 5;
    int y = 3;
    int z = 0;

    z = x + y;
    printf("Soma: %d\n", z);

    z -= 2;
    printf("Subtracao composta: %d\n", z);

    x *= 2;
    printf("Multiplicacao composta: %d\n", x);

    y /= 2;
    printf("Divisao composta: %d\n", y);

    x++;
    y--;
    printf("Incremento: %d  Decremento: %d\n", x, y);

    return 0;
}
