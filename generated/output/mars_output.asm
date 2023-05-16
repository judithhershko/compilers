.data
$$1  :.asciiz "y is :  "
.text
.globl main
#//intf(intx){//x=!x;//this is a commentinty=!x;printf("y is : %d ",x);}
f: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,16	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intx
#//x=!x;
#//this is a comment
#//inty=!x
lw  $s0, -8($fp)
nor $s1, $s0 ,$zero
sw $s1, -12($fp)
#//printf("y is : %d ",x)
li $v0, 4
la $a0, $$1
syscall
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
#//intmain(intx){floaty=123.456;return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,16	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intx
#//floaty=123.456
lw  $s1, -12($fp)
ori $s1,$0,0x42f6e979
sw  $s1, -12($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
