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
#//intmain(){intu[2]={1,2};return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intu[2]={1,2}
addi $t0, $zero, 0
addi $t1, $zero, 1
 sw $t1, $$1($t0)
addi $t0, $t0, 4
addi $t1, $zero, 2
 sw $t1, $$1($t0)
addi $t0, $t0, 4
li $v0, 0
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
