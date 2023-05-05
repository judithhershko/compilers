;//intf(intx){for(intz=0;z<5;z=z+1){x=1+1;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int z;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//for(intz=0;z<5;z=z+1){x=1+1;}

;//intz=0

;//z=z+1

store i32 0, i32* %3, align 4
br label %4
4:
 %5 = load i32, ptr %3, align 4
%6 = icmp slt i32 %5, 5

br i1 %6, label %7, label %9
7:
 %8 = load i32, ptr %2, align 4
;//x=1+1

store i32 2, i32* %8, align 4
store i32 1, i32* %6, align 4
br label %4
9:
ret i32 1
}
