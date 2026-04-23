.data
    .align 3
    memoria_res: .space 800
    const_um: .double 1.0
    num_0: .double 10
    var_CONTADOR: .double 0.0
    num_1: .double 3.14
    var_PI: .double 0.0
    num_2: .double 3
    num_3: .double 2
    num_4: .double 2
    num_5: .double 5.0
    num_6: .double 2.0
    num_7: .double 1
    num_8: .double 2.5

.text
.global _start
_start:
    LDR r0, =num_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_CONTADOR
    VSTR.F64 d0, [r0]
    LDR r0, =num_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_PI
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_PI
    VSTR.F64 d0, [r0]
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_PI
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VADD.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_PI
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VSUB.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_PI
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VMUL.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_PI
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_2
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCVT.S32.F64 s1, d1
    VCVT.S32.F64 s2, d2
    VMOV r1, s1
    VMOV r0, s2
    SDIV r2, r0, r1
    MLS r3, r2, r1, r0
    VMOV s0, r3
    VCVT.F64.S32 d0, s0
    VPUSH {d0}
    LDR r0, =var_CONTADOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_3
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LDR r0, =const_um
    VLDR.F64 d0, [r0]
loop_pot_0:
    CMP r1, #0
    BLE fim_pot_0
    VMUL.F64 d0, d0, d2
    SUB r1, r1, #1
    B loop_pot_0
fim_pot_0:
    VPUSH {d0}
    LDR r0, =num_4
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LSL r1, r1, #3
    LDR r0, =memoria_res
    ADD r0, r0, r1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_5
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_6
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCVT.S32.F64 s1, d1
    VCVT.S32.F64 s2, d2
    VMOV r1, s1
    VMOV r0, s2
    SDIV r2, r0, r1
    VMOV s0, r2
    VCVT.F64.S32 d0, s0
    VPUSH {d0}
    LDR r0, =num_7
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LSL r1, r1, #3
    LDR r0, =memoria_res
    ADD r0, r0, r1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_8
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VADD.F64 d0, d2, d1
    VPUSH {d0}
    BX lr
