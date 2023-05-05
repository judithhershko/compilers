@__const..z = private unnamed_addr constant [3 x i32] [i32 0,i32 1,i32 2] , align 4 
declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [9x i8] c""%d %d"\0A\00", align 1
;//intmain(intx){intz[3]={0,1,2};inty=0;//z[2]=9;printf("%d %d",x,y);return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0) #0 { 
%2 = alloca i32, align 4
;  int y;
%3 = alloca i32, align 4
%4 = alloca [ 3 x i32], align 4

store i32 %0, ptr %2, align 4

;//intx

;//intz[3]={0,1,2}

;//inty=0

store i32 0, i32* %3, align 4
;//z[2]=9;

;//printf("%d %d",x,y)

; printf ("%d %d")
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str , Nonenoundef 3, Nonenoundef 3)
ret i32 1
}
