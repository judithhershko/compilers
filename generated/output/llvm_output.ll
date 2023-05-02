;//#include <stdio.h>

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 

;//this is function f


ret i32 1
}
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4


store i32 0, i32* %1, align 4
%3 = load i32, ptr %2, align 4
%4 = add nsw i32 90, %4

 %5 = load ptr, ptr %1, align 4
ret i32 %5}
