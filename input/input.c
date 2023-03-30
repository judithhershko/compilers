int v=90+89*(78+90)+90;
int w = 20;
int * x = &v;
int ** y = &x;
//int z = * x;
//x = &w; infinite loop because right hand side contains the same declaration again
//*x = 20;