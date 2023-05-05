#include "stdio.h"

int f(int x)
{
x=5+1;
char z='a';
return 1;
}
int main(int x,int y)
{
y = f(x);
//printf("%d and %s", x,y);
x=f(0);
return x;
}