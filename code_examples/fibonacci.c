#include <stdio.h>

int main() {
    int n, i;
    int a = 0, b = 1, c;

    printf("Digite o numero de termos: ");
    scanf("%d", &n);

    if (n <= 0) {
        printf("Valor invalido\n");
        return 0;
    }

    printf("Sequencia Fibonacci:\n");
    for (i = 1; i <= n; i++) {
        printf("%d ", a);
        c = a + b;
        a = b;
        b = c;
    }

    printf("\n");
    return 0;
}
