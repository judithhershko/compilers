.data
$$1  :.asciiz  "Hello World!\n"
$$2  :.asciiz "   "
$$3  :.asciiz  "x is  "
$$4  :.asciiz "   "
$$5  :.asciiz "   "
$$6: .float 0.5
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=5;printf("Hello World!\n");printf("%s %s!\n","Hello","World");printf("x is %i",x*x);printf("%d %f %c",10,0.5,"a");return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//printf("Hello World!\n")
li $v0, 4
la $a0, $$1
syscall
#//printf("%s %s!\n","Hello","World")
li $v0, 4
la $a0, $$2
syscall
#//printf("x is %i",x*x)
li $v0, 4
la $a0, $$3
syscall
li $v0, 1
li $t0, 25
move $a0, $t0
syscall
#//printf("%d %f %c",10,0.5,"a")
li $v0, 4
la $a0, $$4
syscall
li $v0, 1
li $t1, 10
move $a0, $t1
syscall
li $v0, 4
la $a0, $$5
syscall
li $v0, 2
lwc1 $f0, $$6
mov.s $f12, $f0
syscall
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
