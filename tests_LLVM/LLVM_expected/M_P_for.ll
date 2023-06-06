;//intmain(intx,inty){x=x+1*x+89;for(intk=0;k<5;k=k+1){x=x+1;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 {
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4
;  int k;
%6 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intx

;//inty

;//x=x+1*x+89

%7 = load i32, ptr %5, align 4
%8 = load i32, ptr %5, align 4
%9 = add nsw i32 %8, 89

%10 = add nsw i32 %8, %9

%11 = mul nsw i32 1, %10

 store i32 %11, ptr %5, align 4
;//for(intk=0;k<5;k=k+1){x=x+1;}

;//intk=0

;//k=k+1

store i32 0, i32* %6, align 4
br label %12
12:
 %13 = load i32, ptr %6, align 4
%14 = icmp slt i32 %13, 5

br i1 %14, label %15, label %21
15:
 %16 = load i32, ptr %5, align 4
;//x=x+1

 %17 = load i32, ptr %5, align 4
%18 = load i32, ptr %5, align 4
%19 = load i32, ptr %5, align 4
%20 = add nsw i32 %19, 1

 store i32 %20, ptr %5, align 4
store i32 1, i32* %14, align 4
br label %12
21:
ret i32 1
}
