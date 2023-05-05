;//intmain(){intz=0;z=1+2+3*89;intk=90-89;floatf=8.90;f=f/89.90;return1;}

; Function Attrs: noinline nounwind optnone ssp uwtable(sync)
define i32 @main() #0 {
;  int z;
%1 = alloca i32, align 4
;  int k;
%2 = alloca i32, align 4
;  float f;
%3 = alloca float, align 4


;//intz=0

store i32 0, i32* %1, align 4
;//z=1+2+3*89

store i32 270, i32* %1, align 4
;//intk=90-89

store i32 1, i32* %2, align 4
;//floatf=8.90

store float 0x4021ccccc0000000, float* %3, align 4
;//f=f/89.90

store float 0x3fb957fdc0000000, float* %3, align 4
ret i32 1
}
