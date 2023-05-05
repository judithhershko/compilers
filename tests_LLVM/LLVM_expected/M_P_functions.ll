;//intf(intx,floatz,intk){return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,float noundef %1,i32 noundef %2) #0 {
%4 = alloca i32, align 4
%5 = alloca float, align 4
%6 = alloca i32, align 4

store i32 %0, ptr %4, align 4
store float %1, ptr %5, align 4
store i32 %2, ptr %6, align 4

;//intx

;//floatz

;//intk

ret i32 1
}
;//intmain(intx){intk=90;return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 {
%2 = alloca i32, align 4
;  int k;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//intk=90

store i32 90, i32* %3, align 4
ret i32 1
}
