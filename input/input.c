#include "stdio.h";

int f(int a){
    a = a * a;
    return a;
}

int main()
{
int x[2];
x[0] = 3;
int y = 2;
while (y < 5){
    f(y);
    y = y + 1;
}
return 0;
}