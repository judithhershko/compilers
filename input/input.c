#include "stdio.h"

int f(int x, int y)
{
x=5+1;
char z='a';
int q[2]={1,2};
return 1;

}
int main(int x,int y)
{
x=90;
y = f(x, y);
printf("%d %d", x,x);
x=f(0, x);
return x;
}