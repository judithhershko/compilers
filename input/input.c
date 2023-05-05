#include "stdio.h"

int f(int x)
{
    return 1;
}
int main(int x,int y)
{
printf("%d and %s", x,y);
f('x');
return x;
}