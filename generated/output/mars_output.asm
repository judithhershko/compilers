.data
.text
.globl main
j main
#//intmain(){intz=1;inta;intb;a+b;return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intz=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
#//inta
lw  $s1, -12($fp)
ori $s1,$0,0
sw  $s1, -12($fp)
#//intb
lw  $s2, -16($fp)
ori $s2,$0,0
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
