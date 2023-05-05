declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [6 x i8] c"%d %d\00", align 1
;//intmain(intx,inty){printf("%d %d",x,y);return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

;//intx

;//inty

;//printf("%d %d",x,y)

; printf ("%d %d")
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str ,  i32 noundef 4,  i32 noundef 4)
ret i32 1
}
