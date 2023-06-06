#include "stdio.h";
int main()
{
    int z = 1;
    int x[3];
    x[z-1] = 5;
    x[z] = 6;
    x[1+z] = 7;
    int y = x[z-1];
    int w = x[z];
    int v = x[1+z];
    int u[2] = {1, 2};
    return 0;
}