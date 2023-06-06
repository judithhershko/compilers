.data
$$1: .float 90.0
$$2: .float 8190.0
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=0;int*xp=&x;*xp=42;inta=x+*xp;floatf=90.0;float*pf=&f;floatff=*pf+f**pf;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
s.s   $f0, -20($fp)
s.s   $f1, -24($fp)
s.s   $f2, -28($fp)
#//intx=0
lw  $s0, -8($fp)
ori $s0,$0,0
sw  $s0, -8($fp)
#//int*xp=&x
move $s1,$s0
#//*xp=42
lw $s1, -8($fp)
lw  $s1, -8($fp)
ori $s1,$0,42
sw  $s1, -8($fp)
sw $s1, -8($fp)
#//inta=x+*xp
lw  $s2, -16($fp)
ori $s2,$0,84
sw  $s2, -16($fp)
#//floatf=90.0
lwc1 $f3, $$1
#//float*pf=&f
mov.s $f1,$f0
#//floatff=*pf+f**pf
lwc1 $f4, $$2
li $v0, 0
l.s $f2, -28($fp)
l.s $f1, -20($fp)
l.s $f0, -20($fp)
lw $s2, -16($fp)
lw $s1, -8($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
