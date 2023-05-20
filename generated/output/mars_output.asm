.data
.text
.globl main
j main
#//intmain(){intx=5;int*xp=&x;inty=*xp;return1;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//int*xp=&x
lw  $s1, -12($fp)
sw $s1, -8($fp)
#//inty=*xp
li $v0, 1
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
