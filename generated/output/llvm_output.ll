;//intf(intx){x=5+1;charz='a';return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
 %3 = alloca i32, align 4
;  char z;
%4 = alloca i8, align 1

store i32 %0, ptr %2, align 4
store i32 %0, ptr %3, align 4

;//intx

;//x=5+1

store i32 6, i32* %3, align 4
;//charz='a'

store i8 97, i8* %4, align 1
ret i32 1
}
;//intmain(intx,inty){y=f(x);//printf("%d and %s", x,y);x=f(0);returnx;}

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

;//y=f(x)

%8 = call i32 @f ( i32 noundef 0 )
store i32 %8, ptr %6, align 4
;//printf("%d and %s", x,y);

;//x=f(0)

%11 = call i32 @f ( i32 noundef 0 )
store i32 %11, ptr %9, align 4
ret i32 x
}
