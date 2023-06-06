.data
$$1  :.asciiz  "Something went wrong"
$$2  :.asciiz  "Hello world!\n"
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=5;if(x<5){printf("Something went wrong");// Should not print}else{printf("Hello world!\n");// Should print}return0;}
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
#//if(x<5){printf("Something went wrong");// Should not print}

j $loop1
nop
$loop1:
ori $t1,$0,5
slt $1,$t1, $t1
sw $1, -12($fp)
lbu $1, -12($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop
j $loop2
nop
$loop2:
#//printf("Something went wrong")
li $v0, 4
la $a0, $$1
syscall
#// Should not print
j $loop3
j $loop4
$loop3:
#//printf("Hello world!\n")
li $v0, 4
la $a0, $$2
syscall
#// Should print
j $loop4
nop
$loop4:
li $v0, 0
lw $1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
