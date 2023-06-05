.data
x: .word 5
y: .word 6
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intx=5
#//inty=6
#//intmain(){intz=x+y;intw=x*y+z;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,16
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
#//intz=x+y
lw  $s0, -8($fp)
ori $s0,$0,11
sw  $s0, -8($fp)
#//intw=x*y+z
lw  $s1, -12($fp)
ori $s1,$0,41
sw  $s1, -12($fp)
li $v0, 0
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
