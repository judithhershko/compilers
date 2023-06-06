.data
$$1: .space 8
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=2;int*p=&x;inty[2];y[0]=3;y[1]=4;intr=x**p+y[0]*y[1];return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
#//intx=2
lw  $s0, -8($fp)
ori $s0,$0,2
sw  $s0, -8($fp)
#//int*p=&x
move $s1,$s0
#//inty[2]
addi $t0, $zero, 0
#//y[0]=3
addi $t0,$zero, -4
addi $t1, $zero, 3
sw $t1, $$1($t0)
addi $t0,$zero, -4
addi $t1, $zero, 3
sw $t1, $$1($t0)
#//y[1]=4
addi $t0,$zero, 0
addi $t1, $zero, 4
sw $t1, $$1($t0)
addi $t0,$zero, 0
addi $t1, $zero, 4
sw $t1, $$1($t0)
#//intr=x**p+y[0]*y[1]
lw  $s5, -28($fp)
ori $s5,$0,16
sw  $s5, -28($fp)
li $v0, 0
lw $s5, -28($fp)
lw $s4, -24($fp)
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -8($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
