;//intmain(intx,inty){{intx=90;x=x+89;}constintr=5;x=x+1*x+89;if(x>90){x=x-10;}else{x=x+10;}returnx;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
; const int r;
%5 = alloca i32, align 4
 %6 = alloca i32, align 4
;  int x;
%7 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %6, align 4

;//intx

;//inty

;//intx=90

store i32 90, i32* %7, align 4
;//x=x+89

store i32 179, i32* %7, align 4
;//constintr=5

store i32 5, i32* %5, align 4
;//x=x+1*x+89

%8 = load i32, ptr %7, align 4
%9 = load i32, ptr %7, align 4
%10 = add nsw i32 %9, 89

%11 = add nsw i32 %9, %10

%12 = mul nsw i32 1, %11

 store i32 %12, ptr %7, align 4
;//if(x>90){x=x-10;}

%13 = icmp sgt i32 %12, 90

br i1 %13, label %14, label %18
14:
;//x=x-10

%15 = load i32, ptr %7, align 4
%16 = load i32, ptr %7, align 4
%17 = sub nsw i32 %16, 10

 store i32 %17, ptr %7, align 4
br label %22
18:
;//else{x=x+10;}

;//x=x+10

%19 = load i32, ptr %7, align 4
%20 = load i32, ptr %7, align 4
%21 = add nsw i32 %20, 10

 store i32 %21, ptr %7, align 4
br label %22
22:
 %23 = load i32, ptr %7, align 4
ret i32 %23}
