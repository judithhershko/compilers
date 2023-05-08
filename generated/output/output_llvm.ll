declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%i\00", align 1
;//constintxx=90

;//constinty=89+9*(8/78+89)*(5-89)

;//voidff(floaty){return;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define void @ff(float noundef %0) #0 { 
%2 = alloca float, align 4

store float %0, ptr %2, align 4

;//floaty

ret void}
;//floatf(intx,floaty){x=x-1;y=y+1;x<=y;12>=78;!79;{intx=90;}printf("%i",x);return1.1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define float @f(i32 noundef %0,float noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca float, align 4
 %5 = alloca i32, align 4
 %6 = alloca float, align 4
; const int xx = 90
@xx = global i32 90, align 4
; const int y = -67195
@y = global i32 -67195, align 4
;  int x;
%17 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store float %1, ptr %4, align 4
store i32 %1, ptr %5, align 4
store float %1, ptr %6, align 4

;//intx

;//floaty

;//x=x-1

%7 = load i32, ptr %5, align 4
%8 = load i32, ptr %5, align 4
%9 = sub nsw i32 %8, 1

 store i32 %9, ptr %5, align 4
;//y=y+1

%10 = load float, ptr %6, align 4
%11 = load float, ptr %6, align 4
%13 = sitofp i32 %12 to float
%14 = add nsw i32 %11, 1

 store float %14, ptr %6, align 4
%16 = sitofp i32 %14 to float
%16 = fcmp ole float %14, %14

;//intx=90

store i32 90, i32* %17, align 4
;//printf("%i",x)

; printf ("%i")
%18 = call i32 (ptr, ...) @printf(ptr noundef @.str ,  i32 noundef 17)
ret float 1.1
}
;//intmain(){intx=0;floaty=9.90;y=89+9*(8/78+89)*(5-89);34>78;while(y>=789){x=x+78;break;}if(x<=89){x=x+90;}else{y=(89+89)+90;break;y=y+2;}x=!x;floatz=f(1,1.1);//pointersintp=90;int*pp=&p;int**ppp=&pp;return1;x=x+90;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 
;  int x;
%1 = alloca i32, align 4
;  float y;
%2 = alloca float, align 4
;  int p;
%5 = alloca i32, align 4
;  int * pp = & p
%6 = alloca ptr, align 8
;  int ** ppp = & pp
%7 = alloca ptr, align 8


%3 = alloca float, align 4
%4 = call float @f ( i32 noundef 0,float noundef 0x3ff0000000000000)
store float %4, ptr %3, align 4
store ptr %5, ptr %6, align 8
store ptr %6, ptr %7, align 8
;//intx=0

store i32 0, i32* %1, align 4
;//floaty=9.90

store float 0x4023ccccc0000000, float* %2, align 4
;//y=89+9*(8/78+89)*(5-89)

store float 0xc0f067b000000000, float* %2, align 4
;//while(y>=789){x=x+78;break;}

br label %8
8:
%11 = sitofp i32 %10 to float
%12 = icmp sge i32 %9, 789

br i1 %12, label %13, label %14
13:
;//x=x+78

store i32 78, i32* %1, align 4
br label %14
14 :
;//if(x<=89){x=x+90;}

%15 = icmp sle i32 %14, 89

br i1 %15, label %16, label %20
16:
;//x=x+90

%17 = load i32, ptr %1, align 4
%18 = load i32, ptr %1, align 4
%19 = add nsw i32 %18, 90

 store i32 %19, ptr %1, align 4
br label %22
20:
;//else{y=(89+89)+90;break;y=y+2;}

;//y=(89+89)+90

store float 0x4070c00000000000, float* %2, align 4
br label %21
21 :
br label %22
22:
;//x=!x

%23 = load i32, ptr %1, align 4
%23 = icmp ne i32 %24, 0
%25 = xor i1 %24, true

 store i32 %26, ptr %1, align 4
;//floatz=f(1,1.1)

%27 = alloca float, align 4
%28 = call float @f ( i32 noundef 0,float noundef 0x3ff0000000000000)
store float %28, ptr %27, align 4
;//pointers

;//intp=90

store i32 90, i32* %5, align 4
;//int*pp=&p

store ptr %5, ptr %6, align 8
;//int**ppp=&pp

store ptr %6, ptr %7, align 8
ret i32 1
}
