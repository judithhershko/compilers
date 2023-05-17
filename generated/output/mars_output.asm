.data
.text
.globl main
j main
#//intf(intx){x=!x;//this is a comment{intx=90;x=x+1;{x=x+2;}x=3;}//int y=(x*x+78+x*x-12);//printf("y is : %d ", x);returnx;}
f: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx
#//x=!x
lw  $s0, -8($fp)
nor $s0, $s0 ,$zero
sw $s0, -8($fp)
#//this is a comment
#//intx=90
lw  $s0, -8($fp)
ori $s0,$0,90
sw  $s0, -8($fp)
#//x=x+1
lw  $s0, -8($fp)
ori $s0,$0,91
sw  $s0, -8($fp)
#//x=x+2
lw  $s0, -8($fp)
ori $s0,$0,93
sw  $s0, -8($fp)
#//x=3
lw  $s0, -8($fp)
ori $s0,$0,3
sw  $s0, -8($fp)
#//int y=(x*x+78+x*x-12);
#//printf("y is : %d ", x);
lw $t0, -8($fp)
move $v0,$t0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){intz=2;scanf(" val is: %d and %d",z*z,z);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intz=2
lw  $s0, -8($fp)
ori $s0,$0,2
sw  $s0, -8($fp)
#//scanf(" val is: %d and %d",z*z,z)
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
