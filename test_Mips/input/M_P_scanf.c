#include "stdio.h";
int main()
{
    int x;
	int y;
    printf("Enter two numbers:");
	scanf("%d%d", &x, &y);
	printf("%d; %d", x, y);

    char a[5];
    printf("Enter a 5-character string:");
	scanf("%5s", &a);
	printf("%s", a);


return 0;
}