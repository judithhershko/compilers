.data
$$1  : .byte 'b' 
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intf(inta);
#//intf(inta){a=a*a;returna;}
f: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//inta
#//a=a*a
lw  $s0, -8($fp)
lw  $s0, -8($fp)
mul $s0,$s0, $s0
sw $s0, -8($fp)
move $v0, $s0
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//voidf2(charb){printf("%c",b);}
f2: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,12
sw	$ra, -4($fp)
sw	$s0, -8($fp)
#//charb
#//printf("%c",b)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
#//intmain(){intx=5;inty=f(x);charb='a';f2(b);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//inty=f(x)
lw $s0, -8($fp)
jal f
move $s1, $v0
lw $s0, -8($fp)
#//charb='a'
lb $s2 , $$1
sb $s2, -16($fp)
li $v0, 0
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
