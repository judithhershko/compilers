.data
.text
.globl main
j main
#//intmain(){intx[2];x[0]=5;x[1]=6;inty=x[0];return1;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
#//intx[2]
#//x[0]=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//x[1]=6
lw  $s0, -8($fp)
ori $s0,$0,6
sw  $s0, -8($fp)
#//inty=x[0]
li $v0, 1
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
