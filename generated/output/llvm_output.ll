;//#include <stdio.h>

;//intf(intx){//this is function freturn1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4
;//intx

;//this is function f


;//intmain2(){intz=0;intx=0;z=z+f(z);z=90+x;inta[3]={0,1,2};z=a[0]+90;returnz;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4

;//intz=0

;//intx=0

;//z=z+f(z)

;//z=90+x

;//inta[3]={0,1,2}

;//intmain2(){intz=0;intx=0;z=z+f(z);z=90+x;inta[3]={0,1,2};z=a[0]+90;returnz;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { ] , align 4 
;//z=a[0]+90


store i32 0, i32* %1, align 4
store i32 0, i32* %2, align 4
store i32 90, i32* %1, align 4
store i32 90, i32* %1, align 4
 %4 = load ptr, ptr %1, align 4
ret i32 %4}
