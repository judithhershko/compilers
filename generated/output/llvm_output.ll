;//intf(intx){x=x+1*x+89;return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//x=x+1*x+89

%3 = load i32, ptr %2, align 4
%4 = load i32, ptr %2, align 4
%5 = mul nsw i32 1, %4

%6 = add nsw i32 %5, 1

%7 = add nsw i32 %6, 89

 store i32 %7, ptr %2, align 4
ret i32 1
}
;//intmain(intk){return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intk

ret i32 1
}
