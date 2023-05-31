.data
$$1: .space 8
$$2: .space 8
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=2;int*p=&x;inty[2];intyy[2]={1,2};y[0]=3;y[1]=4;intr=x**p+y[0]*y[1];return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,44
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
sw	$s6, -32($fp)
sw s0, -8($fp)
sw s1, -12($fp)
sw s2, -16($fp)
sw s3, -20($fp)
sw s4, -24($fp)
sw s5, -28($fp)
sw s6, -32($fp)
sw	$s0, -36($fp)
sw	$s1, -40($fp)
#//intx=2
sw $s2, -40($fp)
lw  $s2, -40($fp)
ori $s2,$0,2
sw  $s2, -40($fp)
#//int*p=&x
sw $s3, -40($fp)
move $s3,$s2
#//inty[2]
addi $t0, $zero, 0
#//intyy[2]={1,2}
addi $t0, $zero, 0
addi $t1, $zero, 1
sw $t1, yy($t0)
addi $t0, $t0, 4
addi $t1, $zero, 2
 sw $t1, yy($t0)
addi $t0, $t0, 4
#//y[0]=3
sw $s4, -40($fp)
lw  $s4, -40($fp)
ori $s4,$0,3
sw  $s4, -40($fp)
#//y[1]=4
lw  $s4, -40($fp)
ori $s4,$0,4
sw  $s4, -40($fp)
#//intr=x**p+y[0]*y[1]
lw  $s1, -40($fp)
ori $s1,$0,16
sw  $s1, -40($fp)
li $v0, 0
lw $s6, -32($fp)
lw $s5, -28($fp)
lw $s4, -40($fp)
lw $s3, -40($fp)
lw $s2, -40($fp)
lw $s1, -40($fp)
lw $s0, -36($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
