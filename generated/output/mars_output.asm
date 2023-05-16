.data
$$1  :.asciiz "y is :  "
.text
.globl main
#//intf(intx){//this is a commentinty=90;intz=x;z=x+y*x+9;printf("y is : %d ",y);}
f: 
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
#//intz=x
lw  $s2, -16($fp)
sw $s2, -8($fp)
#//z=x+y*x+9
ori $t0,$0,0x42b40000
lw  $s0, -8($fp)
mul $s0,$t0, $s0
sw $s0, -8($fp)
lw  $s0, -8($fp)
ori $t1,$0,0x42b40000
addu $s0,$s0, $t1
sw $s0, -8($fp)
ori $t2,$0,0x42b40000
lw  $s0, -8($fp)
mul $s0,$t2, $s0
sw $s0, -8($fp)
ori $t4,$0,0x42b40000
ori $t3,$0,0x41100000
addu $s2,$t4, $t3
sw $s2, -16($fp)
lw  $s0, -8($fp)
ori $t5,$0,0x42b40000
addu $s0,$s0, $t5
sw $s0, -8($fp)
ori $t6,$0,0x42b40000
lw  $s0, -8($fp)
mul $s0,$t6, $s0
sw $s0, -8($fp)
#//printf("y is : %d ",y)
li $v0, 4
la $a0, $$1
syscall
lw	$t3, -16($fp)
lw	$t6, -12($fp)
lw	$s2, -8($fp)
lw	$s1, -4($fp)
lw	$s0, 0($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
#//intmain(intx){floaty=123.456;return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,16	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s3, -8($fp)
sw	$s4, -12($fp)
#//intx
#//floaty=123.456
lw  $s4, -12($fp)
ori $s4,$0,0x42f6e979
sw  $s4, -12($fp)
lw	$t3, -12($fp)
lw	$t6, -8($fp)
lw	$s2, -4($fp)
lw	$s4, 0($fp)
lw	$s3, 4($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
