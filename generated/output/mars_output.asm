.data
$$1  :.asciiz " val is:  "
.text
.globl main
j main
#//intf(intx){x=!x;//this is a comment{intx=90;x=x+1;{x=x+2;}}//int y=(x*x+78+x*x-12);//printf("y is : %d ", x);returnx;}
f: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,12	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
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
#//int y=(x*x+78+x*x-12);
#//printf("y is : %d ", x);
lw $t0, -8($fp)
move $v0,$t0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){intx=8;intz=1;while(z<x){z=z+1;printf(" val is: %d",z);}return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,16	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intx=8
lw  $s0, -8($fp)
ori $s0,$0,8
sw  $s0, -8($fp)
#//intz=1
lw  $s1, -12($fp)
ori $s1,$0,1
sw  $s1, -12($fp)
#//while(z<x){z=z+1;printf(" val is: %d",z);}
j $loop1
nop
$loop1:
lw  $s1, -12($fp)
lw  $s0, -8($fp)
slt $2,$s1, $s0
sw $2, -16($fp)
lbu $2, -16($fp)
andi  $2, $2, 1
beqz    $2, $loop3
nop 
j $loop2
nop
$loop2:
#//z=z+1
lw  $s1, -12($fp)
ori $t0,$0,1
addu $s1,$s1, $t0
sw $s1, -12($fp)
#//printf(" val is: %d",z)
li $v0, 4
la $a0, $$1
syscall
j $loop1
nop
$loop3:
li $v0, 0
lw $2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
