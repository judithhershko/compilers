.data
$$1: .float 0.0
$$2: .float 90.9
$$3: .float 90.9
$$4: .float 90.9
$$5: .float 2.2
$$6  :.asciiz  "y is :  " 
$$7  :.asciiz "  en int is :  " 
.text
.globl main
j main
#//floatfff(intx,floatfx){float*px=&fx;floatz=*px;floatf=90.9*z+z;returnfx;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,28
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f0, -12($fp)
s.s   $f1, -16($fp)
s.s   $f2, -20($fp)
s.s   $f3, -24($fp)
#//intx
#//floatfx
#//float*px=&fx
swc1  $f0, $$1
la    $t0, $$1
lwc1  $f1, ($t0)
#//floatz=*px
mov.s $f2, $f1
#//floatf=90.9*z+z
lwc1 $f4, $$2
mul.s $f3,$f4, $f2
s.s $f3, -24($fp)
lwc1 $f5, $$3
add.s $f3,$f5, $f2
s.s $f3, -24($fp)
lwc1 $f6, $$4
mul.s $f3,$f6, $f2
s.s $f3, -24($fp)
mov.s $f0,$f0
l.s $f3, -24($fp)
l.s $f2, -20($fp)
l.s $f1, -16($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(intx,floatz){floatf=fff(1,2.2);x=90;printf("y is : %i en int is : %i ",x,x*x+89);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f7, -12($fp)
s.s   $f8, -16($fp)
#//intx
#//floatz
#//floatf=fff(1,2.2)
ori $a0, $zero, 1
sw $a1, -16($fp)
lwc1 $f9, $$5
mfc1 $a1, $f9
jal fff
mov.s $f8, $f0
#//x=90
lw  $s0, -8($fp)
ori $s0,$0,90
sw  $s0, -8($fp)
#//printf("y is : %i en int is : %i ",x,x*x+89)
li $v0, 4
la $a0, $$6
syscall
li $v0, 1
ori $t0, 90
move $a0, $t0
syscall
li $v0, 4
la $a0, $$7
syscall
li $v0, 1
ori $t1, 8189
move $a0, $t1
syscall
li $v0, 0
lw $a1, -16($fp)
l.s $f8, -16($fp)
l.s $f7, -12($fp)
l.s $f3, -24($fp)
l.s $f2, -20($fp)
l.s $f1, -16($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
