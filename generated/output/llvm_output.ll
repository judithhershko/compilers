@.str.1 = private unnamed_addr constant [6 x i8] c"%d %d\00", align 1
declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [6 x i8] c"%d %d\00", align 1
;//intf(intx,inty){printf("%d %d",x,y);return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4

;//intx

;//inty

;//printf("%d %d",x,y)

; printf ("%d %d")
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str ,  i32 noundef 3,  i32 noundef 4)
ret i32 1
}
;//intmain(intx,inty){y=f(x,y);printf("%d %d",x,y);x=f(0,x);returnx;x=5;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4
 %6 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4
store i32 %1, ptr %6, align 4

;//intx

;//inty

;//y=f(x,y)

%7 = alloca i32, align 4
%8 = call i32 @f ( i32 noundef 0,i32 noundef 1)
store i32 %8, ptr %7, align 4
;//printf("%d %d",x,y)

; printf ("%d %d")
%9 = call i32 (ptr, ...) @printf(ptr noundef @.str.1 ,  i32 noundef 6,  i32 noundef 8)
;//x=f(0,x)

%10 = alloca i32, align 4
%11 = call i32 @f ( i32 noundef 0,i32 noundef 1)
store i32 %11, ptr %10, align 4
 %12 = load i32, ptr %10, align 4
ret i32 %12}
