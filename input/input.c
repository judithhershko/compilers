#include "stdio.h";
int main()
{
int i = 0;
	while(i < 10){
		printf("i is %i",i);
		if (i == 5){
			break;
		} else {

			continue;
		}
		i = 10;
	}
return 0;
}