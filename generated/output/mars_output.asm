.data
.text
.globl main
j main
#//intf(inta){a=a*a;returna;}
f: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inta
#//a=a*a
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s0,$s0, $s0
sw $s0, -8($fp)
move $v0, $s0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){int*a;int*b;return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,16
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//int*a
sw $s2, -12($fp)
sw $s2, ($s0)
#//int*b
sw $s2, ($s1)
li $v0, 0
lw $s2, -12($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
