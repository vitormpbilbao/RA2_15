# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | andrei-bley | https://github.com/andrei-bley
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | vitormpbilbao | https://github.com/vitormpbilbao

# Grupo: RA2 15
# ==========================================
# Responsável: Vitor Matias, Andrei Bley e Vinicius Cordeiro
# ==========================================

import json

# ==============================================================================
# SEÇÃO 1 — ESTRUTURA DA ÁRVORE
# ==============================================================================
class No:
    def __init__(self, rotulo: str, tipo: str, valor=None):
        self.rotulo = rotulo
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def adicionar_filho(self, filho: "No"):
        self.filhos.append(filho)

    def serializar(self) -> dict:
        return {
            "rotulo": self.rotulo,
            "tipo": self.tipo,
            "valor": self.valor,
            "filhos": [filho.serializar() for filho in self.filhos],
        }

    def __repr__(self):
        if self.tipo == "terminal":
            return f"No({self.rotulo}, '{self.valor}')"
        return f"No({self.rotulo}, filhos={len(self.filhos)})"

# ==============================================================================
# SEÇÃO 2 — gerarArvore
# ==============================================================================
def _reconstruir_no(dados: dict) -> No:
    no = No(
        rotulo=dados["rotulo"],
        tipo=dados["tipo"],
        valor=dados.get("valor"),
    )
    for filho_dict in dados.get("filhos", []):
        no.adicionar_filho(_reconstruir_no(filho_dict))
    return no

def gerarArvore(derivacao: dict) -> list:
    arvores = []
    for resultado in derivacao.get("resultados", []):
        if resultado.get("sucesso") and resultado.get("arvore"):
            no = _reconstruir_no(resultado["arvore"])
            arvores.append(no)
        else:
            arvores.append(None)
    return arvores

# ==============================================================================
# SEÇÃO 3 — VISUALIZAÇÃO DA ÁRVORE
# ==============================================================================
def imprimir_arvore(no: No, prefixo: str = "", ultimo: bool = True) -> str:
    if no is None:
        return "[ERRO SINTÁTICO]\n"

    conector = "└─ " if ultimo else "├─ "
    if no.valor is not None:
        linha = f"{prefixo}{conector}{no.rotulo}: '{no.valor}'\n"
    else:
        linha = f"{prefixo}{conector}{no.rotulo}\n"

    novo_prefixo = prefixo + ("   " if ultimo else "│  ")
    resultado = linha

    for i, filho in enumerate(no.filhos):
        eh_ultimo = (i == len(no.filhos) - 1)
        resultado += imprimir_arvore(filho, novo_prefixo, eh_ultimo)

    return resultado

def salvar_arvore_json(arvores: list, nome_arquivo: str = "arvore.json"):
    dados = []
    for i, arvore in enumerate(arvores, 1):
        if arvore is not None:
            dados.append({
                "instrucao": i,
                "arvore": arvore.serializar()
            })
        else:
            dados.append({
                "instrucao": i,
                "arvore": None,
                "erro": "instrução com erro sintático"
            })

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ==============================================================================
# SEÇÃO 4 — gerarAssembly
# ==============================================================================
class GeradorAssembly:
    def __init__(self):
        self.codigo_data = ".data\n    .align 3\n    memoria_res: .space 800\n    const_um: .double 1.0\n"
        self.codigo_text = "\n.text\n.global _start\n_start:\n"
        self.variaveis_criadas = []
        self.contador_literais = 0
        self.contador_loops = 0
        self.contador_if = 0
        self.contador_while = 0
        self.ultima_variavel = None

    def _gerar_literal(self, valor: str) -> str:
        nome = f"num_{self.contador_literais}"
        self.codigo_data += f"    {nome}: .double {valor}\n"
        self.contador_literais += 1
        return f"    LDR r0, ={nome}\n    VLDR.F64 d0, [r0]\n    VPUSH {{d0}}\n"

    def _gerar_variavel(self, valor: str) -> str:
        self.ultima_variavel = valor
        if valor not in self.variaveis_criadas:
            self.codigo_data += f"    var_{valor}: .double 0.0\n"
            self.variaveis_criadas.append(valor)
        return f"    LDR r0, =var_{valor}\n    VLDR.F64 d0, [r0]\n    VPUSH {{d0}}\n"

    def _gerar_operador_aritmetico(self, op: str) -> str:
        instrucao = {
            "+": "VADD.F64 d0, d2, d1",
            "-": "VSUB.F64 d0, d2, d1",
            "*": "VMUL.F64 d0, d2, d1",
            "/": "VDIV.F64 d0, d2, d1",
            "|": "VDIV.F64 d0, d2, d1",
        }[op]
        return (
            "    VPOP {d1}\n"
            "    VPOP {d2}\n"
            f"    {instrucao}\n"
            "    VPUSH {d0}\n"
        )

    def _gerar_divisao_inteira(self, op: str) -> str:
        """Gera código para // (divisão inteira) e % (resto) usando FPU."""
        cod = (
            "    @ Iniciando operacao de Divisao Inteira ou Modulo\n"
            "    VPOP {d1}\n"
            "    VPOP {d2}\n"
            "    VDIV.F64 d0, d2, d1\n"      # 1. Faz a divisão real: d0 = A / B
            "    VCVT.S32.F64 s0, d0\n"      # 2. Converte pra Int (isso trunca/joga fora a fração)
            "    VCVT.F64.S32 d0, s0\n"      # 3. Volta pra Float redondo: d0 = int(A/B)
        )
        
        if op == "%":
            cod += (
                "    @ Calculando o Modulo: A - (A//B * B)\n"
                "    VMUL.F64 d0, d0, d1\n"  # d0 = int(A/B) * B
                "    VSUB.F64 d0, d2, d0\n"  # d0 = A - d0
            )
            
        cod += "    VPUSH {d0}\n"
        return cod

    def _gerar_potencia(self) -> str:
        n = self.contador_loops
        self.contador_loops += 1
        return (
            "    VPOP {d1}\n"
            "    VPOP {d2}\n"
            "    VCVT.S32.F64 s1, d1\n"
            "    VMOV r1, s1\n"
            "    LDR r0, =const_um\n"
            "    VLDR.F64 d0, [r0]\n"
            f"loop_pot_{n}:\n"
            "    CMP r1, #0\n"
            f"    BLE fim_pot_{n}\n"
            "    VMUL.F64 d0, d0, d2\n"
            "    SUB r1, r1, #1\n"
            f"    B loop_pot_{n}\n"
            f"fim_pot_{n}:\n"
            "    VPUSH {d0}\n"
        )

    def _gerar_relacional(self, op: str) -> str:
        desvio = {
            ">":  "BGT",
            "<":  "BLT",
            ">=": "BGE",
            "<=": "BLE",
            "==": "BEQ",
            "!=": "BNE",
        }[op]
        n = self.contador_literais
        self.codigo_data += f"    rel_true_{n}: .double 1.0\n"
        self.codigo_data += f"    rel_false_{n}: .double 0.0\n"
        self.contador_literais += 2
        return (
            "    VPOP {d1}\n"
            "    VPOP {d2}\n"
            "    VCMPE.F64 d2, d1\n"
            "    VMRS APSR_nzcv, FPSCR\n"
            f"    {desvio} rel_verdadeiro_{n}\n"
            f"    LDR r0, =rel_false_{n}\n"
            "    VLDR.F64 d0, [r0]\n"
            "    VPUSH {d0}\n"
            f"    B rel_fim_{n}\n"
            f"rel_verdadeiro_{n}:\n"
            f"    LDR r0, =rel_true_{n}\n"
            "    VLDR.F64 d0, [r0]\n"
            "    VPUSH {d0}\n"
            f"rel_fim_{n}:\n"
        )

    def _gerar_if(self, filhos_corpo: list) -> str:
        n = self.contador_if
        self.contador_if += 1
        self.codigo_data += f"    zero_if_{n}: .double 0.0\n"

        cod = (
            "    @ IF: testa condição no topo da pilha\n"
            "    VPOP {d0}\n"
            f"    LDR r0, =zero_if_{n}\n"
            "    VLDR.F64 d1, [r0]\n"
            "    VCMPE.F64 d0, d1\n"
            "    VMRS APSR_nzcv, FPSCR\n"
            f"    BEQ fim_if_{n}\n"
        )
        for filho in filhos_corpo:
            cod += self._visitar(filho)
        cod += f"fim_if_{n}:\n"
        return cod

    def _gerar_while(self, filhos_condicao: list, filhos_corpo: list) -> str:
        n = self.contador_while
        self.contador_while += 1
        self.codigo_data += f"    zero_while_{n}: .double 0.0\n"

        cod = f"inicio_while_{n}:\n"
        for filho in filhos_condicao:
            cod += self._visitar(filho)
        cod += (
            "    @ WHILE: testa condição\n"
            "    VPOP {d0}\n"
            f"    LDR r0, =zero_while_{n}\n"
            "    VLDR.F64 d1, [r0]\n"
            "    VCMPE.F64 d0, d1\n"
            "    VMRS APSR_nzcv, FPSCR\n"
            f"    BEQ fim_while_{n}\n"
        )
        for filho in filhos_corpo:
            cod += self._visitar(filho)
        cod += f"    B inicio_while_{n}\n"
        cod += f"fim_while_{n}:\n"
        return cod

    def _visitar(self, no: No) -> str:
        if no is None:
            return ""

        cod = ""

        if no.tipo == "terminal":
            if no.rotulo == "NUMERO":
                cod += self._gerar_literal(no.valor)
            elif no.rotulo == "VARIAVEL":
                cod += self._gerar_variavel(no.valor)
            elif no.rotulo == "OPERADOR":
                if no.valor in ("+", "-", "*", "/", "|"):
                    cod += self._gerar_operador_aritmetico(no.valor)
                elif no.valor in ("//", "%"):
                    cod += self._gerar_divisao_inteira(no.valor)
                elif no.valor == "^":
                    cod += self._gerar_potencia()
                elif no.valor in (">", "<", ">=", "<=", "==", "!="):
                    cod += self._gerar_relacional(no.valor)
            elif no.rotulo == "MEM":
                cod += (
                    "    @ MEM: armazena valor na variável\n"
                    "    VPOP {d1}\n"
                    "    VPOP {d0}\n"
                    f"    LDR r0, =var_{self.ultima_variavel}\n"
                    "    VSTR.F64 d0, [r0]\n"
                )
            elif no.rotulo == "RES":
                cod += (
                    "    @ RES: recupera resultado anterior\n"
                    "    VPOP {d1}\n"
                    "    VCVT.S32.F64 s1, d1\n"
                    "    VMOV r1, s1\n"
                    "    LSL r1, r1, #3\n"
                    "    LDR r0, =memoria_res\n"
                    "    ADD r0, r0, r1\n"
                    "    VLDR.F64 d0, [r0]\n"
                    "    VPUSH {d0}\n"
                )
            elif no.rotulo in ("START", "END"):
                cod += f"    @ {no.rotulo}\n"
        else:
            # ---------------------------------------------------------
            # MÁGICA DA ARQUITETURA SÊNIOR
            # Interceptando o IF e WHILE para extrair Condição e Corpo
            # ---------------------------------------------------------
            if no.rotulo == "Conteudo" and len(no.filhos) == 2 and no.filhos[1].rotulo == "RestoConteudo":
                condicao = no.filhos[0]
                resto = no.filhos[1]
                
                if len(resto.filhos) == 2 and resto.filhos[1].rotulo == "Cauda":
                    corpo = resto.filhos[0]
                    cauda = resto.filhos[1]
                    
                    if cauda.filhos and cauda.filhos[0].valor == "IF":
                        cod += self._visitar(condicao)     # Avalia a condição primeiro
                        cod += self._gerar_if([corpo])     # Joga o corpo para dentro do bloco IF
                        return cod
                        
                    elif cauda.filhos and cauda.filhos[0].valor == "WHILE":
                        cod += self._gerar_while([condicao], [corpo]) # Joga ambos para o laço
                        return cod

            # Se não for um caso especial de controle, apenas visita os filhos na ordem
            for filho in no.filhos:
                cod += self._visitar(filho)

        return cod

    def gerar(self, arvores: list) -> str:
        for arvore in arvores:
            if arvore is not None:
                self.codigo_text += self._visitar(arvore)
        self.codigo_text += "    BX lr\n"
        return self.codigo_data + self.codigo_text

def gerarAssembly(arvores: list) -> str:
    gerador = GeradorAssembly()
    return gerador.gerar(arvores)