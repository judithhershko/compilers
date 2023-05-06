#include "stdio.h"
int main( int y)
{
/**
const int r = 5;

int x=0;
x=x+1*x+89;
if(x>90)
{
x=x-10;
while(x<8)
{
x=x+1;
}
}
**/

//INCOMPATIBLE TYPES OPERATIONS
/**
int x = 478;
char b = 'a';
int y = x + b;
**/

//INCOMPATIBLE POINTERS OP
/**
int x = 478;
int b = -251454;
int* b_ptr = &b;
int** x_ptr = &b_ptr;
x_ptr = &b;
**/

//INCOMPATIBLE TYPES VARIABLES
//int x = 'a';

//PRINT FAIL REMOVE INCLULDE
//printf("is value");

//REASSIGMENT ERROR
/**
const int x = 478;
x=5;
**/

//REDECLARATION
/**
int x = 5;
int x;
**/

//RVALUE
//nt 0 = 5;

//UNDECLARED
/**
int some_variable;
some_variable = x + 3;
**/

return 1;
}
