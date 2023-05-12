.data
.text
.globl main
main: 
addi $sp, $sp, 4        # allocate space for arguments on stack
sw $fp, -8($sp)           # save return address on stack
move $fp, $sp           # set new frame pointer
#fucntion parameters
lw   $fp, -8($sp)       # restore old frame pointer
addi $sp, $sp, 4       # deallocate stack space
jr $ra
