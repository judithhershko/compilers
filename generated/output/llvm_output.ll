@.str = private unnamed_addr constant [4x i8] c"91\0A\00", align 1
@.str.1 = private unnamed_addr constant [4x i8] c"90\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
//  int d = 7087
%2 = alloca i32, align 4
//  int v = 90
%3 = alloca i32, align 4
//  int x = 91
%4 = alloca i32, align 4
//  int * z = & x
%5 = alloca ptr, align 8
//  int ** y = & z
%6 = alloca ptr, align 8
// printf (91)
%7 = call i32 (ptr, ...) @printf(ptr noundef @.str)
// printf (90)
%8 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
//  int zz = 0
%9 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 7087, i32* %2, align 4
//d=90;

//bool vv= 34+8>89;

store i32 90, i32* %3, align 4
store i32 91, i32* %4, align 4
store ptr %4, ptr %5, align 8
store ptr %5, ptr %6, align 8
//comment1

///**multi
//line
//comment
//**/
store i32 0, i32* %9, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

