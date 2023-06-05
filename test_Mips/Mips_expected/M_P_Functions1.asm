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
#//intf(inta){if(a<2){returnf(a);}else{returnf(a-1)+f(a-2);}}
f:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inta
#//if(a<2){returnf(a);}

j $loop1
nop
$loop1:
lw  $s0, -8($fp)
ori $t0,$0,2
slt $1,$s0, $t0
sw $1, -12($fp)
lbu $1, -12($fp)
andi  $1, $1, 1
beqz    $1, $loop3
nop
j $loop2
nop
$loop2:
j $loop3
j $loop4
$loop3:
j $loop4
nop
$loop4:
jal f
move $t0, $v0
jal f
move $t0, $v0
addu $s1,$t0, $t0
move $v0, $s1
lw $1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){inti=5;inta=0;while(a<i){f(a);}return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,16
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//inti=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//inta=0
lw  $s1, -12($fp)
ori $s1,$0,0
sw  $s1, -12($fp)
#//while(a<i){f(a);}
j $loop5
nop
$loop5:
lw  $s1, -12($fp)
lw  $s0, -8($fp)
slt $2,$s1, $s0
sw $2, -16($fp)
lbu $2, -16($fp)
andi  $2, $2, 1
beqz    $2, $loop7
nop
j $loop6
nop
$loop6:
j $loop5
nop
$loop7:
li $v0, 0
lw $2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
