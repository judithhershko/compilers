#include "stdio.h";

void f(int a) {
	if (a>1) {
		a = 1;
	}
}

int main()
{
    int i = 5;
    f(i);
return 0;
}