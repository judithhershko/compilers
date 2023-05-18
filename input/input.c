#include <stdio.h>

void f(){
    return;
}

int main(){
	int x = 0;
	int* xp = &x;
	*xp = 42;
	int** p = &xp;

	int y = 1;
	int* yp = &y;
	*yp = 5;

	return 1;
}