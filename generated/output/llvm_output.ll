; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f() #0 { 
;  int z = 0
%1 = alloca i32, align 4


store i32 0, i32* %1, align 4
store i32 78, i32* %1, align 4
 %3 = load ptr, ptr %2, align 4
ret i32 %3}
