.data
$$1: .float 0.986312
$$2: .float 34.548296
$$3: .float 35.534608
$$4  : .byte 'a'
$$5  : .byte 'b'
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){intx=5;intz=x+3;x=z*z*z*(x+x);floatf=0.986312;floatf2=f*33.0+2.0;f2=f2+f;charc='a';c='b';return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,28
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
s.s   $f0, -16($fp)
s.s   $f1, -20($fp)
sw	$s2, -24($fp)
#//intx=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//intz=x+3
lw  $s1, -12($fp)
ori $s1,$0,8
sw  $s1, -12($fp)
#//x=z*z*z*(x+x)
lw  $s0, -8($fp)
ori $s0,$0,5120
sw  $s0, -8($fp)
#//floatf=0.986312
lwc1 $f2, $$1
#//floatf2=f*33.0+2.0
lwc1 $f3, $$2
#//f2=f2+f
lwc1 $f4, $$3
#//charc='a'
lb $s2 , $$4
sb $s2, -24($fp)
#//c='b'
lb $s2 , $$5
sb $s2, -24($fp)
li $v0, 0
lw $s2, -24($fp)
l.s $f1, -20($fp)
l.s $f0, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
