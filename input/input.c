#include "stdio.h"
int f(int b, char a) {
	b = b +1;
	return b+1;
}


int main()
{
int x=5+1;
char z='a';

int y = f(x, z);
return 1;
}
