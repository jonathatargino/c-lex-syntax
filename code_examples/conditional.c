#include <stdio.h>

int main() {
    int opcao;

    printf("Digite um numero (1 a 3): ");
    scanf("%d", &opcao);

    switch (opcao) {
        case 1:
            printf("Opcao 1 escolhida\n");
            break;
        case 2:
            printf("Opcao 2 escolhida\n");
            break;
        case 3:
            printf("Opcao 3 escolhida\n");
            break;
        default:
            printf("Opcao invalida\n");
            break;
    }

    return 0;
}
