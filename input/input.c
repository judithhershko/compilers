int x = 5*5+4);
int w = 20;
int * x = &v;
int ** y = &x;
//int z = * x;
//x = &w; infinite loop because right hand side contains the same declaration again
//*x = 20;