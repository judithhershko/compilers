;//intmain2(){intz=0;intx=0;z=z+f(z,x);z=90+x;inta[3];z=a[0]+90;returnz;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4

;//intz=0

;//intx=0

;//z=z+f(z,x)

;//z=90+x

;//inta[3]

;//z=a[0]+90


store i32 0, i32* %1, align 4
store i32 0, i32* %2, align 4
store i32 90, i32* %1, align 4
store i32 90, i32* %1, align 4
 %4 = load ptr, ptr %1, align 4
ret i32 %4}
