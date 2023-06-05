.data
$$1: .float 856.25668
$$2  : .byte 'x'
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intinteger=5;int*ptr=&integer;int**ptr_ptr=&ptr;int**another_pointer=ptr_ptr;intz=integer+5;ptr=&z;int*pointer=&z;intx=*pointer;int**x_ptr=&ptr;floata=856.25668;float*a_ptr=&a;charc='x';char*char_ptr=&c;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,56
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
sw	$s6, -32($fp)
sw $s0, -8($fp)
sw $s1, -12($fp)
sw $s2, -16($fp)
sw $s3, -20($fp)
sw $s4, -24($fp)
sw $s5, -28($fp)
sw $s6, -32($fp)
sw	$s0, -36($fp)
s.s   $f0, -40($fp)
s.s   $f1, -44($fp)
sw	$s1, -48($fp)
sw	$s2, -52($fp)
#//intinteger=5
sw $s3, -52($fp)
lw  $s3, -52($fp)
ori $s3,$0,5
sw  $s3, -52($fp)
#//int*ptr=&integer
sw $s4, -52($fp)
move $s4,$s3
#//int**ptr_ptr=&ptr
sw $s5, -52($fp)
move $s5,$s4
#//int**another_pointer=ptr_ptr
sw $s6, -52($fp)
move $s6,$s5
#//intz=integer+5
sw $s0, -36($fp)
sw $s1, -48($fp)
sw $s2, -52($fp)
sw $s3, -52($fp)
sw $s4, -52($fp)
sw $s5, -52($fp)
sw $s6, -52($fp)
sw $s0, -52($fp)
lw  $s0, -52($fp)
ori $s0,$0,10
sw  $s0, -52($fp)
#//ptr=&z
sw $s1, -52($fp)
lw $s0, -52($fp)
move $s1, $s0
#//int*pointer=&z
sw $s2, -52($fp)
move $s2,$s0
#//intx=*pointer
sw $s3, -52($fp)
lw  $s3, -52($fp)
ori $s3,$0,10
sw  $s3, -52($fp)
#//int**x_ptr=&ptr
sw $s4, -52($fp)
move $s4,$s1
#//floata=856.25668
lwc1 $f2, $$1
#//float*a_ptr=&a
mov.s $f1,$f0
#//charc='x'
sw $s5, -52($fp)
lb $s5 , $$2
sb $s5, -52($fp)
#//char*char_ptr=&c
sw $s6, -52($fp)
move $s6,$s5
li $v0, 0
l.s $f1, -40($fp)
l.s $f0, -40($fp)
lw $s6, -52($fp)
lw $s5, -52($fp)
lw $s4, -52($fp)
lw $s3, -52($fp)
lw $s2, -52($fp)
lw $s1, -52($fp)
lw $s0, -52($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
