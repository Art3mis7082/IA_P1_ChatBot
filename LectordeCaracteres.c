//Version: 8 de septiembre 2026
//Falta traducir a Python
//AFD con cadenas de 0's y 1's que solo aceptan que termine en 1's, es decir, que no puede terminar en 0's.

#include <stdio.h>

void edo1();
void edo2();

char cad[100];
int i = -1;

int main () {
    FILE *archivo;
    archivo = fopen("archivo.txt", "r");
    fscanf(archivo, "%s", cad);
    edo1();
}

void edo1() {
    i++;
    if (cad[i] == '0'){
        edo1();
    }
    else if (cad[i] == '1'){
        edo2();
    }
    else {
        printf("Cadena no valida");
    }
}