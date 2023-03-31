@.str = private unnamed_addr constant [33x i8] c"('25', <LiteralType.INT: 5>, 0)\0A\00", align 1
@.str.1 = private unnamed_addr constant [32x i8] c"('1', <LiteralType.INT: 5>, 0)\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 5
%2 = alloca i32, align 4
;  float y = 7.0
%3 = alloca float, align 4
;  char z = 'a'
%4 = alloca i8, align 1
;  int u = 6
%5 = alloca i32, align 4
;  int * xx = & x
%6 = alloca ptr, align 8
;  int ** xxx = & xx
%7 = alloca ptr, align 8
; const int v = 5
%8 = alloca i32, align 4
; printf (('25', <LiteralType.INT: 5>, 0))
%9 = call i32 (ptr, ...) @printf(ptr noundef @.str)
; printf (('1', <LiteralType.INT: 5>, 0))
%10 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)

store i32 0, ptr %1, align 4
store i32 5, i32* %2, align 4
store float 0x401c000000000000, float* %3, align 4
store i8 97, i8* %4, align 1
store i32 6, i32* %5, align 4
store ptr %2, ptr %6, align 8
store ptr %6, ptr %7, align 8
store i32 5, i32* %8, align 4
%11 = load ptr, ptr %7, align 8
%12 = load ptr, ptr %11, align 8
store i32 20, ptr %12, align 4
store ptr %5, ptr %12, align 8
%13 = load ptr, ptr %11, align 8
%14 = load ptr, ptr %13, align 8
store i32 25, ptr %14, align 4
store i32 1, i32* %2, align 1
store float 0x3ff5555560000000, float* %3, align 1

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

