#include <stdio.h>

int main() {
    int i;
    int v[5];
    int soma = 0;

    printf("Digite 5 numeros:\n");
    for (i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }

    for (i = 0; i < 5; i++) {
        soma += v[i];
    }

    printf("Soma: %d\n", soma);

    if (soma % 2 == 0) {
        printf("Soma eh par\n");
    } else {
        printf("Soma eh impar\n");
    }

    return 0;
}
