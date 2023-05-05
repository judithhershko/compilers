;//voidf(int*x){return;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define void @f(ptr noundef %0) #0 { 
%2 = alloca ptr, align 4

store ptr %0, ptr %2, align 4

;//int*x

ret void}
;//intmain(intx,inty){x=x+1*x+89;while(x+90>90){x=x+1;}return1;}

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

;//x=x+1*x+89

%6 = load i32, ptr %5, align 4
%7 = load i32, ptr %5, align 4
%8 = add nsw i32 %7, 89

%9 = add nsw i32 %7, %8

%10 = mul nsw i32 1, %9

 store i32 %10, ptr %5, align 4
;//while(x+90>90){x=x+1;}

%11 = add nsw i32 %10, 90

%12 = icmp sgt i32 %11, 90

%13 = add nsw i32 %12, 90

br label %14
14:
 %15 = load i32, ptr %5, align 4
%16 = add nsw i32 %15, 90

%17 = icmp sgt i32 %16, 90

 %18 = load i32, ptr %5, align 4
%19 = add nsw i32 %18, 90

%20 = icmp ne i32 %19, 0
br i1 %20, label %21, label %27
21:
 %22 = load i32, ptr %5, align 4
;//x=x+1

 %23 = load i32, ptr %5, align 4
%24 = load i32, ptr %5, align 4
%25 = load i32, ptr %5, align 4
%26 = add nsw i32 %25, 1

 store i32 %26, ptr %5, align 4
br label %14
27:
ret i32 1
}
