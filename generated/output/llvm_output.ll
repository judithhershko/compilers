; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int v = 15132
%2 = alloca i32, align 4
;  int w = 20
%3 = alloca i32, align 4
;  int * x = & v
%4 = alloca ptr, align 8
;  int ** y = & x
%5 = alloca ptr, align 8

store i32 0, ptr %1, align 4
store i32 15132, i32* %2, align 4
store i32 20, i32* %3, align 4
store ptr %2, ptr %4, align 8
store ptr %4, ptr %5, align 8
;//int z = * x;

;//x = &w; infinite loop because right hand side contains the same declaration again

;//*x = 20;


ret i32 0
}


