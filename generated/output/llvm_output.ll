; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 5
%2 = alloca i32, align 4
;  int u = 7
%3 = alloca i32, align 4
;  int * xx = & x
%4 = alloca ptr, align 8
;  int ** xxx = & xx
%5 = alloca ptr, align 8
; const int v = 5
%6 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 5, i32* %2, align 4
store i32 7, i32* %3, align 4
store ptr %2, ptr %4, align 8
store ptr %4, ptr %5, align 8
store i32 1, i32* %2, align 1
store ptr %3, ptr %4, align 8
store i32 5, i32* %6, align 4
;//**xxx = 20;

;//**xxx = 25;


ret i32 0
}


