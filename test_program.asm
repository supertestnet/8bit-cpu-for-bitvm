start:
  STA 14
  ADD 15
  JC continue
  JMP start

continue:
  SUB 15
  STA 14
  JC start
  JMP continue
  
  .org 15
  .word 50
