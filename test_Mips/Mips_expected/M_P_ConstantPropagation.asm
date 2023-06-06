.data
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=5;inty=x*2;intz=x-y;intu=x+y*z;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//inty=x*2
lw  $s1, -12($fp)
ori $s1,$0,10
sw  $s1, -12($fp)
#//intz=x-y
move $s2, $s4
sw $s2, -16($fp)
#//intu=x+y*z
move $s3, $s5
sw $s3, -20($fp)
li $v0, 0
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
