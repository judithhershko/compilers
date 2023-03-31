; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 5
%2 = alloca i32, align 4
;  int y = 7
%3 = alloca i32, align 4
;  char z = 'a'
%4 = alloca i8, align 1
;  int u = 6
%5 = alloca i32, align 4
;  int * xx = & x
%6 = alloca ptr, align 8
;  int ** xxx = & xx
%7 = alloca ptr, align 8
%8 = load ptr, ptr %7, align 8
;  int * xx = & u
%9 = alloca ptr, align 8
%10 = load ptr, ptr %8, align 8
;  int x = 1
%11 = alloca i32, align 4
;  int y = 1
%12 = alloca i32, align 4
; const int v = 5
%13 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 5, i32* %2, align 4
store i32 7, i32* %3, align 4
store i8 97, i8* %4, align 1
store i32 6, i32* %5, align 4
store ptr %2, ptr %6, align 8
store ptr %6, ptr %7, align 8
store i32 20, ptr %8, align 4
store ptr %5, ptr %9, align 8
store i32 25, ptr %10, align 4
store i32 1, i32* %11, align 4
store i32 1, i32* %12, align 4
store i32 5, i32* %13, align 4

ret i32 0
}


