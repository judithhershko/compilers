#include "stdio.h";

float fff(int x, float fx){
float *px=&fx;
float **ppx=&px;
float z=*px;
float f=90.9*z+z;
return 100.1;
}

int main(int x, float fx, int xi)
{
int y[3];
//scanf("%d%d", &x, &y);
scanf("%d%d", x, y);

float f=fff(1,2.2);
float *px=&f;
*px=fx;
float z=*px;
float ff=90.9*(z)+z;
while(f<ff)
{
x=x+1;
}
printf("y is : %d en int is : %i ",*px,x*x+89);
//printf("y is : %d en int is : %i ",f,x*x+89);

return 0;
}