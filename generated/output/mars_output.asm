.data
xglobal: .word 90
fgloabal: .float 90.9
$$3  :.asciiz  "this is printing something"  
$$4: .float 1654.0
$$5: .float 0.0
$$6  :.asciiz  "this is printing something"  
$$7: .float 9.0
$$8: .space 12
$$9: .float 45.0
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//intxglobal=90
#//floatfgloabal=90.9
#//intf(inta){if(a>1){a=1;}printf("this is printing something");inty=-60;int*some_pointer=&y;*some_pointer=53;returna;}
f: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,20
sw	$ra, -4($fp)
sw	$s0, -8($fp)
sw	$s1, -12($fp)
sw	$s2, -16($fp)
#//inta
#//if(a>1){a=1;}

j $loop1
nop
$loop1:
ori $t1,$0,1
sgt $3,$t1, $t1
sw $3, -20($fp)
lbu $3, -20($fp)
andi  $3, $3, 1
beqz    $3, $loop3
nop 
j $loop2
nop
$loop2:
#//a=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
j $loop3
$loop3:
#//printf("this is printing something")
li $v0, 4
la $a0, $$3
syscall
#//inty=-60
move $s1, $s3
#//int*some_pointer=&y
move $s2,$s1
#//*some_pointer=53
lw $s2, -12($fp)
lw  $s2, -12($fp)
ori $s2,$0,53
sw  $s2, -12($fp)
sw $s2, -12($fp)
li $v0, 1
lw $3, -20($fp)
lw $s2, -12($fp)
lw $s1, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//voida_void_func(){floata=1654.0000;floatd=0.00000;intz=90;z=z+z*z+89;intx=90;0||(0*3);1&&(!(1+0));}
a_void_func: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
s.s   $f0, -8($fp)
s.s   $f1, -12($fp)
sw	$s0, -16($fp)
sw	$s1, -20($fp)
#//floata=1654.0000
lwc1 $f2, $$4
#//floatd=0.00000
lwc1 $f3, $$5
#//intz=90
lw  $s0, -16($fp)
ori $s0,$0,90
sw  $s0, -16($fp)
#//z=z+z*z+89
lw  $s0, -16($fp)
ori $s0,$0,8279
sw  $s0, -16($fp)
#//intx=90
lw  $s1, -20($fp)
ori $s1,$0,90
sw  $s1, -20($fp)
lw $s1, -20($fp)
lw $s0, -16($fp)
l.s $f1, -12($fp)
l.s $f0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
#//intmain(){printf("this is printing something");inti=5;floatfi=9.0;intarray[3];//this is a commentfloatz=i*fi;int*a=&i;if(i>1){i=1;}return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,40
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f4, -12($fp)
sw	$s1, -16($fp)
sw	$s2, -20($fp)
sw	$s3, -24($fp)
sw	$s4, -28($fp)
s.s   $f5, -32($fp)
sw	$s5, -36($fp)
#//printf("this is printing something")
li $v0, 4
la $a0, $$6
syscall
#//inti=5
lw  $s0, -8($fp)
ori $s0,$0,5
sw  $s0, -8($fp)
#//floatfi=9.0
lwc1 $f6, $$7
#//intarray[3]
addi $t0, $zero, 0
#//this is a comment
#//floatz=i*fi
lwc1 $f7, $$9
#//int*a=&i
move $s5,$s0
#//if(i>1){i=1;}

j $loop4
nop
$loop4:
ori $t1,$0,1
sgt $8,$t1, $t1
sw $8, -40($fp)
lbu $8, -40($fp)
andi  $8, $8, 1
beqz    $8, $loop6
nop 
j $loop5
nop
$loop5:
#//i=1
lw  $s0, -8($fp)
ori $s0,$0,1
sw  $s0, -8($fp)
j $loop6
$loop6:
li $v0, 0
lw $8, -40($fp)
lw $s5, -8($fp)
l.s $f5, -32($fp)
lw $s4, -28($fp)
lw $s3, -24($fp)
lw $s2, -20($fp)
lw $s1, -16($fp)
l.s $f4, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
