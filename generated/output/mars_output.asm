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
#//intmain(){intx[2];x[0]=3;inty=2;while(y<5){f(y);y=y+1;}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
#//intx[2]
#//x[0]=3
lw  $s0, -8($fp)
ori $s0,$0,3
sw  $s0, -8($fp)
#//inty=2
lw  $s3, -20($fp)
ori $s3,$0,2
sw  $s3, -20($fp)
#//while(y<5){f(y);y=y+1;}
j $loop1
nop
$loop1:
lw  $s3, -20($fp)
ori $t0,$0,5
slt $4,$s3, $t0
sw $4, -24($fp)
lbu $4, -24($fp)
andi  $4, $4, 1
beqz    $4, $loop3
nop 
j $loop2
nop
$loop2:
#//y=y+1
lw  $s3, -20($fp)
ori $t0,$0,1
addu $s3,$s3, $t0
sw $s3, -20($fp)
j $loop1
nop
$loop3:
li $v0, 0
lw $4, -24($fp)
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
