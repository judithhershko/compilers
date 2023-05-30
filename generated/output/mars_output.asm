.data
$$1: .float 90.9
$$2: .float 90.9
$$3: .float 90.9
$$4: .float 100.1
$$5: .float 2.2
$$6: .float 90.9
$$7: .float 90.9
$$8: .float 90.9
.text
.globl main
j main
false:
  li $1, 0
  jr $ra
true:
  li $1, 1
  jr $ra
#//floatfff(intx,floatfx){float*px=&fx;float**ppx=&px;floatz=*px;floatf=90.9*z+z;return100.1;}
fff: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,32
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f0, -12($fp)
s.s   $f1, -16($fp)
s.s   $f2, -20($fp)
s.s   $f3, -24($fp)
s.s   $f4, -28($fp)
#//intx
#//floatfx
#//float*px=&fx
mov.s $f1,$f0
#//float**ppx=&px
mov.s $f2,$f1
#//floatz=*px
l.s $f1, -12($fp)
mov.s $f3, $f1
#//floatf=90.9*z+z
lwc1 $f5, $$1
mul.s $f4,$f5, $f3
s.s $f4, -28($fp)
lwc1 $f6, $$2
add.s $f4,$f6, $f3
s.s $f4, -28($fp)
lwc1 $f7, $$3
mul.s $f4,$f7, $f3
s.s $f4, -28($fp)
lwc1 $f0, $$4
l.s $f4, -28($fp)
l.s $f3, -24($fp)
l.s $f2, -12($fp)
l.s $f1, -12($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
jr	$ra
#//intmain(intx,floatfx,intxi){inty[3];//scanf("%d%d", &x, &y);scanf("%d%d",x,y);floatf=fff(1,2.2);float*px=&f;*px=fx;floatz=*px;floatff=90.9*(z)+z;while(f<ff){x=x+1;}//printf("y is : %d en int is : %i ",*px,x*x+89);//printf("y is : %d en int is : %i ",f,x*x+89);return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,52
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f8, -12($fp)
sw	$s1, -16($fp)
sw	$s2, -20($fp)
sw	$s3, -24($fp)
sw	$s4, -28($fp)
sw	$s5, -32($fp)
s.s   $f9, -36($fp)
s.s   $f10, -40($fp)
s.s   $f11, -44($fp)
s.s   $f12, -48($fp)
#//intx
#//floatfx
#//intxi
#//inty[3]
#//scanf("%d%d", &x, &y);
#//scanf("%d%d",x,y)
li $v0, 5
syscall
sw $s0, -8($fp)
move $s0, $v0
lw $s0, -8($fp)
li $v0, 5
syscall
sw $s6, -48($fp)
sw $s6, -48($fp)
move $s6, $v0
lw $s6, -48($fp)
#//floatf=fff(1,2.2)
ori $s0, $zero, 1
lw $t0, $$5
mtc1 $t0, $f0
cvt.s.w $f0, $f0
jal fff
mov.s $f9, $f0
lw $s0, -8($fp)
l.s $f0, -12($fp)
#//float*px=&f
mov.s $f10,$f9
#//*px=fx
l.s $f10, -36($fp)
l.s $f8, -12($fp)
mov.s $f10, $f8
s.s $f10, -36($fp)
#//floatz=*px
l.s $f10, -36($fp)
mov.s $f11, $f10
#//floatff=90.9*(z)+z
lwc1 $f13, $$6
mul.s $f12,$f13, $f11
s.s $f12, -48($fp)
lwc1 $f14, $$7
add.s $f12,$f14, $f11
s.s $f12, -48($fp)
lwc1 $f15, $$8
mul.s $f12,$f15, $f11
s.s $f12, -48($fp)
#//while(f<ff){x=x+1;}
j $loop1
nop
$loop1:
c.lt.s $f9, $f12
bc1f false
bc1t true
lbu $16, -52($fp)
andi  $16, $16, 1
beqz    $16, $loop3
nop 
j $loop2
nop
$loop2:
#//x=x+1
lw  $s0, -8($fp)
ori $t0,$0,1
addu $s0,$s0, $t0
sw $s0, -8($fp)
j $loop1
nop
$loop3:
#//printf("y is : %d en int is : %i ",*px,x*x+89);
#//printf("y is : %d en int is : %i ",f,x*x+89);
li $v0, 0
lw $16, -52($fp)
lw $s6, -48($fp)
l.s $f12, -48($fp)
l.s $f11, -44($fp)
l.s $f10, -36($fp)
l.s $f9, -36($fp)
lw $s5, -32($fp)
lw $s4, -28($fp)
lw $s3, -24($fp)
lw $s2, -20($fp)
lw $s1, -16($fp)
l.s $f8, -12($fp)
l.s $f4, -28($fp)
l.s $f3, -24($fp)
l.s $f2, -12($fp)
l.s $f1, -12($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
