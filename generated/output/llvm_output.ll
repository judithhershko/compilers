@__const..z = private unnamed_addr constant [3 x i32] [i32 0,i32 1,i32 2] , align 4 
;//intmain(intx){intz[3]={0,1,2};return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
%3 = alloca [ 3 x i32], align 4

store i32 %0, ptr %2, align 4

;//intx

;//intz[3]={0,1,2}

ret i32 1
}
