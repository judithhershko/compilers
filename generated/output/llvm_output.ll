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

br label %11
11:
 %12 = load i32, ptr %5, align 4
%13 = add nsw i32 %12, 90

%14 = icmp sgt i32 %13, 90

 %15 = load i32, ptr %5, align 4
%16 = add nsw i32 %15, 90

%17 = icmp ne i32 %16, 0
br i1 %17, label %18, label %24
18:
 %19 = load i32, ptr %5, align 4
;//x=x+1

 %20 = load i32, ptr %5, align 4
%21 = load i32, ptr %5, align 4
%22 = load i32, ptr %5, align 4
%23 = add nsw i32 %22, 1

 store i32 %23, ptr %5, align 4
br label %11
24:
ret i32 1
}
