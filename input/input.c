#include "stdio.h"
int f(int x,int y)
{
printf("%d %d", x,y);

return 1;
}
int main(int x,int y)
{
y = f(x, y);
printf("%d %d", x,y);
x=f(0, x);
return x;
x = 5;
}
