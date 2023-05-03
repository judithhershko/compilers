;//#include <stdio.h>

;//intf(intx){//this is function freturn1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4
;//intx

;//this is function f


;//intmain2(){intz=0;intx=0;//int *xp=&x;z=z+f();z=90+x;//int a[3]={0,1,2};//z=a[0]+90;return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4

;//intz=0

;//intx=0

;//int *xp=&x;

;//z=z+f()

;//z=90+x

;//int a[3]={0,1,2};

;//z=a[0]+90;


store i32 0, i32* %1, align 4
store i32 0, i32* %2, align 4
%3 = call i32 @f()
%4 = load i32, ptr %3, align 4
%5 = add nsw i32 0, %4

store i32 90, i32* %1, align 4
