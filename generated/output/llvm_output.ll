declare float @llvm.fmuladd.f32(float, float, float) #1
declare i32 @printf(ptr noundef, ...) #2
@.str = private unnamed_addr constant [6x i8] c"None\0A\00", align 1
@.str.1 = private unnamed_addr constant [6x i8] c"None\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 


 %2 = load ptr, ptr %1, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(float noundef %0,ptr noundef %1) #0 { 
%3 = alloca float, align 4
%4 = alloca ptr, align 4
;  float z = 0
%5 = alloca float, align 4
;  int zz;
%6 = alloca i32, align 4
; printf (None)
%15 = call i32 (ptr, ...) @printf(ptr noundef @.str)
; printf (None)
%17 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)

store float %0, ptr %3, align 4
store ptr %1, ptr %4, align 4

%7 = load float, ptr %3, align 4
%8 = load float, ptr %5, align 4
%9 = fsub float %7, %8
%10 = load float, ptr %8, align 4
%12 = sitofp i32 %11 to float
 %13 = call float @llvm.fmuladd.f32(float 40, float 13, float %13)
%13 = call13, %13
br label %14
14 :
 br i1 %15, label %16, label %$
16 :
%18 = load float, ptr %13, align 4
%20 = sitofp i32 %19 to float
%21 = add nsw i32 %18, 1
22 :
 %23 = load ptr, ptr %20, align 4
ret i32 %23}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,ptr noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca ptr, align 4
;  int z;
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store ptr %1, ptr %4, align 4
;//second scope


 %7 = load ptr, ptr %6, align 4
ret i32 %7}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4

;//fourth scope


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
;//fifth scope


%6 = load i32, ptr %3, align 4
%7 = load i32, ptr %4, align 4
%8 = add nsw i32 %6, %7
 %9 = load ptr, ptr %5, align 4
ret void}
