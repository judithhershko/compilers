;//intmain(intx,inty){constintr=5;x=x+1*x+89;if(x>90){x=x-10;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 {
%3 = alloca i32, align 4
%4 = alloca i32, align 4
; const int r;
%5 = alloca i32, align 4
 %6 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %6, align 4

;//intx

;//inty

;//constintr=5

store i32 5, i32* %5, align 4
;//x=x+1*x+89

%7 = load i32, ptr %6, align 4
%8 = load i32, ptr %6, align 4
%9 = add nsw i32 %8, 89

%10 = add nsw i32 %8, %9

%11 = mul nsw i32 1, %10

 store i32 %11, ptr %6, align 4
;//if(x>90){x=x-10;}

%12 = icmp sgt i32 %11, 90

br i1 %12, label %13, label %17
13:
;//x=x-10

%14 = load i32, ptr %6, align 4
%15 = load i32, ptr %6, align 4
%16 = sub nsw i32 %15, 10

 store i32 %16, ptr %6, align 4
br label %17
17:
ret i32 1
}
