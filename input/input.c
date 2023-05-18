#include <stdio.h>

// Should print the numbers: 42 42 43 43 44 44 45 45

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