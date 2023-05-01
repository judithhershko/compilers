; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%1 = alloca i32, align 4


%2 = load i32, ptr %1, align 4
%3 = icmp sge i32 %2, 10

br i1 %3, label %4, label %7
4 :
%5 = load i32, ptr %3, align 4
%6 = add nsw i32 %5, 1

br label %10
7 :
%8 = load i32, ptr %6, align 4
%9 = add nsw i32 %8, 2

br label %10
10 :
 %12 = load ptr, ptr %11, align 4
ret i32 %12}
