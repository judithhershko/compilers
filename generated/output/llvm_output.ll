@.str = private unnamed_addr constant [31x i8] c"(90, <LiteralType.INT: 5>, 0)\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int f = 909
%2 = alloca i32, align 4
;  int f = 99
%3 = alloca i32, align 4
; const int i = 90
%4 = alloca i32, align 4
; printf ()
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str)

store i32 0, ptr %1, align 4
store i32 909, i32* %2, align 4
store i32 99, i32* %3, align 4
store i32 90, i32* %4, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

