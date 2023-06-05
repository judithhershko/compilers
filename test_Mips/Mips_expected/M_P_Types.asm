.data
$$1  : .byte 'b'
$$2  : .byte '.'
$$3: .float 1654.0
$$4: .float 0.0
$$5: .float -565.21547
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){charb='b';chardot='.';floata=1654.0000;floatd=0000.00000;d=-565.21547;intx=5;intz=x+3;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
s.s   $f0, -16($fp)
s.s   $f1, -20($fp)
sw	$s2, -24($fp)
sw	$s3, -28($fp)
#//charb='b'
lb $s0 , $$1
sb $s0, -8($fp)
#//chardot='.'
lb $s1 , $$2
sb $s1, -12($fp)
#//floata=1654.0000
lwc1 $f2, $$3
#//floatd=0000.00000
lwc1 $f3, $$4
#//d=-565.21547
lwc1 $f4, $$5
#//intx=5
lw  $s2, -24($fp)
ori $s2,$0,5
sw  $s2, -24($fp)
#//intz=x+3
lw  $s3, -28($fp)
ori $s3,$0,8
sw  $s3, -28($fp)
li $v0, 0
lw $s3, -28($fp)
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
