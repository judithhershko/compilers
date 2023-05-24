.data
$$1: .float 90.9
$$2  : .byte 'z' 
.text
.globl main
j main
#//intmain(){floatf=90.9;intx=88;charz='a';inty=x+x;return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
s.s   $f0, -8($fp)
sw	$s0, -12($fp)
sw	$s1, -16($fp)
sw	$s2, -20($fp)
#//floatf=90.9
lwc1 $f1, $$1
#//intx=88
lw  $s0, -12($fp)
ori $s0,$0,88
sw  $s0, -12($fp)
#//charz='a'
lb $s1 , $$2
sb $s1, -16($fp)
#//inty=x+x
lw  $s2, -20($fp)
ori $s2,$0,176
sw  $s2, -20($fp)
li $v0, 0
lw $s2, -20($fp)
lw $s1, -16($fp)
lw $s0, -12($fp)
l.s $f0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
