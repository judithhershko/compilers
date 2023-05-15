.data
$$1  :.asciiz "y is :  "
.text
.globl main
#//intmain(intx){//this is a commentinty=90;intz=y;printf("y is : %d ",y);return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,20	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intx
#//this is a comment
#//inty=90
lw  $s1, -12($fp)
ori $s1,$0,90
sw  $s1, -12($fp)
#//intz=y
lw  $s2, -16($fp)
ori $s2,$0,90
sw  $s2, -16($fp)
#//printf("y is : %d ",y)
li $v0, 4
la $a0, $$1
syscall
lw	$s2, -16($fp)
lw	$s1, -12($fp)
lw	$s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
