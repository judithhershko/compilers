#include <stdio.h>;

int f(int a);

int f(int a){
    a = a*a;
    return a;
}

void f2(char b){
    printf("%c", b);
}

int main()
{
    int x = 5;
    int y = f(x);
    char b = 'a';
    f2(b);
return 0;
}