; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,ptr noundef %1) #0 { 
%3 = alloca i32, align 4
store i32 %0, ptr %3, align 4
%4 = alloca ptr, align 4
store ptr %1, ptr %4, align 4
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
store i32 %0, ptr %2, align 4
%3 = load i32, ptr %2, align 4
% 4 = add nsw i32 %3, %5
 %6 = load ptr, ptr %4, align 4
ret void}
