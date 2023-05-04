;//intf(intx){x=x+3;return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//x=x+3

%3 = load i32, ptr %2, align 4
%4 = add nsw i32 %3, 3

 store i32 %3, ptr %4, align 4
ret ptr %3}
