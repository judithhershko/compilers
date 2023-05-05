declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [13x i8] c""%d and %s"\0A\00", align 1
@.str.1 = private unnamed_addr constant [3x i8] c"y\0A\00", align 1
;//intf(intx){return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

ret i32 1
}
;//intmain(intx,inty){printf("%d and %s",x,y);f(0,x);returnx;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

;//intx

;//inty

;//printf("%d and %s",x,y)

; printf ("%d and %s")
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str , Nonenoundef 4,  ptr noundef @.str{}.1)
 %6 = load i32, ptr %3, align 4
ret i32 %6}
