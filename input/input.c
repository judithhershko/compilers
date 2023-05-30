#include "stdio.h";

int f(int a) {
	if (a>1) {
		a = 1;
	}
	return a;
}

int main()
{
    int i = 5;
    int* a = &i;
    while(*a > 0){
        int x = *a;
        f(*a);
    }

return 0;
}