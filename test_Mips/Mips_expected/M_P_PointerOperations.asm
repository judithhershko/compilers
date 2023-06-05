.data
$$1  : .byte 'a'
$$2  : .byte 'b'
$$3  : .byte 'b'
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intmain(){charx='a';char*chr_ptr=&x;*chr_ptr='b';charanother_char=*chr_ptr;inty=-60;int*some_pointer=&y;*some_pointer=53;int**another_pointer=&some_pointer;int***triple_pointer=&another_pointer;intz=***triple_pointer;return0;}
main:
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,40
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
sw	$s3, -20($fp)
sw	$s4, -24($fp)
sw	$s5, -28($fp)
sw	$s6, -32($fp)
sw $s0, -8($fp)
sw $s1, -12($fp)
sw $s2, -16($fp)
sw $s3, -20($fp)
sw $s4, -24($fp)
sw $s5, -28($fp)
sw $s6, -32($fp)
sw	$s0, -36($fp)
#//charx='a'
sw $s1, -36($fp)
lb $s1 , $$1
sb $s1, -36($fp)
#//char*chr_ptr=&x
sw $s2, -36($fp)
move $s2,$s1
#//*chr_ptr='b'
lw $s2, -36($fp)
lb $s2 , $$2
sb $s2, -36($fp)
sw $s2, -36($fp)
#//charanother_char=*chr_ptr
sw $s3, -36($fp)
lb $s3 , $$3
sb $s3, -36($fp)
#//inty=-60
sw $s4, -36($fp)
sw $s5, -36($fp)
lw $s5, -36($fp)
move $s4, $s5
#//int*some_pointer=&y
sw $s6, -36($fp)
move $s6,$s4
#//*some_pointer=53
lw $s6, -36($fp)
lw  $s6, -36($fp)
ori $s6,$0,53
sw  $s6, -36($fp)
sw $s6, -36($fp)
#//int**another_pointer=&some_pointer
sw $s0, -36($fp)
sw $s1, -36($fp)
sw $s2, -36($fp)
sw $s3, -36($fp)
sw $s4, -36($fp)
sw $s5, -36($fp)
sw $s6, -36($fp)
sw $s0, -36($fp)
sw $s1, -36($fp)
move $s0,$s1
#//int***triple_pointer=&another_pointer
sw $s2, -36($fp)
move $s2,$s0
#//intz=***triple_pointer
sw $s3, -36($fp)
lw  $s3, -36($fp)
ori $s3,$0,53
sw  $s3, -36($fp)
li $v0, 0
lw $s6, -36($fp)
lw $s5, -36($fp)
lw $s4, -36($fp)
lw $s3, -36($fp)
lw $s2, -36($fp)
lw $s1, -36($fp)
lw $s0, -36($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
