.data
$$1  :.asciiz "y is :  "
$$2: .float 90.9
.text
.globl main
j main
#//intfff(intx){returnx;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx
lw $t0, -8($fp)
move $v0,$t0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){floatf=90.9;printf("y is : %f ",f);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//floatf=90.9
lw  $s0, -8($fp)
ori $s0,$0,0x42b5cccd
sw  $s0, -8($fp)
#//printf("y is : %f ",f)
li $v0, 4
la $a0, $$1
syscall
li $v0, 2
lwc1 $f0, $$2
mov.s $f12, $f0
syscall
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
