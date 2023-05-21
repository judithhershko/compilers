#include "stdio.h";
int fff(){
    return 1;
}

int f(int x)
{
x=!x;
//this is a comment
{
int x= x+x*fff();
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
char y = 'a';
int x=90;
int z=33;
while (z<x)
{
int za;
z=z+1;
printf(" val is: %d",z);
}
return 0;
}
