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
#//intmain(){inta=1;{intb=2;{intc=3;}}return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inta=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
#//intb=2
sw $s1, -12($fp)
lw  $s1, -12($fp)
ori $s1,$0,2
sw  $s1, -12($fp)
#//intc=3
sw $s2, -16($fp)
lw  $s2, -16($fp)
ori $s2,$0,3
sw  $s2, -16($fp)
li $v0, 0
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
