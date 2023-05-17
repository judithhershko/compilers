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
int z = 2;
scanf(" val is: %d and %d",z*z, z);
return 0;
}
