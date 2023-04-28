declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [3x i8] c"z\0A\00", align 1
@.str.1 = private unnamed_addr constant [5x i8] c"'a'\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z;
%1 = alloca i32, align 4

;//q=z > z + 1 + 3 || z < z - 1 ;

; printf (z)
%2 = call i32 (ptr, ...) @printf(ptr noundef @.str)
br label %3
3 :
br i1 %3, label %4, label %7
4 :
; printf ('a')
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
%6 = load i32, ptr %1, align 4
%7 = add nsw i32 %6, 1
br label %3, !llvm.loop !5
8 :
br label %9
9 :
br i1 %9, label %10, label %12
10 :
%11 = load i32, ptr %7, align 4
%12 = add nsw i32 %11, 2
br label %9, !llvm.loop !5
13 :
 %15 = load ptr, ptr %14, align 4
ret i32 %15}
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
