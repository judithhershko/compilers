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
#//intmain(){33+69789*(69421/51213+(2231-654));654*(15486-(15000+486));12+(98721+36265/456)*(0+1687);12+(98721*0+36265/(456))*(0);return0;}
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
