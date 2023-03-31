@.str = private unnamed_addr constant [32x i8] c"(909, <LiteralType.INT: 5>, 0)\0A\00", align 1
@.str.1 = private unnamed_addr constant [33x i8] c"('99', <LiteralType.INT: 5>, 0)\0A\00", align 1
@.str.2 = private unnamed_addr constant [37x i8] c"('994511', <LiteralType.INT: 5>, 0)\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int f = 909
%2 = alloca i32, align 4
; printf ((909, <LiteralType.INT: 5>, 0))
%3 = call i32 (ptr, ...) @printf(ptr noundef @.str)
;  int f = 99
%4 = alloca i32, align 4
; printf (('99', <LiteralType.INT: 5>, 0))
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
; const int i = 994511
%6 = alloca i32, align 4
; printf (('994511', <LiteralType.INT: 5>, 0))
%7 = call i32 (ptr, ...) @printf(ptr noundef @.str.2)

store i32 0, ptr %1, align 4
store i32 909, i32* %2, align 4
store i32 99, i32* %4, align 4
store i32 994511, i32* %6, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

