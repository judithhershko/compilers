;//intf(intx){//this is function finty=0;y=y+90;return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int y;
%3 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//this is function f

;//inty=0

store i32 0, i32* %3, align 4
;//y=y+90

store i32 90, i32* %3, align 4
ret i32 1
}
;//intmain2(intk){return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intk

ret i32 1
}
