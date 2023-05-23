.data
$$1: .float 90.0
$$2: .float 8271.0
$$3  :.asciiz  "y is :  " 
$$4  :.asciiz "  en int is :  " 
.text
.globl main
j main
#//intfff(intx){floatz=90.0;floatf=90.9*z+z;returnx;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx
#//floatz=90.0
lwc1 $f2, $$1
#//floatf=90.9*z+z
lwc1 $f3, $$2
lw $t0, -8($fp)
move $v0,$t0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(intx,floatz){intf=fff(1);x=90;printf("y is : %i en int is : %i ",f,x*x+89);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -16($fp)
#//intx
#//floatz
#//intf=fff(1)
ori $a0, $zero, 1
jal fff
move $s1, $v0
sw $s1, -16($fp)
#//x=90
lw  $s0, -8($fp)
ori $s0,$0,90
sw  $s0, -8($fp)
#//printf("y is : %i en int is : %i ",f,x*x+89)
li $v0, 4
la $a0, $$3
syscall
li $v0, 1
move $a0, $s1
syscall
li $v0, 4
la $a0, $$4
syscall
li $v0, 1
ori $t0, 8189
move $a0, $t0
syscall
li $v0, 0
lw $s1, -16($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
