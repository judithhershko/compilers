; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  float x = -5.78
%2 = alloca float, align 4
;  int y = 20
%3 = alloca i32, align 4
; const float * x_ptr = & x
%4 = alloca ptr, align 8

store i32 0, ptr %1, align 4
store float -5.78, float* %2, align 4
store i32 20, i32* %3, align 4
store ptr %2, ptr %4, align 8
;//x_ptr = &y;

;//*x_ptr = 62;


ret i32 0
}


