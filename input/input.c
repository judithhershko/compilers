#include <stdio.h>

int f(bool q)
{
    int z=0;
    if (z>=10)
    {
        z=z+1;
    }

    else if (z<89)
    {
        z=z+2;
    }

    z=90+0-89*z;
    return 1;
}