@.str = private unnamed_addr constant [33x i8] c"(\0A\00", align 1
@.str.1 = private unnamed_addr constant [6x i8] c"N\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
; _Boolx=True
%2 = alloca i8, align 1
;  bool * z = & x
%3 = alloca ptr, align 8
;  bool ** y = & z
%4 = alloca ptr, align 8
; printf (()
%5 = call i32 (ptr, ...) @printf(ptr noundef @.str)
; printf (N)
%6 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
;  int zz = 0
%8 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i8 1, i8* %2, align 1
store ptr %2, ptr %3, align 8
store ptr %3, ptr %4, align 8
;//comment1

;/**multi
;line
;comment
;**/
store i32 0, i32* %8, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

