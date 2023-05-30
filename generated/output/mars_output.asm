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
#//intf(inta){if(a>1){a=1;}returna;}
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
li $v0, 1
lw $1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){inti=5;int*a=&i;while(*a>0){intx=*a;f(*a);}return0;}
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
#//int*a=&i
move $s1,$s0
#//while(*a>0){intx=*a;f(*a);}
j $loop4
nop
$loop4:
lw  $s1, -8($fp)
ori $t0,$0,0
sgt $2,$s1, $t0
sw $2, -16($fp)
lbu $2, -16($fp)
andi  $2, $2, 1
beqz    $2, $loop6
nop 
j $loop5
nop
$loop5:
#//intx=*a
lw $s1, -8($fp)
move $s2, $s1
j $loop4
nop
$loop6:
li $v0, 0
lw $2, -16($fp)
lw $s1, -8($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
