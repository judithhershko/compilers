.data
$$1  :.asciiz  "val of a is:  "
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){for(inta=0;a<10;a++){printf("val of a is: %i\n",a);}return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//for(inta=0;a<10;a++){printf("val of a is: %i\n",a);}
#//inta=0
lw  $s0, -8($fp)
ori $s0,$0,0
sw  $s0, -8($fp)
j $loop1
nop
$loop1:
lw  $s0, -8($fp)
ori $t0,$0,10
slt $1,$s0, $t0
sw $1, -12($fp)
lbu $1, -12($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop
j $loop2
nop
$loop2:
#//printf("val of a is: %i\n",a)
li $v0, 4
la $a0, $$1
syscall
li $v0, 1
move $a0, $s0
syscall
lw  $s0, -8($fp)
ori $t0,$0,1
addu $s0,$s0, $t0
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
