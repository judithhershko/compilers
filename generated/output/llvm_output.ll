;//#include <stdio.h>

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4
;//this is function f


; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4

;//int a[3]={0,1,2};


store i32 0, i32* %1, align 4
store i32 0, i32* %2, align 4
%3 = call i32 @f(i32 noundef %2)
%4 = load i32, ptr %3, align 4
%5 = add nsw i32 0, %4

store i32 90, i32* %1, align 4
 %6 = load ptr, ptr %1, align 4
ret i32 %6}
