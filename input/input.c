#include "stdio.h";
float fff(int x, float fx){
float *px=&fx;
float z=*px;
float f=90.9*z+z;
return fx;
}
int main(int x, float z)
{
float f=fff(1,2.2);
x=90;

printf("y is : %i en int is : %i ", x,x*x+89);
return 0;
}
