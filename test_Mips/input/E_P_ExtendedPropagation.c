#include "stdio.h";

int main()
{
int x = 2;
int* p = &x;
int y[2];
y[0] = 3;
y[1] = 4;

int r = x * *p + y[0]*y[1];

return 0;
}