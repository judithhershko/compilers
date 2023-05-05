;//intx=90

;//intmain(intx){intk=90;k=k+23;return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 {
%2 = alloca i32, align 4
;  int x = 90
@x = global i32 90, align 4
;  int k;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//intk=90

store i32 90, i32* %3, align 4
;//k=k+23

store i32 113, i32* %3, align 4
ret i32 1
}
