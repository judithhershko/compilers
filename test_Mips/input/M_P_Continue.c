#include "stdio.h";
int main()
{
int i = 0;
	while(i < 10){
		printf("%d\n",i);
		if (i == 5){
			break;
		} else {
			i = i + 1;
			continue;
		}
		i = 10;
	}
return 0;
}