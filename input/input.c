#include "stdio.h";

int f(int a){
    a = a * a;
    return a;
}

int main()
{
int x = 5;
int* y = &x;
f(*y);
return 0;
}