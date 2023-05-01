declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [2x i8] c"\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%1 = alloca i32, align 4


%2 = call i32 (ptr, ...) @printf(ptr noundef @.str)
br label %3
3 :
%4 = load i32, ptr %1, align 4
%5 = icmp slt i32 %4, 10

br i1 %5, label %6, label %9
6 :
%7 = load i32, ptr %5, align 4
%8 = add nsw i32 %7, 1

br label %9
9 :
 %11 = load ptr, ptr %10, align 4
ret i32 %11}
