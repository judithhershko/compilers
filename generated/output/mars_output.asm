.data
$$1: .float 0.0
$$2: .float 0.0
$$3: .float 90.9
$$4: .float 90.9
$$5: .float 90.9
$$6: .float 2.2
$$7  :.asciiz  "y is :  " 
$$8  :.asciiz "  en int is :  " 
.text
.globl main
j main
#//floatfff(intx,floatfx){float*px=&fx;float**ppx=&px;floatz=*px;floatf=90.9*z+z;returnfx;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f0, -12($fp)
s.s   $f1, -16($fp)
s.s   $f2, -20($fp)
s.s   $f3, -24($fp)
s.s   $f4, -28($fp)
#//intx
#//floatfx
#//float*px=&fx
swc1  $f0, $$1
la    $t0, $$1
lwc1  $f1, ($t0)
#//float**ppx=&px
swc1  $f1, $$2
la    $t0, $$2
lwc1  $f2, ($t0)
#//floatz=*px
mov.s $f3, $f1
#//floatf=90.9*z+z
lwc1 $f5, $$3
mul.s $f4,$f5, $f3
s.s $f4, -28($fp)
lwc1 $f6, $$4
add.s $f4,$f6, $f3
s.s $f4, -28($fp)
lwc1 $f7, $$5
mul.s $f4,$f7, $f3
s.s $f4, -28($fp)
mov.s $f0,$f0
l.s $f4, -28($fp)
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
s.s   $f8, -12($fp)
s.s   $f9, -16($fp)
#//intx
#//floatz
#//floatf=fff(1,2.2)
ori $a0, $zero, 1
sw $a1, -16($fp)
lwc1 $f10, $$6
mfc1 $a1, $f10
jal fff
mov.s $f9, $f0
#//x=90
lw  $s0, -8($fp)
ori $s0,$0,90
sw  $s0, -8($fp)
#//printf("y is : %i en int is : %i ",x,x*x+89)
li $v0, 4
la $a0, $$7
syscall
li $v0, 1
li $t0, 90
move $a0, $t0
syscall
li $v0, 4
la $a0, $$8
syscall
li $v0, 1
li $t1, 8189
move $a0, $t1
syscall
li $v0, 0
lw $a1, -16($fp)
l.s $f9, -16($fp)
l.s $f8, -12($fp)
l.s $f4, -28($fp)
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
