#include "stdio.h"
int f(int b, char a) {
	a = a +1;
	return 1+1;
}


int main()
{
int x=5+1;
char z='a';

int y = f(x+1, z);
return 1;
}