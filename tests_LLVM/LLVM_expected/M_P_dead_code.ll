;//intx=90

;//intmain(intx){floatk=90;k=k+23;return1;intf=90;f=89+f;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 {
%2 = alloca i32, align 4
;  int x = 90
@x = global i32 90, align 4
;  float k;
%3 = alloca float, align 4

store i32 %0, ptr %2, align 4

;//intx

;//floatk=90

store float 0x4056800000000000, float* %3, align 4
;//k=k+23

store float 0x405c400000000000, float* %3, align 4
ret i32 1
}
