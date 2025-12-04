#include <stdio.h>

int main() {
    int n, fat = 1;

    printf("Digite um numero: ");
    scanf("%d", &n);

    if (n < 0) {
        printf("Nao existe fatorial de numero negativo\n");
        return 0;
    }

    while (n > 0) {
        fat *= n;
        n--;
    }

    printf("Fatorial: %d\n", fat);
    return 0;
}
