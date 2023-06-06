#include <stdio.h>

int print(int n) {

    printf("%i",n);
    return 0;
}

int main() {
    int n=5;
    int counter=0;
    int i=1;
    int ip=1;
    int pp=1;
    int a=0;
    printf("%i",i);
    printf("%i",i);
    while(counter<n)
    {
        i=ip+pp;
        pp=ip;
        ip=i;
        printf("%i",i);
        counter=counter+1;
    }
    return 0;
}