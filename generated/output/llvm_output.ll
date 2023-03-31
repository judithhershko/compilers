@.str = private unnamed_addr constant [34x i8] c"(909, <LiteralType.FLOAT: 8>, 0)\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  float f = 909
%2 = alloca float, align 4
; printf (()
%3 = call i32 (ptr, ...) @printf(ptr noundef @.str)
;  int u = 90
%4 = alloca i32, align 4
;  int * pu = & u
%5 = alloca ptr, align 8
;  int * pu = & u
%6 = alloca ptr, align 8

store i32 0, ptr %1, align 4
store float 0X408C68000000000, float* %2, align 4
store i32 90, i32* %4, align 4
store ptr %4, ptr %5, align 8
store ptr %4, ptr %6, align 8

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

