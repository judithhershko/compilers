.data
.text
.globl main
j main
#//intmain(){intz=2;{scanf(" val is: %d and %d",z*z,z);}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intz=2
lw  $s0, -8($fp)
ori $s0,$0,2
sw  $s0, -8($fp)
#//scanf(" val is: %d and %d",z*z,z)
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
