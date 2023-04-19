; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %1,ptr noundef %3) #0 { 
%2 = alloca i32, align 4
%4 = alloca ptr, align 4
store i32 %1, ptr %2, align 4
store ptr %3, ptr %4, align 4
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @function(i32 noundef %1) #0 { 
%2 = alloca i32, align 4
store i32 %1, ptr %2, align 4
 %3 = load ptr, ptr %2, align 4
ret void}
