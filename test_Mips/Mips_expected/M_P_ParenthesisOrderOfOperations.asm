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
#//intmain(){12+(98721+36265/456)*(0+1687);12+(98721*0+36265/(456))*(0);(0&&(1&&1)||(1&&1));1&&(!(1+0));((12>55)&&((5*4)==(3*(2+1))))||(1<(5*4));return0;}
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
