;//intf(intx){return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

ret i32 1
}
;//intmain(intx,inty){//printf("%d and %s", x,y);x=f(x);returnx;}

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

;//printf("%d and %s", x,y);

;//x=f(x)

%8 = call i32 @f ( i32 noundef 0 )
store i32 %8, ptr %6, align 4
ret i32 x
}
