.data
.text
.globl main
j main
#//intmain(){intz=1;while(z>0){z=z-1;}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intz=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
#//while(z>0){z=z-1;}
j $loop1
nop
$loop1:
lw  $s0, -8($fp)
ori $t0,$0,0
sgt $1,$s0, $t0
sw $1, -12($fp)
lbu $1, -12($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop 
j $loop2
nop
$loop2:
#//z=z-1
lw  $s0, -8($fp)
ori $t0,$0,1
subu $s0,$s0, $t0
sw $s0, -8($fp)
j $loop1
nop
$loop3:
li $v0, 0
lw $1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
