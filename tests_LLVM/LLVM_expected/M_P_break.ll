;//intmain(intx){x=x+1*x+89;while(x+90>90){x=x+1;break;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 {
%2 = alloca i32, align 4
 %3 = alloca i32, align 4

store i32 %0, ptr %2, align 4
store i32 %0, ptr %3, align 4

;//intx

;//x=x+1*x+89

%4 = load i32, ptr %3, align 4
%5 = load i32, ptr %3, align 4
%6 = add nsw i32 %5, 89

%7 = add nsw i32 %5, %6

%8 = mul nsw i32 1, %7

 store i32 %8, ptr %3, align 4
;//while(x+90>90){x=x+1;break;}

%9 = add nsw i32 %8, 90

%10 = icmp sgt i32 %9, 90

%11 = add nsw i32 %10, 90

br label %12
12:
 %13 = load i32, ptr %3, align 4
%14 = add nsw i32 %13, 90

%15 = icmp sgt i32 %14, 90

 %16 = load i32, ptr %3, align 4
%17 = add nsw i32 %16, 90

%18 = icmp ne i32 %17, 0
br i1 %18, label %19, label %25
19:
 %20 = load i32, ptr %3, align 4
;//x=x+1

 %21 = load i32, ptr %3, align 4
%22 = load i32, ptr %3, align 4
%23 = load i32, ptr %3, align 4
%24 = add nsw i32 %23, 1

 store i32 %24, ptr %3, align 4
br label %25
25 :
ret i32 1
}
