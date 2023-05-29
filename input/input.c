#include "stdio.h";
float fff(int x, float fx){
float *px=&fx;
float **ppx=&px;
float z=*px;
float f=90.9*z+z;
return fx;
}
int main(int x)
{
float f=fff(1,2.2);
float *px=&f;
*px=x;
float z=*px;
float ff=90.9*(z)+z;
while(z<x)
{
z=z+1;
}
printf("y is : %d en int is : %i ", f,x*x+89);
return 0;
}
