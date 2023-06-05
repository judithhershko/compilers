.data
$$1  :.asciiz  "Enter two numbers:"  
$$2  :.asciiz "  en  " 
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx;inty;printf("Enter two numbers:");scanf("%i%i",&x,&y);printf("%i en %i",x,y);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,16
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intx
lw  $s0, -8($fp)
ori $s0,$0,0
sw  $s0, -8($fp)
#//inty
lw  $s1, -12($fp)
ori $s1,$0,0
sw  $s1, -12($fp)
#//printf("Enter two numbers:")
li $v0, 4
la $a0, $$1
syscall
#//scanf("%i%i",&x,&y)
li $v0, 5
syscall
sw $s0, -8($fp)
move $s0, $v0
lw $s0, -8($fp)
li $v0, 5
syscall
sw $s1, -12($fp)
move $s1, $v0
lw $s1, -12($fp)
#//printf("%i en %i",x,y)
li $v0, 4
la $a0, $$2
syscall
li $v0, 1
move $a0, $s0
syscall
li $v0, 0
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
