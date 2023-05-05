@__const.main.v = private unnamed_addr constant [3 x i32] [i32 1,i32 2,i32 3] , align 4 
;//intf(intx,floatz,intk){return90;}

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

ret i32 90
}
;//intmain(intx){intk[2];intv[3]={1,2,3};intf=10;while(f<10){f=f+1;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int f;
%3 = alloca i32, align 4
%4 = alloca [ 2 x i32], align 4
%5 = alloca [ 3 x i32], align 4

store i32 %0, ptr %2, align 4

;//intx

;//intk[2]

;//intv[3]={1,2,3}

;//intf=10

store i32 10, i32* %3, align 4
;//while(f<10){f=f+1;}

br label %6
6:
%8 = icmp slt i32 %7, 10

br i1 %8, label %9, label %10
9:
;//f=f+1

store i32 11, i32* %3, align 4
br label %6
10:
ret i32 1
}
