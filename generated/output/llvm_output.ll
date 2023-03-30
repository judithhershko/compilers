; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int x = 29
%2 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 29, i32* %2, align 4

ret i32 0
}


