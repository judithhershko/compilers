#include "stdio.h";
int main()
{
int x = 5;
	if (x < 5){
		printf("Something went wrong"); // Should not print
	} else {
		printf("Hello world!\n"); // Should print
	}
return 0;
}