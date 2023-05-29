.data
$$1: .float 90.9
$$2: .float 90.9
$$3: .float 90.9
$$4: .float 2.2
$$5: .float 90.9
$$6: .float 90.9
$$7: .float 90.9
$$8  :.asciiz  "y is :  " 
$$9  :.asciiz "  en int is :  " 
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
#//float**ppx=&px
#//floatz=*px
mov.s $f3, $f1
#//floatf=90.9*z+z
lwc1 $f5, $$1
mul.s $f4,$f5, $f3
s.s $f4, -28($fp)
lwc1 $f6, $$2
add.s $f4,$f6, $f3
s.s $f4, -28($fp)
lwc1 $f7, $$3
mul.s $f4,$f7, $f3
s.s $f4, -28($fp)
mov.s $f0,$f0
l.s $f4, -28($fp)
l.s $f3, -24($fp)
l.s $f2, -12($fp)
l.s $f1, -12($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(intx){floatf=fff(1,2.2);float*px=&f;*px=x;floatz=*px;floatff=90.9*(z)+z;while(z<x){z=z+1;}printf("y is : %d en int is : %i ",f,x*x+89);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,28
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f8, -12($fp)
s.s   $f9, -16($fp)
s.s   $f10, -20($fp)
s.s   $f10, -24($fp)
#//intx
#//floatf=fff(1,2.2)
ori $a0, $zero, 1
sw $a1, -24($fp)
lwc1 $f10, $$4
mfc1 $a1, $f10
jal fff
mov.s $f8, $f0
#//float*px=&f
#//*px=x
s.s $f9, -12($fp)
mov.s $f9, $s0
l.s $f9, -12($fp)
#//floatz=*px
mov.s $f10, $f9
#//floatff=90.9*(z)+z
lwc1 $f10, $$5
mul.s $f10,$f10, $f10
s.s $f10, -24($fp)
lwc1 $f10, $$6
add.s $f10,$f10, $f10
s.s $f10, -24($fp)
lwc1 $f10, $$7
mul.s $f10,$f10, $f10
s.s $f10, -24($fp)
#//while(z<x){z=z+1;}
j $loop1
nop
$loop1:
lw  $s0, -8($fp)
slt $1,$f10, $s0
sw $1, -28($fp)
lbu $1, -28($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop 
j $loop2
nop
$loop2:
#//z=z+1
ori $t0,$0,1
addu $f10,$f10, $t0
s.s $f10, -24($fp)
j $loop1
nop
$loop3:
#//printf("y is : %d en int is : %i ",f,x*x+89)
li $v0, 4
la $a0, $$8
syscall
li $v0, 1
move $a0, $f8
syscall
li $v0, 4
la $a0, $$9
syscall
sw $s1, -32($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -32($fp)
lw  $s0, -8($fp)
ori $t0,$0,89
addu $s1,$s0, $t0
sw $s1, -32($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -32($fp)
li $v0, 1
move $a0, $s1
syscall
li $v0, 0
lw $s1, -32($fp)
lw $1, -28($fp)
lw $a1, -24($fp)
l.s $f10, -24($fp)
l.s $f9, -12($fp)
l.s $f8, -12($fp)
l.s $f4, -28($fp)
l.s $f3, -24($fp)
l.s $f2, -12($fp)
l.s $f1, -12($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
