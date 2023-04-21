; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%0 = alloca i32, align 4


 %2 = load ptr, ptr %1, align 4
ret i32 %2}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,ptr noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca ptr, align 4
;  int z;
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store ptr %1, ptr %4, align 4

 %7 = load ptr, ptr %6, align 4
ret i32 %7}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int z;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

%4 = load i32, ptr %3, align 4
%5 = mult nsw i32 %4, 90
%6 = load i32, ptr %5, align 4
%7 = load i32, ptr %2, align 4
%8 = mult nsw i32 %6, %7
%9 = load i32, ptr %7, align 4
%10 = load i32, ptr %8, align 4
%11 = sub nsw i32 %9, %10
%12 = load i32, ptr %11, align 4
%13 = add nsw i32 %12, 90
 %14 = load ptr, ptr %13, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 
;  int z;
%0 = alloca i32, align 4
;  int x;
%1 = alloca i32, align 4


%2 = load i32, ptr %0, align 4
%3 = add nsw i32 %2, 5
%4 = load i32, ptr %1, align 4
%5 = add nsw i32 5, %5
 %6 = load ptr, ptr %3, align 4
ret void}
