.data
$$1: .space 12
$$2: .space 8
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intz=1;intx[3];x[z-1]=5;x[z]=6;x[1+z]=7;inty=x[z-1];intw=x[z];intv=x[1+z];intu[2]={1,2};return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,52
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
sw	$s6, -32($fp)
sw $s0, -8($fp)
sw $s1, -12($fp)
sw $s2, -16($fp)
sw $s3, -20($fp)
sw $s4, -24($fp)
sw $s5, -28($fp)
sw $s6, -32($fp)
sw	$s0, -36($fp)
sw	$s1, -40($fp)
sw	$s2, -44($fp)
sw	$s3, -48($fp)
#//intz=1
sw $s4, -48($fp)
lw  $s4, -48($fp)
ori $s4,$0,1
sw  $s4, -48($fp)
#//intx[3]
addi $t0, $zero, 0
#//x[z-1]=5
addi $t0,$zero, -4
addi $t1, $zero, 5
sw $t1, $$1($t0)
addi $t0,$zero, -4
addi $t1, $zero, 5
sw $t1, $$1($t0)
sw $s5, -52($fp)
#//x[z]=6
addi $t0,$zero, 0
addi $t1, $zero, 6
sw $t1, $$1($t0)
addi $t0,$zero, 0
addi $t1, $zero, 6
sw $t1, $$1($t0)
#//x[1+z]=7
addi $t0,$zero, 4
addi $t1, $zero, 7
sw $t1, $$1($t0)
addi $t0,$zero, 4
addi $t1, $zero, 7
sw $t1, $$1($t0)
#//inty=x[z-1]
sw $s6, -56($fp)
#//intw=x[z]
sw $s0, -36($fp)
sw $s1, -40($fp)
sw $s2, -44($fp)
sw $s3, -48($fp)
sw $s4, -48($fp)
sw $s5, -52($fp)
sw $s6, -56($fp)
sw $s0, -60($fp)
#//intv=x[1+z]
sw $s1, -64($fp)
#//intu[2]={1,2}
addi $t0, $zero, 0
addi $t1, $zero, 1
 sw $t1, $$2($t0)
addi $t0, $t0, 4
addi $t1, $zero, 2
 sw $t1, $$2($t0)
addi $t0, $t0, 4
li $v0, 0
lw $s6, -56($fp)
lw $s5, -52($fp)
lw $s4, -48($fp)
lw $s3, -48($fp)
lw $s2, -44($fp)
lw $s1, -64($fp)
lw $s0, -60($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
