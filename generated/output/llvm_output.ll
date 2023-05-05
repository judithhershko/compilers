declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [41x i8] c"<src.ast.AST.AST object at 0x120bbd750>\0A\00", align 1
;//intmain(intx,inty){x=x+1*x+89;printf("%d",x+x*2,x+y);for(intk=0;k<5;k=k+1){x=x+1;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4
;  int k;
%6 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intx

;//inty

;//x=x+1*x+89

%7 = load i32, ptr %5, align 4
%8 = load i32, ptr %5, align 4
%9 = add nsw i32 %8, 89

%10 = add nsw i32 %8, %9

%11 = mul nsw i32 1, %10

 store i32 %11, ptr %5, align 4
;//printf("%d",x+x*2,x+y)

; printf (<src.ast.AST.AST object at 0x120bbd750>)
%12 = call i32 (ptr, ...) @printf(ptr noundef @.str)
;//for(intk=0;k<5;k=k+1){x=x+1;}

;//intk=0

;//k=k+1

store i32 0, i32* %6, align 4
br label %13
13:
 %14 = load i32, ptr %6, align 4
%15 = icmp slt i32 %14, 5

br i1 %15, label %16, label %26
16:
 %17 = load i32, ptr %5, align 4
;//x=x+1

 %18 = load i32, ptr %5, align 4
%19 = load i32, ptr %5, align 4
%20 = load i32, ptr %5, align 4
%21 = add nsw i32 %20, 1

 store i32 %21, ptr %5, align 4
 %22 = load i32, ptr %6, align 4
%23 = load i32, ptr %6, align 4
%24 = load i32, ptr %6, align 4
%25 = add nsw i32 %24, 1

 store i32 %25, ptr %6, align 4
br label %13
26:
ret i32 1
}
