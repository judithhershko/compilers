;//intf(intx){//this is function freturn1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0) #0 { 
%2 = alloca i32, align 4

store i32 %0, ptr %2, align 4

;//intx

;//this is function f

ret i32 1
}
;//intmain2(){inta[3]={0,1,2};//a[0]=90;intz=0;intx=0;//int *xp=&x;z=z+f();z=90+x;//z=a[0]+90;//todo:{z=90;}return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { 
;  int z;
%1 = alloca i32, align 4
;  int x;
%2 = alloca i32, align 4


;//inta[3]={0,1,2}

;//intmain2(){inta[3]={0,1,2};//a[0]=90;intz=0;intx=0;//int *xp=&x;z=z+f();z=90+x;//z=a[0]+90;//todo:{z=90;}return1+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main2() #0 { ] , align 4 
;//a[0]=90;

;//intz=0

store i32 0, i32* %1, align 4
;//intx=0

store i32 0, i32* %2, align 4
;//int *xp=&x;

;//z=z+f()

 store i32 %2, ptr %1, align 4
;//z=90+x

store i32 90, i32* %1, align 4
;//z=a[0]+90;

;//todo:

;//z=90

store i32 90, i32* %1, align 4
ret ptr %2}
