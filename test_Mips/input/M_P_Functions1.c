#include "stdio.h";

int f(int a) {
	if (a<2) {
		return f(a);
	}
	else {
		return f(a-1) + f(a-2);
	}
}

int main()
{
    int i = 5;
    int a = 0;
    while(a < i){
		f(a);
	}
return 0;
}