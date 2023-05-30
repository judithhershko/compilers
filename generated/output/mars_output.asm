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
#/**floatfff(intx,floatfx){float*px=&fx;float**ppx=&px;floatz=*px;floatf=90.9*z+z;return100.1;}**/#//intmain(intx,floatfx,intxi){inty;//scanf("%d%d", &x, &y);scanf("%d%d",x,y);/**floatf=fff(1,2.2);float*px=&f;*px=fx;floatz=*px;floatff=90.9*(z)+z;while(x<xi){x=x+1;}//printf("y is : %d en int is : %i ",*px,x*x+89);printf("y is : %d en int is : %i ",f,x*x+89);**/return0;}
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
#//scanf("%d%d",x,y)
li $v0, 5
syscall
sw $s0, -8($fp)
move $s0, $v0
lw $s0, -8($fp)
li $v0, 5
syscall
sw $s3, -20($fp)
sw $s3, -20($fp)
move $s3, $v0
lw $s3, -20($fp)
#/**floatf=fff(1,2.2);float*px=&f;*px=fx;floatz=*px;floatff=90.9*(z)+z;while(x<xi){x=x+1;}//printf("y is : %d en int is : %i ",*px,x*x+89);printf("y is : %d en int is : %i ",f,x*x+89);**/li $v0, 0
lw $s3, -20($fp)
lw $s2, -20($fp)
lw $s1, -16($fp)
l.s $f0, -12($fp)
lw $s0, -8($fp)
lw	$ra, -4($fp)
move	$sp, $fp
lw	$fp, ($sp)
li  $v0,10
syscall
