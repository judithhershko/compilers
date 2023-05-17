#include "stdio.h";

int f(int x)
{
x=!x;
//this is a comment
{
int x=90;
x=x+1;
{
x=x+2;
}
x=3;
}
//int y=(x*x+78+x*x-12);
//printf("y is : %d ", x);
return x;
}
int main()
{
int x=f(2);
int z=1;
while (z<x)
{
z=z+1;
printf(" val is: %d",z);
}
return 0;
}
