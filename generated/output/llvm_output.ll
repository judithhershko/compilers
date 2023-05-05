declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [6 x i8] c"%d %d\00", align 1
@__const.f.q = private unnamed_addr constant [2 x i32] [i32 1,i32 2] , align 4 
;//intf(intx,inty){x=5+1;charz='a';intq[2]={1,2};return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4
;  char z;
%6 = alloca i8, align 1
%7 = alloca [ 2 x i32], align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intx

;//inty

;//x=5+1

store i32 6, i32* %5, align 4
;//charz='a'

store i8 97, i8* %6, align 1
;//intq[2]={1,2}

ret i32 1
}
;//intmain(intx,inty){x=90;y=f(x,y);printf("%d %d",x,x);x=f(0,x);returnx;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intx

;//inty

;//x=90

store i32 90, i32* %3, align 4
;//y=f(x,y)

%6 = alloca i32, align 4
%7 = call i32 @f ( i32 noundef 0,i32 noundef 1)
store i32 %7, ptr %6, align 4
;//printf("%d %d",x,x)

; printf ("%d %d")
%8 = call i32 (ptr, ...) @printf(ptr noundef @.str ,  i32 noundef 90,  i32 noundef 90)
;//x=f(0,x)

%9 = alloca i32, align 4
%10 = call i32 @f ( i32 noundef 0,i32 noundef 1)
store i32 %10, ptr %9, align 4
 %11 = load i32, ptr %9, align 4
ret i32 %11}
