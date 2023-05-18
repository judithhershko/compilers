.data
.text
.globl main
j main
#// Should print the numbers: 42 42 43 43 44 44 45 45
#//intmain(){intx=0;int*xp=&x;*xp=42;int**p=&xp;inty=1;int*yp=&y;*yp=5;return1;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,28
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
#//intx=0
lw  $s0, -8($fp)
ori $s0,$0,0
sw  $s0, -8($fp)
#//int*xp=&x
lw  $s1, -12($fp)
sw $s1, -8($fp)
#//*xp=42
lw  $s1, -12($fp)
ori $s1,$0,42
sw  $s1, -12($fp)
#//int**p=&xp
lw  $s2, -16($fp)
sw $s2, -12($fp)
#//inty=1
lw  $s3, -20($fp)
ori $s3,$0,1
sw  $s3, -20($fp)
#//int*yp=&y
lw  $s4, -24($fp)
sw $s4, -20($fp)
#//*yp=5
lw  $s4, -24($fp)
ori $s4,$0,5
sw  $s4, -24($fp)
li $v0, 1
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
