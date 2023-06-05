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
#//intmain(){1&&(1||0);(0&&(1&&1)||(1&&1));0||(0*3);1&&(!(1+0));return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,8
sw	$ra, -4($fp)
li $v0, 0
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
