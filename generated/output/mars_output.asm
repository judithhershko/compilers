.data
$$1: .float 90.9
$$2: .float 90.9
$$3: .float 90.9
$$4: .float 90.9
$$5: .float 1.1
$$6  :.asciiz  "y is :  " 
$$7  :.asciiz "  en int is :  " 
.text
.globl main
j main
#//floatfff(intx,floatz){floatf=90.9*z+z;return90.9;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx
#//floatz
#//floatf=90.9*z+z
lwc1 $f2, $$1
mul.s $f1,$f2, $f0
lwc1 $f3, $$2
add.s $f1,$f3, $f0
lwc1 $f4, $$3
mul.s $f1,$f4, $f0
mov.s $f0, $f4
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(intx,floatz){floatf=fff(1,1.1);x=90;printf("y is : %f en int is : %i ",f,x*x+89);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx
#//floatz
#//floatf=fff(1,1.1)
ori $a0, $zero, 1
sw $a1, -16($fp)
lwc1 $f7, $$5
mfc1 $a1, $f7
jal fff
mov.s $f6, $f0
#//x=90
lw  $s0, -8($fp)
ori $s0,$0,90
sw  $s0, -8($fp)
#//printf("y is : %f en int is : %i ",f,x*x+89)
li $v0, 4
la $a0, $$6
syscall
li $v0, 2
mov.s $f12, $f6
syscall
li $v0, 4
la $a0, $$7
syscall
li $v0, 1
ori $t0, 8189
move $a0, $t0
syscall
li $v0, 0
lw $a1, -16($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
