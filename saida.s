.data
    .align 3
    memoria_res: .space 800
    const_um: .double 1.0
    num_0: .double 1
    var_I: .double 0.0
    num_1: .double 0
    var_SOMA: .double 0.0
    num_2: .double 2.5
    var_FATOR: .double 0.0
    num_3: .double 8
    var_N: .double 0.0
    num_4: .double 3
    num_5: .double 4
    num_6: .double 2
    num_7: .double 1
    zero_while_0: .double 0.0
    rel_true_8: .double 1.0
    rel_false_8: .double 0.0
    num_10: .double 1
    num_11: .double 1
    rel_true_12: .double 1.0
    rel_false_12: .double 0.0
    zero_if_0: .double 0.0
    num_14: .double 2
    num_15: .double 3
    num_16: .double 2

.text
.global _start
_start:
    @ START
    LDR r0, =num_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_I
    VSTR.F64 d0, [r0]
    LDR r0, =num_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_SOMA
    VSTR.F64 d0, [r0]
    LDR r0, =num_2
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_FATOR
    VSTR.F64 d0, [r0]
    LDR r0, =num_3
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_N
    VSTR.F64 d0, [r0]
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VADD.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VSUB.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VMUL.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_4
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ Iniciando operacao de Divisao Inteira ou Modulo
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VCVT.S32.F64 s0, d0
    VCVT.F64.S32 d0, s0
    @ Calculando o Modulo: A - (A//B * B)
    VMUL.F64 d0, d0, d1
    VSUB.F64 d0, d2, d0
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_5
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
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ Iniciando operacao de Divisao Inteira ou Modulo
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VCVT.S32.F64 s0, d0
    VCVT.F64.S32 d0, s0
    VPUSH {d0}
    LDR r0, =num_6
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ RES: recupera resultado anterior
    VPOP {d1}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LSL r1, r1, #3
    LDR r0, =memoria_res
    ADD r0, r0, r1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_7
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ RES: recupera resultado anterior
    VPOP {d1}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LSL r1, r1, #3
    LDR r0, =memoria_res
    ADD r0, r0, r1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VMUL.F64 d0, d2, d1
    VPUSH {d0}
inicio_while_0:
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_N
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCMPE.F64 d2, d1
    VMRS APSR_nzcv, FPSCR
    BLE rel_verdadeiro_8
    LDR r0, =rel_false_8
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    B rel_fim_8
rel_verdadeiro_8:
    LDR r0, =rel_true_8
    VLDR.F64 d0, [r0]
    VPUSH {d0}
rel_fim_8:
    @ WHILE: testa condição
    VPOP {d0}
    LDR r0, =zero_while_0
    VLDR.F64 d1, [r0]
    VCMPE.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_while_0
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VADD.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_SOMA
    VSTR.F64 d0, [r0]
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_10
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VADD.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_I
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_I
    VSTR.F64 d0, [r0]
    B inicio_while_0
fim_while_0:
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_11
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCMPE.F64 d2, d1
    VMRS APSR_nzcv, FPSCR
    BEQ rel_verdadeiro_12
    LDR r0, =rel_false_12
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    B rel_fim_12
rel_verdadeiro_12:
    LDR r0, =rel_true_12
    VLDR.F64 d0, [r0]
    VPUSH {d0}
rel_fim_12:
    @ IF: testa condição no topo da pilha
    VPOP {d0}
    LDR r0, =zero_if_0
    VLDR.F64 d1, [r0]
    VCMPE.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_if_0
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_14
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VMUL.F64 d0, d2, d1
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ MEM: armazena valor na variável
    VPOP {d1}
    VPOP {d0}
    LDR r0, =var_SOMA
    VSTR.F64 d0, [r0]
fim_if_0:
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_15
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    @ Iniciando operacao de Divisao Inteira ou Modulo
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VCVT.S32.F64 s0, d0
    VCVT.F64.S32 d0, s0
    @ Calculando o Modulo: A - (A//B * B)
    VMUL.F64 d0, d0, d1
    VSUB.F64 d0, d2, d0
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =num_16
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LDR r0, =const_um
    VLDR.F64 d0, [r0]
loop_pot_1:
    CMP r1, #0
    BLE fim_pot_1
    VMUL.F64 d0, d0, d2
    SUB r1, r1, #1
    B loop_pot_1
fim_pot_1:
    VPUSH {d0}
    LDR r0, =var_SOMA
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_FATOR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}
    VPOP {d2}
    VDIV.F64 d0, d2, d1
    VPUSH {d0}
    @ END
    BX lr
