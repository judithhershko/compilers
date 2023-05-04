;//intf(intx){x=x+1*x+90;//this is function freturn1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//x=x+1*x+90

%3 = load i32, ptr %2, align 4
%4 = mult nsw i32 1, %3

 store i32 %3, ptr %4, align 4
;//this is function f

ret i32 1
}
