declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [3x i8] c"z\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%1 = alloca i32, align 4
; printf (z)
%2 = call i32 (ptr, ...) @printf(ptr noundef @.str)

;//q=z > z + 1 + 3 || z < z - 1 ;


br label %3
3 :
 %4 = load i32, ptr %1, align 4
%5 = icmp slt i32 %4, 90
br i1 %5, label %6, label %$
6 :
%7 = load i32, ptr %5, align 4
%8 = add nsw i32 %7, 1
9 :
 %11 = load ptr, ptr %10, align 4
ret i32 %11}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
;  int z;
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

 %7 = load ptr, ptr %6, align 4
ret i32 %7}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int z;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

%4 = load i32, ptr %2, align 4
%5 = load i32, ptr %3, align 4
%6 = sub nsw i32 %4, %5
%7 = load i32, ptr %6, align 4
%8 = mult nsw i32 8, %8
 %9 = load ptr, ptr %8, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4


%3 = load i32, ptr %1, align 4
%4 = add nsw i32 %3, 5
%5 = load i32, ptr %2, align 4
%6 = add nsw i32 6, %6
 %7 = load ptr, ptr %4, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
;  int z;
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

%6 = load i32, ptr %3, align 4
%7 = load i32, ptr %4, align 4
%8 = add nsw i32 %6, %7
 %9 = load ptr, ptr %5, align 4
ret void}
