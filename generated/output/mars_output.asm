.data
.text
.globl main
j main
#//intf(intx){//x=!x;//this is a comment//int y=(x*x+78+x*x-12);//printf("y is : %d ", x);returnx;}
f: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,12	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
#//intx
#//x=!x;
#//this is a comment
#//int y=(x*x+78+x*x-12);
#//printf("y is : %d ", x);
lw $t0, -8($fp)
move $v0,$t0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){floaty=123.456;return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,12	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
#//floaty=123.456
lw  $s0, -8($fp)
ori $s0,$0,0x42f6e979
sw  $s0, -8($fp)
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
