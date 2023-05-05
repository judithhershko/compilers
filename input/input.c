#include "stdio.h"

int f(int x, int y)
{
x=5+1;
char z='a';
return 1;
}
int main(int x,int y)
{
y = f(x, y);
//printf("%d %s", x,x);
x=f(0, x);
return x;
}