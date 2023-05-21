.data
$$1  : .byte 'y' 
$$2  :.asciiz " val is:  "
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
#//intmain(){chary='a';intx=90;intz=33;while(z<x){intza;z=z+1;printf(" val is: %d",z);}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//chary='a'
lw  $s0, -8($fp)
lb $s0 , $$1
sb $s0, -8($fp)
#//intx=90
lw  $s1, -12($fp)
ori $s1,$0,90
sw  $s1, -12($fp)
#//intz=33
lw  $s2, -16($fp)
ori $s2,$0,33
sw  $s2, -16($fp)
#//while(z<x){intza;z=z+1;printf(" val is: %d",z);}
j $loop1
nop
$loop1:
lw  $s2, -16($fp)
lw  $s1, -12($fp)
slt $3,$s2, $s1
sw $3, -20($fp)
lbu $3, -20($fp)
andi  $3, $3, 1
beqz    $3, $loop3
nop 
j $loop2
nop
$loop2:
#//intza
sw $s3, -20($fp)
lw  $s3, -20($fp)
ori $s3,$0,0
sw  $s3, -20($fp)
#//z=z+1
lw  $s2, -16($fp)
ori $t0,$0,1
addu $s2,$s2, $t0
sw $s2, -16($fp)
#//printf(" val is: %d",z)
li $v0, 4
la $a0, $$2
syscall
j $loop1
nop
$loop3:
li $v0, 0
lw $s3, -20($fp)
lw $3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
