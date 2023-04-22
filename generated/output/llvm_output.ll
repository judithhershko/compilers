
;  int integer = 5
@integer = global i32 5, align 4
;  int * int_ptr = & integer
%1 = alloca ptr, align 8
;  int ** ptr_ptr = & int_ptr
%3 = alloca ptr, align 8
;  int z = 10
@z = global i32 10, align 4
;  int * pointer = & z
%4 = alloca ptr, align 8
;  int x = 10
@x = global i32 10, align 4
;  int ** x_ptr = & int_ptr
%6 = alloca ptr, align 8

store ptr %2, ptr %1, align 8
store ptr %1, ptr %3, align 8
store ptr %5, ptr %4, align 8
store ptr %1, ptr %6, align 8


