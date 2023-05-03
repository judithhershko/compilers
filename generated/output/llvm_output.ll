;//intf(intx){//this is function freturn1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//this is function f

ret i32 1
}
;//intmain2(intk){inta[3]={0,1,2};//a[0]=90;intz=0;intx=0;//int *xp=&x;z=!k+f();z=90+x;//z=a[0]+90;return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int z;
%3 = alloca i32, align 4
;  int x;
%4 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intk

;//inta[3]={0,1,2}

;//intmain2(intk){inta[3]={0,1,2};//a[0]=90;intz=0;intx=0;//int *xp=&x;z=!k+f();z=90+x;//z=a[0]+90;return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2(i32 noundef %0) #0 { ] , align 4 
;//a[0]=90;

;//intz=0

store i32 0, i32* %3, align 4
;//intx=0

store i32 0, i32* %4, align 4
;//int *xp=&x;

;//z=!k+f()

%6 = load i32, ptr %2, align 4
%6 = icmp ne i32 %7, 0
%8 = xor i1 %7, true

 store i32 %8, ptr %3, align 4
;//z=90+x

store i32 90, i32* %3, align 4
;//z=a[0]+90;

ret ptr %8}
