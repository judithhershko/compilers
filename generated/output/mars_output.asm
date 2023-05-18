.data
.text
.globl main
j main
#//intmain(){intx=5;while(x>5){x=x+5;}inty=(x*x+78+x*x-12);return1;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,16
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//while(x>5){x=x+5;}
j $loop1
nop
$loop1:
lw  $s0, -8($fp)
ori $t0,$0,5
sgt $2,$s0, $t0
sw $2, -16($fp)
lbu $2, -16($fp)
andi  $2, $2, 1
beqz    $2, $loop3
nop 
j $loop2
nop
$loop2:
#//x=x+5
lw  $s0, -8($fp)
ori $t0,$0,5
addu $s0,$s0, $t0
sw $s0, -8($fp)
j $loop1
nop
$loop3:
#//inty=(x*x+78+x*x-12)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -12($fp)
lw  $s0, -8($fp)
ori $t0,$0,78
addu $s1,$s0, $t0
sw $s1, -12($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -12($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -12($fp)
lw  $s0, -8($fp)
ori $t0,$0,12
subu $s1,$s0, $t0
sw $s1, -12($fp)
lw  $s0, -8($fp)
ori $t0,$0,78
addu $s1,$s0, $t0
sw $s1, -12($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -12($fp)
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s1,$s0, $s0
sw $s1, -12($fp)
li $v0, 1
lw $2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
