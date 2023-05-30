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
#//intmain(){inti=0;while(i<10){printf("%d\n",i);if(i==5){break;}else{i++;continue;}i=10;}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inti=0
lw  $s0, -8($fp)
ori $s0,$0,0
sw  $s0, -8($fp)
#//while(i<10){printf("%d\n",i);if(i==5){break;}else{i++;continue;}i=10;}
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
#//printf("%d\n",i)
#//if(i==5){break;}
j $loop4
nop
$loop4:
lw  $s0, -8($fp)
ori $t0,$0,5
seq $1,$s0, $t0
sw $1, -16($fp)
lbu $1, -16($fp)
andi  $1, $1, 1
beqz    $1, $loop6
nop 
j $loop5
nop
$loop5:
j loop6
j $loop7
$loop6:
j loop7
nopj $loop7
nop
$loop7:
#//i=10
lw  $s0, -8($fp)
ori $s0,$0,10
sw  $s0, -8($fp)
j $loop1
nop
$loop3:
li $v0, 0
lw $1, -16($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
