#include "stdio.h"

int f(int x)
{
int x=5+1;
char z='a';

int y = f(1+1, z);
return 1;
}
int main(int x,int y)
{
//printf("%d and %s", x,y);
x=f(x);
return x;
}