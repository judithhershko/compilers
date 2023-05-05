;//intmain(intx){x=0;{intx=90;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 {
%2 = alloca i32, align 4
 %3 = alloca i32, align 4
;  int x;
%4 = alloca i32, align 4

store i32 %0, ptr %2, align 4
store i32 %0, ptr %3, align 4

;//intx

;//x=0

store i32 0, i32* %3, align 4
;//intx=90

store i32 90, i32* %4, align 4
ret i32 1
}
