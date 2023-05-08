.data
xx: .word 90
yy:
  .word 1
  .word 2
  .word 3
y: .word -67195
z: .word 1
.text
.globl main
ff: 
addi $sp, $sp, 0        # allocate space for arguments on stack
sw $fp, -4($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
s.s $a0, 0($sp)
lw   $fp, -4($sp)       # restore old frame pointer
addi $sp, $sp, 0       # deallocate stack space
jr $ra
f: 
addi $sp, $sp, -4        # allocate space for arguments on stack
sw $fp, 0($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
sw $a1, 0($sp)
s.s $a2, 4($sp)
lwc1 $f0, 0($sp)        # load the return value from stack to $f0
lw   $fp, 0($sp)       # restore old frame pointer
addi $sp, $sp, -4       # deallocate stack space
jr $ra
main: 
addi $sp, $sp, 4        # allocate space for arguments on stack
sw $fp, -8($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
li   $v0, 1            # set return value
lw   $fp, -8($sp)       # restore old frame pointer
addi $sp, $sp, 4       # deallocate stack space
jr $ra
