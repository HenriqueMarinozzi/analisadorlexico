.syntax unified
.arch_extension idiv
.global _start
_start:
  LDR r0, =fconst_0
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VADD.F32 S2, S0, S1
  MOV r2, #3
  VMOV S3, r2
  VCVT.F32.S32 S3, S3
  VMUL.F32 S4, S2, S3
  LDR r3, =result_1
  VSTR S4, [r3]
  LDR r0, =fconst_2
  VLDR S0, [r0]
  LDR r1, =addr_X
  VSTR S0, [r1]
  LDR r2, =addr_X
  VLDR S1, [r2]
  LDR r3, =result_2
  VSTR S1, [r3]
  MOV r0, #10
  MOV r1, #2
  SDIV r0, r0, r1
  MOV r2, #3
  MOV r3, #1
  ADD r2, r2, r3
  MUL r0, r0, r2
  LDR r4, =result_3
  STR r0, [r4]
  LDR r0, =fconst_3
  VLDR S0, [r0]
  LDR r1, =addr_Y
  VSTR S0, [r1]
  LDR r2, =addr_Y
  VLDR S1, [r2]
  LDR r3, =result_4
  VSTR S1, [r3]
  MOV r0, #1
  LDR r1, =result_4
  VLDR S0, [r1]
  MOV r2, #2
  VMOV S1, r2
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S0, S1
  LDR r3, =result_5
  VSTR S2, [r3]
  MOV r0, #8
  MOV r1, #3
  SDIV r2, r0, r1
  MLS r0, r2, r1, r0
  MOV r3, #2
  MOV r4, #1
  MOV r5, r0
pow_loop_0:
  CMP r3, #0
  BEQ pow_end_0
  MUL r4, r4, r5
  SUB r3, r3, #1
  B pow_loop_0
pow_end_0:
  LDR r6, =result_6
  STR r4, [r6]
  LDR r0, =fconst_4
  VLDR S0, [r0]
  LDR r1, =fconst_5
  VLDR S1, [r1]
  LDR r2, =fconst_1
  VLDR S2, [r2]
  VSUB.F32 S3, S1, S2
  VMUL.F32 S4, S0, S3
  LDR r3, =result_7
  VSTR S4, [r3]
  MOV r0, #7
  MOV r1, #2
  MUL r0, r0, r1
  MOV r2, #3
  MOV r3, #3
  MUL r2, r2, r3
  VMOV S0, r0
  VCVT.F32.S32 S0, S0
  VMOV S1, r2
  VCVT.F32.S32 S1, S1
  VDIV.F32 S2, S0, S1
  LDR r4, =result_8
  VSTR S2, [r4]
  LDR r0, =fconst_6
  VLDR S0, [r0]
  LDR r1, =fconst_7
  VLDR S1, [r1]
  VSUB.F32 S2, S0, S1
  LDR r2, =addr_Z
  VSTR S2, [r2]
  LDR r0, =addr_Z
  VLDR S0, [r0]
  MOV r1, #4
  VMOV S1, r1
  VCVT.F32.S32 S1, S1
  VMUL.F32 S2, S0, S1
  LDR r2, =result_10
  VSTR S2, [r2]
  LDR r0, =fconst_8
  VLDR S0, [r0]
  LDR r1, =fconst_9
  VLDR S1, [r1]
  VADD.F32 S2, S0, S1
  LDR r2, =result_11
  VSTR S2, [r2]
  MOV r0, #5
  LDR r1, =result_7
  VLDR S0, [r1]
  LDR r2, =result_12
  VSTR S0, [r2]
  LDR r0, =fconst_10
  VLDR S0, [r0]
  LDR r1, =addr_CONTADOR
  VSTR S0, [r1]

.data
  addr_X: .word 0
  addr_Y: .word 0
  addr_Z: .word 0
  addr_CONTADOR: .word 0
  result_1: .float 0.0
  result_2: .float 0.0
  result_3: .word 0
  result_4: .float 0.0
  result_5: .float 0.0
  result_6: .word 0
  result_7: .float 0.0
  result_8: .float 0.0
  result_10: .float 0.0
  result_11: .float 0.0
  result_12: .float 0.0
  fconst_0: .float 2.5
  fconst_1: .float 1.5
  fconst_2: .float 4.0
  fconst_3: .float 6.0
  fconst_4: .float 5.5
  fconst_5: .float 6.5
  fconst_6: .float 9.0
  fconst_7: .float 1.0
  fconst_8: .float 3.14
  fconst_9: .float 2.0
  fconst_10: .float 10.5