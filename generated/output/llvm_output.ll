; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,ptr noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca ptr, align 4
;  int z = 0
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store ptr %1, ptr %4, align 4

 %7 = load ptr, ptr %6, align 4
ret i32 %7}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int z = 0
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

%4 = load i32, ptr %2, align 4
%5 = load i32, ptr %3, align 4
% 6 = sub nsw i32 %4, %5
%7 = load i32, ptr %6, align 4
% 9 = mult nsw i32 %8, %7
%10 = load i32, ptr %7, align 4
% 11 = add nsw i32 %10, %9
 %12 = load ptr, ptr %11, align 4
ret void}
