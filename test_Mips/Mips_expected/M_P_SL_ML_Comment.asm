.data
$$1  : .byte 'b'
$$2  : .byte 'a'
$$3: .float 33.1
$$4: .float 33.99895
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){/**Thisisacomment**/intline_of_code=5;/***AnotherComment*****//******/intf=45;charc='b';intx=5;// line 1chard='a';floate=33.1;// another line/////// some documentation/////////////////////////////////////// abcdef 123 //////////floatfinal_line=33.99895;return0;};
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,36
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
s.s   $f0, -28($fp)
s.s   $f1, -32($fp)
#/**Thisisacomment**/#//intline_of_code=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#/***AnotherComment*****//******/#//intf=45
lw  $s1, -12($fp)
ori $s1,$0,45
sw  $s1, -12($fp)
#//charc='b'
lb $s2 , $$1
sb $s2, -16($fp)
#//intx=5
lw  $s3, -20($fp)
ori $s3,$0,5
sw  $s3, -20($fp)
#// line 1
#//chard='a'
lb $s4 , $$2
sb $s4, -24($fp)
#//floate=33.1
lwc1 $f2, $$3
#// another line
#/////// some documentation
#/////////////////////////////////////
#// abcdef 123 //////////
#//floatfinal_line=33.99895
lwc1 $f3, $$4
li $v0, 0
l.s $f1, -32($fp)
l.s $f0, -28($fp)
lw $s4, -24($fp)
lw $s3, -20($fp)
lw $s2, -16($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
