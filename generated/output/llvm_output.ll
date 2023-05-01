; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%1 = alloca i32, align 4


br label %2
2 :
%3 = load i32, ptr %1, align 4
%4 = icmp slt i32 %3, 10

br i1 %4, label %5, label %8
5 :
%6 = load i32, ptr %4, align 4
%7 = add nsw i32 %6, 1

br label %8
8 :
 %10 = load ptr, ptr %9, align 4
ret i32 %10}
