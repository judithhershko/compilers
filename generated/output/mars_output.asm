.data
.text
.globl main
j main
#//intmain(){intz=1;intx[3];x[z-1]=5;x[z]=6;x[1+z]=7;inty=x[z-1];intw=x[z];intv=x[1+z];return1;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,40
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
sw	$s6, -32($fp)
sw	$s7, -36($fp)
#//intz=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
#//intx[3]
#//x[z-1]=5
lw  $s1, -12($fp)
ori $s1,$0,5
sw  $s1, -12($fp)
#//x[z]=6
lw  $s1, -12($fp)
ori $s1,$0,6
sw  $s1, -12($fp)
#//x[1+z]=7
lw  $s1, -12($fp)
ori $s1,$0,7
sw  $s1, -12($fp)
#//inty=x[z-1]
#//intw=x[z]
#//intv=x[1+z]
li $v0, 1
lw $s7, -36($fp)
lw $s6, -32($fp)
lw $s5, -28($fp)
lw $s4, -24($fp)
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
