declare i32 @printf(ptr noundef, ...) #1
@.str = private unnamed_addr constant [41x i8] c"<src.ast.AST.AST object at 0x123cf3810>\0A\00", align 1
;//intmain(intx,inty){x=x+1*x+89;charxi='a';printf("%d",x+x*2,x+y);for(intk=0;k<5;k=k+1){x=x+1;}return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main(i32 noundef %0,i32 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i32, align 4
 %5 = alloca i32, align 4
;  char xi;
%6 = alloca i8, align 1
;  int k;
%7 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i32 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intx

;//inty

;//x=x+1*x+89

%8 = load i32, ptr %5, align 4
%9 = load i32, ptr %5, align 4
%10 = add nsw i32 %9, 89

%11 = add nsw i32 %9, %10

%12 = mul nsw i32 1, %11

 store i32 %12, ptr %5, align 4
;//charxi='a'

store i8 97, i8* %6, align 1
;//printf("%d",x+x*2,x+y)

; printf (<src.ast.AST.AST object at 0x123cf3810>)
%13 = call i32 (ptr, ...) @printf(ptr noundef @.str)
;//for(intk=0;k<5;k=k+1){x=x+1;}

;//intk=0

;//k=k+1

store i32 0, i32* %7, align 4
br label %14
14:
 %15 = load None, ptr %7, align 4
%16 = icmp slt i32 %15, 5

%17 = icmp ne i32 %16, 0
br i1 %17, label %18, label %28
18:
 %19 = load i32, ptr %5, align 4
;//x=x+1

 %20 = load i32, ptr %5, align 4
%21 = load i32, ptr %5, align 4
%22 = load i32, ptr %5, align 4
%23 = add nsw i32 %22, 1

 store i32 %23, ptr %5, align 4
 %24 = load None, ptr %7, align 4
%25 = load i32, ptr %7, align 4
%26 = load i32, ptr %7, align 4
%27 = add nsw i32 %26, 1

 store i32 %27, ptr %7, align 4
br label %14
28:
ret i32 1
}
