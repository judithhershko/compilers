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
#//intprint(intn){printf("%i",n);return0;}
print:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//intn
#//printf("%i",n)
li $v0, 1
move $a0, $s0
syscall
li $v0, 0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(){intn=5;intcounter=0;inti=1;intip=1;intpp=1;inta=0;printf("%i",i);printf("%i",i);while(counter<n){i=ip+pp;pp=ip;ip=i;printf("%i",i);counter=counter+1;}return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
#//intn=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//intcounter=0
lw  $s1, -12($fp)
ori $s1,$0,0
sw  $s1, -12($fp)
#//inti=1
lw  $s2, -16($fp)
ori $s2,$0,1
sw  $s2, -16($fp)
#//intip=1
lw  $s3, -20($fp)
ori $s3,$0,1
sw  $s3, -20($fp)
#//intpp=1
lw  $s4, -24($fp)
ori $s4,$0,1
sw  $s4, -24($fp)
#//inta=0
lw  $s5, -28($fp)
ori $s5,$0,0
sw  $s5, -28($fp)
#//printf("%i",i)
li $v0, 1
li $t0, 1
move $a0, $t0
syscall
#//printf("%i",i)
li $v0, 1
li $t0, 1
move $a0, $t0
syscall
#//while(counter<n){i=ip+pp;pp=ip;ip=i;printf("%i",i);counter=counter+1;}
j $loop1
nop
$loop1:
lw  $s1, -12($fp)
lw  $s0, -8($fp)
slt $6,$s1, $s0
sw $6, -32($fp)
lbu $6, -32($fp)
andi  $6, $6, 1
beqz    $6, $loop3
nop
j $loop2
nop
$loop2:
#//i=ip+pp
lw  $s3, -20($fp)
lw  $s4, -24($fp)
addu $s2,$s3, $s4
sw $s2, -16($fp)
#//pp=ip
lw $s3, -20($fp)
move $s4, $s3
sw $s4, -24($fp)
#//ip=i
lw $s2, -16($fp)
move $s3, $s2
sw $s3, -20($fp)
#//printf("%i",i)
li $v0, 1
move $a0, $s2
syscall
#//counter=counter+1
lw  $s1, -12($fp)
ori $t0,$0,1
addu $s1,$s1, $t0
sw $s1, -12($fp)
j $loop1
nop
$loop3:
li $v0, 0
lw $6, -32($fp)
lw $s5, -28($fp)
lw $s4, -24($fp)
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
