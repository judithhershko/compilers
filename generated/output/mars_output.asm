.data
xx: .word 90
3:
  .word 1
  .word 2
  .word 3
y: .word -67195
z: .word 1
.text
.globl main
ff: 
addi $sp, $sp, -4        # allocate space for arguments on stack
sw $fp, 0($sp)           # save return address on stack
sw $ra, -4($sp)          # save frame pointer on stack
addi $fp, $sp, 4         # set up new frame pointer
#fucntion parameters
s.s $a0, 0 ($sp)
# Return from the function
jr $ra
f: 
addi $sp, $sp, -8        # allocate space for arguments on stack
sw $fp, 4($sp)           # save return address on stack
sw $ra, 0($sp)          # save frame pointer on stack
addi $fp, $sp, 8         # set up new frame pointer
#fucntion parameters
sw $a1, 0 ($sp)
s.s $a2, 4 ($sp)
# Return from the function
jr $ra
main: 
addi $sp, $sp, -24        # allocate space for arguments on stack
sw $fp, 20($sp)           # save return address on stack
sw $ra, 16($sp)          # save frame pointer on stack
addi $fp, $sp, 24         # set up new frame pointer
#fucntion parameters
# Return from the function
jr $ra
