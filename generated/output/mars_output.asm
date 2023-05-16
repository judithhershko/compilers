.data
$$1  :.asciiz "y is :  "
.text
.globl main
#//intf(intx){//this is a commentinty=90;intz=x;z=x+y*x+9;while(y>z+89*z){y=y-1;}if(x+y*z+90>x){x=x+90;}else{y=y-1;}printf("y is : %d ",y);}
f: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,20	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intx
#//this is a comment
#//inty=90
lw  $s1, -12($fp)
ori $s1,$0,90
sw  $s1, -12($fp)
#//intz=x
lw  $s2, -16($fp)
sw $s2, -8($fp)
#//z=x+y*x+9
ori $t0,$0,0x42b40000
lw  $s0, -8($fp)
mul $s2,$t0, $s0
sw $s2, -16($fp)
lw  $s0, -8($fp)
ori $t0,$0,0x42b40000
addu $s2,$s0, $t0
sw $s2, -16($fp)
ori $t0,$0,0x42b40000
lw  $s0, -8($fp)
mul $s2,$t0, $s0
sw $s2, -16($fp)
ori $t1,$0,0x42b40000
ori $t0,$0,0x41100000
addu $s2,$t1, $t0
sw $s2, -16($fp)
lw  $s0, -8($fp)
ori $t0,$0,0x42b40000
addu $s2,$s0, $t0
sw $s2, -16($fp)
ori $t0,$0,0x42b40000
lw  $s0, -8($fp)
mul $s2,$t0, $s0
sw $s2, -16($fp)
#//while(y>z+89*z){y=y-1;}
j $loop1
nop
$loop1:
ori $t0,$0,0x42b20000
lw  $s2, -16($fp)
mul $3,$t0, $s2
sw $3, -20($fp)
lw  $s2, -16($fp)
ori $t0,$0,0x42b20000
addu $3,$s2, $t0
sw $3, -20($fp)
ori $t0,$0,0x42b20000
lw  $s2, -16($fp)
mul $3,$t0, $s2
sw $3, -20($fp)
lw  $s1, -12($fp)
ori $t0,$0,0x42b20000
sgt $3,$s1, $t0
sw $3, -20($fp)
lw  $s2, -16($fp)
lw  $s1, -12($fp)
addu $3,$s2, $s1
sw $3, -20($fp)
ori $t0,$0,0x42b20000
lw  $s2, -16($fp)
mul $3,$t0, $s2
sw $3, -20($fp)
lbu $3, -20($fp)
andi  $3, $3, 1
beqz    $3, $loop3
nop 
j $loop2
nop
$loop2:
#//y=y-1
lw  $s1, -12($fp)
ori $t0,$0,0x3f800000
subu $s1,$s1, $t0
sw $s1, -12($fp)
j $loop1
nop
$loop3:
#//if(x+y*z+90>x){x=x+90;}
j $loop4
nop
$loop4:
lw  $s1, -12($fp)
lw  $s2, -16($fp)
mul $3,$s1, $s2
sw $3, -24($fp)
lw  $s0, -8($fp)
lw  $s1, -12($fp)
addu $3,$s0, $s1
sw $3, -24($fp)
lw  $s1, -12($fp)
lw  $s2, -16($fp)
mul $3,$s1, $s2
sw $3, -24($fp)
lw  $s1, -12($fp)
ori $t0,$0,0x42b40000
addu $3,$s1, $t0
sw $3, -24($fp)
lw  $s0, -8($fp)
lw  $s1, -12($fp)
addu $3,$s0, $s1
sw $3, -24($fp)
lw  $s1, -12($fp)
lw  $s2, -16($fp)
mul $3,$s1, $s2
sw $3, -24($fp)
lw  $s1, -12($fp)
lw  $s0, -8($fp)
sgt $3,$s1, $s0
sw $3, -24($fp)
lw  $s1, -12($fp)
ori $t0,$0,0x42b40000
addu $3,$s1, $t0
sw $3, -24($fp)
lw  $s0, -8($fp)
lw  $s1, -12($fp)
addu $3,$s0, $s1
sw $3, -24($fp)
lw  $s1, -12($fp)
lw  $s2, -16($fp)
mul $3,$s1, $s2
sw $3, -24($fp)
lbu $3, -24($fp)
andi  $3, $3, 1
beqz    $3, $loop6
nop 
j $loop5
nop
$loop5:
#//x=x+90
lw  $s0, -8($fp)
ori $t0,$0,0x42b40000
addu $s0,$s0, $t0
sw $s0, -8($fp)
j $loop7
$loop6:
#//y=y-1
lw  $s1, -12($fp)
ori $t0,$0,0x3f800000
subu $s1,$s1, $t0
sw $s1, -12($fp)
j $loop7
nop
$loop7:
#//printf("y is : %d ",y)
li $v0, 4
la $a0, $$1
syscall
lw	$s2, -24($fp)
lw	$s1, -20($fp)
lw	$s0, -16($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
#//intmain(intx){floaty=123.456;return0;}
main: 
 sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
move	$fp, $sp	# frame	pointer now points to the top of the stack
subu	$sp, $sp,16	# allocate bytes on the stack
sw	$ra, -4($fp)	# store the value of the return address
sw	$s3, -8($fp)
sw	$s4, -12($fp)
#//intx
#//floaty=123.456
lw  $s4, -12($fp)
ori $s4,$0,0x42f6e979
sw  $s4, -12($fp)
lw	$3, -12($fp)
lw	$s2, -8($fp)
lw	$s4, -4($fp)
lw	$s3, 0($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
