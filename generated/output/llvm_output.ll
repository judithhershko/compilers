; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 


br label %0
0 :
  %2 = load ptr, ptr %1, align 4
ret i32 %2}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,ptr noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca ptr, align 4
;  int k;
%5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store ptr %1, ptr %4, align 4

 %7 = load ptr, ptr %6, align 4
ret i32 %7}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int a;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

 %4 = load ptr, ptr %2, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 


 %1 = load ptr, ptr %0, align 4
ret void}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

 %6 = load ptr, ptr %5, align 4
ret void}
