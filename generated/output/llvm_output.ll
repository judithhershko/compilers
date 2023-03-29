@.str = private unnamed_addr constant [3x i8] c"91\00", align 1
@.str.1 = private unnamed_addr constant [3x i8] c"90\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
//  int d = 7087
%2 = alloca i32, align 4
//  int v = 90
%3 = alloca i32, align 4
//  int x = 91
%4 = alloca i32, align 4
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str)
%6 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
//  int zz = 0
%7 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 7087, i32* %2, align 4
//d=90;

//bool vv= 34+8>89;

store i32 90, i32* %3, align 4
store i32 91, i32* %4, align 4
//comment1

///**multi
//line
//comment
//**/
store i32 0, i32* %7, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

