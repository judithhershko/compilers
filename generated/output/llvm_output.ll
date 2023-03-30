@.str = private unnamed_addr constant [33x i8] c"('True', <LiteralType.BOOL: 7>)\0A\00", align 1
@.str.1 = private unnamed_addr constant [32x i8] c"('8178', <LiteralType.INT: 5>)\0A\00", align 1
; Function Attrs: noinline nounwind optnone ssp uwtable(sync)

define i32 @main() #0 {
%1 = alloca i32, align 4
;  int v = 8178
%2 = alloca i32, align 4
; _Boolx=True
%3 = alloca i8, align 1
; _Boolxx=False
%4 = alloca i8, align 1
;  bool * z = & x
%5 = alloca ptr, align 8
;  bool * z = & xx
%6 = alloca ptr, align 8
;  bool ** y = & z
%7 = alloca ptr, align 8
; printf (()
%8 = call i32 (ptr, ...) @printf(ptr noundef @.str)
; printf (()
%9 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
;  char r = 'b'
%10 = alloca i8, align 1
;  char r = 'b'
%11 = alloca i8, align 1
;  int vv = 90
%12 = alloca i32, align 4

store i32 0, ptr %1, align 4
store i32 8178, i32* %2, align 4
store i8 1, i8* %3, align 1
store i8 0, i8* %4, align 1
store ptr %3, ptr %5, align 8
store ptr %4, ptr %6, align 8
store ptr %6, ptr %7, align 8
store i8 98, i8* %10, align 1
store i8 98, i8* %11, align 1
;//comment1

;/**multi
;line
;comment
;**/
store i32 90, i32* %12, align 4

ret i32 0
}

declare i32 @printf(ptr noundef, ...) #1

