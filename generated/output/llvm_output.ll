;//intf(intb,chara){b=b+1;returnb+1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @f(i32 noundef %0,i8 noundef %1) #0 { 
%3 = alloca i32, align 4
%4 = alloca i8, align 4
 %5 = alloca i32, align 4

store i32 %0, ptr %3, align 4
store i8 %1, ptr %4, align 4
store i32 %1, ptr %5, align 4

;//intb

;//chara

;//b=b+1

%6 = load i32, ptr %5, align 4
%7 = load i32, ptr %5, align 4
%8 = add nsw i32 %7, 1

 store i32 %8, ptr %5, align 4
%10 = add nsw i32 %9, 1

ret ptr %10}
;//intmain(){intx=5+1;charz='a';inty=f(x,z);return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 { 
;  int x;
%1 = alloca i32, align 4
;  char z;
%2 = alloca i8, align 1
;  int y;
%3 = alloca i32, align 4


;//intx=5+1

store i32 6, i32* %1, align 4
;//charz='a'

store i8 97, i8* %2, align 1
;//inty=f(x,z)

 store i32 %3, ptr %3, align 4
ret i32 1
}
