; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 29
%2 = alloca i32, align 4
;  int * x = & v
%3 = alloca ptr, align 8
;  int z = 15132
%4 = alloca i32, align 4
;  int w = 20
%5 = alloca i32, align 4
;  int * x = & w
%6 = alloca ptr, align 8
;  int aa = 90
%8 = alloca i32, align 4
;  float q = 90.89
%9 = alloca float, align 4

store i32 0, ptr %1, align 4
store i32 15132, i32* %2, align 4
store ptr %2, ptr %3, align 8
store i32 15132, i32* %4, align 4
store i32 20, i32* %5, align 4
store ptr %5, ptr %6, align 8
%7 = load ptr, ptr %6, align 8
store i32 20, ptr %7, align 4
;//gogyg

store i32 90, i32* %8, align 4
;/**
;hui
;puihupi
;hi
;**/
store float 90.89, float* %9, align 4

ret i32 0
}


