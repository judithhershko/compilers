.data
x: .word 90
.text
.globl main
f: 
addi $sp, $sp, -4        # allocate space for arguments on stack
sw $fp, 0($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
sw $a0, 0($sp)
sw $a1, 4($sp)
lw   $fp, 0($sp)       # restore old frame pointer
addi $sp, $sp, -4       # deallocate stack space
jr $ra
main: 
addi $sp, $sp, 4        # allocate space for arguments on stack
sw $fp, -8($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
li   $v0, 0            # set return value
lw   $fp, -8($sp)       # restore old frame pointer
addi $sp, $sp, 4       # deallocate stack space
jr $ra
