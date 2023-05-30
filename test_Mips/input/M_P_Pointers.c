#include "stdio.h";
int main()
{
int integer = 5;
int* ptr = &integer;
int ** ptr_ptr = &ptr;
int **another_pointer = ptr_ptr;

int z = integer + 5;
ptr = &z;
int* pointer = &z;
int x = *pointer;
int** x_ptr = &ptr;

float a = 856.25668;
float* a_ptr = &a;

char c = 'x';
char* char_ptr = &c;
return 0;
}