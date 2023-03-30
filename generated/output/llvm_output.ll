@.str = private unnamed_addr constant [33x i8] c"(\0A\00", align 1
@.str.1 = private unnamed_addr constant [6x i8] c"N\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
; _Boolx=True
%2 = alloca i8, align 1
; _Boolxx=False
%3 = alloca i8, align 1
;  bool * z = & x
%4 = alloca ptr, align 8
;  bool * z = & xx
%4 = alloca ptr, align 8
;  bool ** y = & z
%5 = alloca ptr, align 8
; printf (()
%6 = call i32 (ptr, ...) @printf(ptr noundef @.str)
; printf (N)
%7 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)

store i32 0, ptr %1, align 4
store i8 1, i8* %2, align 1
store i8 0, i8* %3, align 1
store ptr %2, ptr %4, align 8
store ptr %3, ptr %4, align 8
store ptr %4, ptr %5, align 8
;//comment1


ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

