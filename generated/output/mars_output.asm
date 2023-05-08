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
sw $ra, 0($sp)           # save return address on stack
sw $fp, -5($sp)          # save frame pointer on stack
addi $fp, $sp, 4         # set up new frame pointer
#fucntion parameters
s.s $1, 4($fp)
f: 
addi $sp, $sp, -8        # allocate space for arguments on stack
sw $ra, 4($sp)           # save return address on stack
sw $fp, -1($sp)          # save frame pointer on stack
addi $fp, $sp, 8         # set up new frame pointer
#fucntion parameters
sw $1, 8($fp)
s.s $1, 12($fp)
main: 
addi $sp, $sp, 0        # allocate space for arguments on stack
sw $ra, -4($sp)           # save return address on stack
sw $fp, -9($sp)          # save frame pointer on stack
addi $fp, $sp, 0         # set up new frame pointer
#fucntion parameters
