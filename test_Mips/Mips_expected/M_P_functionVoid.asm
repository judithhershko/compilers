.data
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//voidf(inta){if(a>1){a=1;}}
f:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inta
#//if(a>1){a=1;}

j $loop1
nop
$loop1:
ori $t1,$0,1
sgt $1,$t1, $t1
sw $1, -12($fp)
lbu $1, -12($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop
j $loop2
nop
$loop2:
#//a=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
j $loop3
$loop3:
lw $1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
#//intmain(){inti=5;f(i);return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inti=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
