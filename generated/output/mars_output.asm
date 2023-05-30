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
#/**floatfff(intx,floatfx){float*px=&fx;float**ppx=&px;floatz=*px;floatf=90.9*z+z;return100.1;}**/#//intmain(intx,floatfx,intxi){inty;//scanf("%d%d", &x, &y);//scanf("%d%d", x, y);while(x<xi){x=x+1;break;}/**floatf=fff(1,2.2);float*px=&f;*px=fx;floatz=*px;floatff=90.9*(z)+z;while(x<xi){x=x+1;}//printf("y is : %d en int is : %i ",*px,x*x+89);printf("y is : %d en int is : %i ",f,x*x+89);**/return0;}
main: 
 sw	$fp, 0($sp)
move	$fp, $sp
subu	$sp, $sp,24
sw	$ra, -4($fp)
sw	$s0, -8($fp)
s.s   $f0, -12($fp)
sw	$s1, -16($fp)
sw	$s2, -20($fp)
#//intx
#//floatfx
#//intxi
#//inty
lw  $s2, -20($fp)
ori $s2,$0,0
sw  $s2, -20($fp)
#//scanf("%d%d", &x, &y);
#//scanf("%d%d", x, y);
#//while(x<xi){x=x+1;break;}
j $loop1
nop
$loop1:
lw  $s0, -8($fp)
lw  $s1, -16($fp)
slt $3,$s0, $s1
sw $3, -24($fp)
lbu $3, -24($fp)
andi  $3, $3, 1
beqz    $3, $loop3
nop 
j $loop2
nop
$loop2:
#//x=x+1
lw  $s0, -8($fp)
ori $t0,$0,1
addu $s0,$s0, $t0
sw $s0, -8($fp)
j loop3
nopj $loop1
nop
$loop3:
#/**floatf=fff(1,2.2);float*px=&f;*px=fx;floatz=*px;floatff=90.9*(z)+z;while(x<xi){x=x+1;}//printf("y is : %d en int is : %i ",*px,x*x+89);printf("y is : %d en int is : %i ",f,x*x+89);**/li $v0, 0
lw $3, -24($fp)
lw $s2, -20($fp)
lw $s1, -16($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
