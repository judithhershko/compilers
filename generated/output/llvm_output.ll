;//intmain(intx,inty){x=x+1*x+89;while(x>90+y){x=x+1;}return1;}

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
%8 = mul nsw i32 1, %7

%9 = add nsw i32 %8, 1

%10 = add nsw i32 %9, 89

 store i32 %10, ptr %5, align 4
;//while(x>90+y){x=x+1;}

br label %11
11:
 %12 = load i32, ptr %4, align 4
%13 = add nsw i32 90, %12

br i1 %13, label %14, label %20
14:
 %15 = load i32, ptr %5, align 4
;//x=x+1

 %16 = load i32, ptr %5, align 4
%17 = load i32, ptr %5, align 4
%18 = load i32, ptr %5, align 4
%19 = add nsw i32 %18, 1

 store i32 %19, ptr %5, align 4
br label %11
20:
ret i32 1
}
