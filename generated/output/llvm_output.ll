; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 90
%2 = alloca i32, align 4
;  int * z = & x
%3 = alloca ptr, align 8
;  int a = 30
%4 = alloca i32, align 4
;  int * z = & a
%5 = alloca ptr, align 8

store i32 0, ptr %1, align 4
store i32 90, i32* %2, align 4
store ptr %2, ptr %3, align 8
store i32 30, i32* %4, align 4
store ptr %4, ptr %5, align 8

ret i32 0
}


