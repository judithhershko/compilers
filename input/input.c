#include "stdio.h";

int main(){
int z = 2;
{
    int x = 5;
	if (x < 5){
		printf("x < 5 namely: %d", x); // Should not print
	}
	else if (x == 5){
	    printf("x == 5");
	}
	else {
	    printf("x > 5 namely: %d", x);
	}
	scanf(" val is: %d and %d",z*z, z);
}
return 0;
}
