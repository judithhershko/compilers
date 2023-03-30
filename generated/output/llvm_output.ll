; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  float x = -5.78
%2 = alloca float, align 4
;  int zz = 810
%3 = alloca i32, align 4
;  int a = 0
%4 = alloca i32, align 4
;  int * y = & zz
%5 = alloca ptr, align 8
;  int * y = & a
%6 = alloca ptr, align 8
; const float * x_ptr = & x
%7 = alloca ptr, align 8

store i32 0, ptr %1, align 4
store float -5.78, float* %2, align 4
store i32 810, i32* %3, align 4
store i32 0, i32* %4, align 4
store ptr %3, ptr %5, align 8
store ptr %4, ptr %6, align 8
store ptr %2, ptr %7, align 8
;//x_ptr = &y;

;//*x_ptr = 62;


ret i32 0
}


