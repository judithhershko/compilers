#include "stdio.h";
int main()
{
char x = 'a';
char* chr_ptr = &x;
*chr_ptr = 'b';
char another_char = *chr_ptr;

int y = -60;
int* some_pointer = &y;
*some_pointer = 53;
int** another_pointer = &some_pointer;
int*** triple_pointer = &another_pointer;
int z = ***triple_pointer;

return 0;
}