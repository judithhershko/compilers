#include "stdio.h";

int main()
{
	int x = 0;
	int* xp = &x;
	*xp = 42;
	int a=x+*xp;

	float f=90.0;
	float *pf=&f;

	float ff= *pf+f**pf;

return 0;
}