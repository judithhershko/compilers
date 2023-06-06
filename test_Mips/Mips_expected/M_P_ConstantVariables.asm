.data
$$1: .float 0.5487
$$2: .float 0.16519803630299995
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){constintx=5;constfloatf=0.5487;constinty=x*35*-5;constfloatz=f*f*f;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f0, -12($fp)
sw	$s1, -16($fp)
s.s   $f1, -20($fp)
#//constintx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//constfloatf=0.5487
lwc1 $f2, $$1
#//constinty=x*35*-5
move $s1, $s2
sw $s1, -16($fp)
#//constfloatz=f*f*f
lwc1 $f3, $$2
li $v0, 0
l.s $f1, -20($fp)
lw $s1, -16($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
