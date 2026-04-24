# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | andrei-bley | https://github.com/andrei-bley
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | vitormpbilbao | https://github.com/vitormpbilbao

# Grupo: RA2 15
"""
Fase 2 do Compilador: Análise Sintática Descendente
Descrição:
    Implementa um parser LL(1) não-recursivo usando algoritmo de pilha
    para validar tokens contra a gramática fornecida pelo Aluno 1.
"""

from dataclasses import dataclass, field

try:
    from gramatica import calcularFirst, calcularFollow, construirTabelaLL1
except Exception as e:
    print(f"Erro ao importar módulos: {e}")
    pass


@dataclass
class NoArvore:
    rotulo: str  # Programa, Comando, Elemento
    tipo: str  # terminal ou nao_terminal
    valor: str | None = None  # Valor para terminais
    # importa construtor de lista vazia para evitar mutabilidade compartilhada (onibus fantasma)
    filhos: list["NoArvore"] = field(default_factory=list)

    # represenacao str de saida
    def __repr__(self) -> str:
        if self.tipo == "terminal":
            return f"NoArvore({self.rotulo}, '{self.valor}')"
        else:
            return f"NoArvore({self.rotulo}, filhos={len(self.filhos)})"

    def serializar(self):
        """Converte nó para dicionário (JSON-compatível)."""
        return {
            "rotulo": self.rotulo,
            "tipo": self.tipo,
            "valor": self.valor,
            "filhos": [filho.serializar() for filho in self.filhos],
        }


@dataclass
class ErroSintatico:
    numero_comando: int  # Qual comando tem erro
    indice_token: int  # Posição no token do comando
    esperado: str  # O que era esperado
    encontrado: str  # O que foi encontrado
    mensagem: str  # Mensagem descritiva completa

    # represenacao str de saida
    def __repr__(self) -> str:
        return f"ErroSintatico(cmd={self.numero_comando}[{self.indice_token}]: {self.mensagem})"


class ParserLL1:
    def __init__(self, gramatica):
        """Inicializa parser com gramática dinâmica (não hardcoded)."""
        self.gramatica = gramatica
        self.firsts = calcularFirst(gramatica)
        self.follows = calcularFollow(gramatica, self.firsts)
        self.tabela_ll1 = construirTabelaLL1(gramatica, self.firsts, self.follows)

        # Estado do parser
        self.tokens = []  # Tokens sendo processados
        self.posicao = 0  # Posição atual no buffer
        self.derivacoes = []  # Histórico de derivações
        self.erros = []  # Erros encontrados
        self.numero_comando = 0  # Qual comando está sendo processado

    def get_terminal(self, token: dict) -> str:
        if not token:
            return "$"

        tipo = token.get("tipo", "")
        valor = token.get("valor", "")

        if tipo == "PARENTESIS":
            return "PARENTESIS_ESQ" if valor == "(" else "PARENTESIS_DIR"
        elif tipo == "NUMERO":
            return "NUMERO"
        elif tipo == "VARIAVEL":
            return "VARIAVEL"
        elif tipo == "OPERADOR":
            return "OPERADOR"
        elif tipo == "COMANDO":
            # Retorna o valor específico: MEM, RES, IF, WHILE, IFELSE
            return valor
        else:
            return "DESCONHECIDO"

    def _is_terminal(self, simbolo: str) -> bool:
        # TODO: Verificar se isso aqui vai mudar deopis que a gramatica e a tokenizacao estiverem implementadas
        terminais = {
            "PARENTESIS_ESQ",
            "PARENTESIS_DIR",
            "NUMERO",
            "VARIAVEL",
            "OPERADOR",
            "START",
            "END",
            "MEM",
            "RES",
            "IF",
            "IFELSE",
            "WHILE",
            "FOR",
            "EPSILON",
            "$",
        }
        return simbolo in terminais

    def _next_token(self) -> dict | None:
        if self.indice_token < len(self.tokens_atuais):
            return self.tokens_atuais[self.indice_token]
        return None

    def _get_next_token(self) -> dict | None:
        token = self._next_token()
        if token:
            self.indice_token += 1
        return token

    def _add_erro(self, esperado: str, encontrado: str, contexto: str):
        erro = ErroSintatico(
            numero_comando=self.numero_comando,
            indice_token=self.indice_token,
            esperado=esperado,
            encontrado=encontrado,
            mensagem=f"Cmd {self.numero_comando}[{self.indice_token}]: "
            f"Esperado '{esperado}', encontrado '{encontrado}' ({contexto})",
        )
        self.erros.append(erro)

    def _combinar_terminal(self, esperado, contexto, no):
        """Combina um terminal esperado com o próximo token."""
        token = self._next_token()
        terminal = self.get_terminal(token)

        if terminal == esperado:
            self._get_next_token()
            if token:
                no_terminal = NoArvore(
                    esperado, "terminal", valor=token.get("valor", "")
                )
                no.filhos.append(no_terminal)
            return True
        else:
            self._add_erro(esperado, terminal, contexto)
            return False

    def _add_derivacao(self, derivacao: str):
        self.derivacoes.append(derivacao)

    def parser_programa(self):
        """Programa ::= ( START ) ListaOuFim"""
        no = NoArvore("Programa", "nao_terminal")

        if not self._combinar_terminal("PARENTESIS_ESQ", "inicio de programa", no):
            return None

        if not self._combinar_terminal("START", "palavra-chave START", no):
            return None

        if not self._combinar_terminal("PARENTESIS_DIR", "fim de START", no):
            return None

        lista_no = self.parser_lista_OuFim()
        if lista_no:
            no.filhos.append(lista_no)

        return no

    def parser_lista_OuFim(self):
        """ListaOuFim ::= ( ConteudoOuFim )"""
        no = NoArvore("ListaOuFim", "nao_terminal")

        if not self._combinar_terminal("PARENTESIS_ESQ", "inicio de ListaOuFim", no):
            return None

        conteudo_no = self.parser_conteudo_Fim()
        if conteudo_no:
            no.filhos.append(conteudo_no)

        if not self._combinar_terminal("PARENTESIS_DIR", "fim de ConteudoOuFim", no):
            return None

        return no

    def parser_conteudo_Fim(self):
        """ConteudoOuFim ::= END | Conteudo ListaOuFim"""
        no = NoArvore("ConteudoOuFim", "nao_terminal")

        token = self._next_token()
        if not token:
            return None

        terminal = self.get_terminal(token)

        # Caso 1: END
        if terminal == "END":
            no_end = NoArvore("END", "terminal", valor=token.get("valor"))
            no.filhos.append(no_end)
            self._get_next_token()
            self._add_derivacao("ConteudoOuFim -> END")
            return no

        # Caso 2: Conteudo ListaOuFim
        conteudo_no = self.parser_conteudo()
        if conteudo_no:
            no.filhos.append(conteudo_no)

            lista_no = self.parser_lista_OuFim()
            if lista_no:
                no.filhos.append(lista_no)

            self._add_derivacao("ConteudoOuFim -> Conteudo ListaOuFim")
            return no

        return None

    def parser_comando(self):
        """Comando ::= ( Conteudo )"""
        no = NoArvore("Comando", "nao_terminal")

        if not self._combinar_terminal("PARENTESIS_ESQ", "inicio de comando", no):
            return None

        conteudo_no = self.parser_conteudo()
        if conteudo_no:
            no.filhos.append(conteudo_no)

        if not self._combinar_terminal("PARENTESIS_DIR", "fim de comando", no):
            return None

        self._add_derivacao("Comando -> ( Conteudo )")
        return no

    def parser_conteudo(self):
        """Conteudo ::= Elemento RestoConteudo"""
        no = NoArvore("Conteudo", "nao_terminal")

        elem_no = self.parser_elemento()
        if elem_no:
            no.filhos.append(elem_no)

        resto_no = self.parser_resto_conteudo()
        if resto_no:
            no.filhos.append(resto_no)

        self._add_derivacao("Conteudo -> Elemento RestoConteudo")
        return no

    def parser_resto_conteudo(self):
        """RestoConteudo ::= Elemento Cauda | RES | epsilon"""
        no = NoArvore("RestoConteudo", "nao_terminal")

        token = self._next_token()
        if not token:
            self._add_derivacao("RestoConteudo -> epsilon")
            return no

        terminal = self.get_terminal(token)

        # Caso 1: RES
        if terminal == "RES":
            no_res = NoArvore("RES", "terminal", valor=token.get("valor"))
            no.filhos.append(no_res)
            self._get_next_token()
            self._add_derivacao("RestoConteudo -> RES")
            return no

        # Caso 2: Elemento Cauda
        if terminal in ["NUMERO", "VARIAVEL", "PARENTESIS_ESQ"]:
            elem_no = self.parser_elemento()
            if not elem_no:
                return None  # Erro ao parsear Elemento

            no.filhos.append(elem_no)

            cauda_no = self.parser_cauda()
            if cauda_no:
                no.filhos.append(cauda_no)

            self._add_derivacao("RestoConteudo -> Elemento Cauda")
            return no

    def parser_cauda(self):
        """Cauda ::= OPERADOR | MEM | IF | WHILE | FOR"""
        no = NoArvore("Cauda", "nao_terminal")

        token = self._next_token()
        if not token:
            self._add_derivacao("Cauda -> epsilon")
            return no

        terminal = self.get_terminal(token)

        if terminal == "OPERADOR":
            no_op = NoArvore("OPERADOR", "terminal", valor=token.get("valor"))
            no.filhos.append(no_op)
            self._get_next_token()
            self._add_derivacao("Cauda -> OPERADOR")
            return no
        elif terminal in ["MEM", "IF", "WHILE", "FOR"]:
            no_cmd = NoArvore(terminal, "terminal", valor=token.get("valor"))
            no.filhos.append(no_cmd)
            self._get_next_token()
            self._add_derivacao("Cauda -> %s" % terminal)
            return no

        # epsilon
        self._add_derivacao("Cauda -> epsilon")
        return no

    def parser_elemento(self):
        """Elemento ::= NUMERO | VARIAVEL | Comando"""
        no = NoArvore("Elemento", "nao_terminal")

        token = self._next_token()
        if not token:
            self._add_erro("Elemento", "$", "elemento")
            return None

        terminal = self.get_terminal(token)

        if terminal == "NUMERO":
            no_num = NoArvore("NUMERO", "terminal", valor=token.get("valor"))
            no.filhos.append(no_num)
            self._get_next_token()
            self._add_derivacao("Elemento -> NUMERO")
            return no
        elif terminal == "VARIAVEL":
            no_var = NoArvore("VARIAVEL", "terminal", valor=token.get("valor"))
            no.filhos.append(no_var)
            self._get_next_token()
            self._add_derivacao("Elemento -> VARIAVEL")
            return no
        elif terminal == "PARENTESIS_ESQ":
            cmd_no = self.parser_comando()
            if cmd_no:
                no.filhos.append(cmd_no)
                self._add_derivacao("Elemento -> Comando")
                return no

        self._add_erro("NUMERO/VARIAVEL/COMANDO", terminal, "elemento")
        return None

    def parser_comando_completo(self, tokens, num_comando):
        """Processa um único comando e retorna resultado estruturado."""
        self.tokens = tokens
        self.posicao = 0
        self.numero_comando = num_comando
        self.derivacoes = []
        self.erros = []

        arvore = self.parsearPrograma()

        return {
            "numero_comando": num_comando,
            "sucesso": arvore is not None and len(self.erros) == 0,
            "arvore": arvore.serializar() if arvore else None,
            "derivacoes": self.derivacoes,
            "erros": [
                {
                    "numero_comando": e.numero_comando,
                    "indice_token": e.indice_token,
                    "esperado": e.esperado,
                    "encontrado": e.encontrado,
                    "mensagem": e.mensagem,
                }
                for e in self.erros
            ],
        }


def agruparTokensPorComando(tokens_planificados: list[dict]) -> list[list[dict]]:
    """
    Agrupa tokens em comandos (cada comando começa e termina com parênteses).

    Entrada: [
        {'tipo': 'PARENTESIS', 'valor': '('},
        {'tipo': 'NUMERO', 'valor': '10'},
        {'tipo': 'VARIAVEL', 'valor': 'CONTADOR'},
        {'tipo': 'COMANDO', 'valor': 'MEM'},
        {'tipo': 'PARENTESIS', 'valor': ')'},
        ...
    ]

    Saída: [
        [{'tipo': 'PARENTESIS', 'valor': '('}, ...],
        [{'tipo': 'PARENTESIS', 'valor': '('}, ...],
    ]
    """
    comandos = []
    comando_atual = []
    profundidade = 0

    for token in tokens_planificados:
        if token["tipo"] == "PARENTESIS":
            if token["valor"] == "(":
                profundidade += 1
            elif token["valor"] == ")":
                profundidade -= 1

        comando_atual.append(token)

        # Comando termina quando profundidade volta a 0
        if profundidade == 0 and comando_atual:
            comandos.append(comando_atual)
            comando_atual = []

    return comandos


def parsear(tokens_planificados: list[dict], gramatica: str) -> dict:
    """
    Função principal - processa todos os comandos.

    Args:
        tokens_planificados: Lista única de tokens (do Aluno 3)
        gramatica: String da gramática (do Aluno 1)

    Returns:
        {
            'sucesso': bool,
            'resultados': [
                {
                    'numero_comando': int,
                    'sucesso': bool,
                    'derivacoes': list,
                    'arvore': dict,
                    'erros': list
                },
                ...
            ],
            'resumo': str
        }
    """
    parser = ParserLL1(gramatica)

    # Agrupar tokens por comando
    comandos = agruparTokensPorComando(tokens_planificados)

    resultados = []

    for num_cmd, tokens_cmd in enumerate(comandos, 1):
        resultado = parser.parsearComandoCompleto(tokens_cmd, num_cmd)
        resultados.append(resultado)

    # Resumo
    sucessos = sum(1 for r in resultados if r["sucesso"])
    total = len(resultados)

    return {
        "sucesso": all(r["sucesso"] for r in resultados),
        "resultados": resultados,
        "resumo": "%d/%d comandos válidos" % (sucessos, total),
    }


if __name__ == "__main__":
    print("Parser LL(1) Recursivo Descendente - Aluno 2")
    print("Com Gramática Dinâmica (não hardcoded)\n")

    # Gramática de teste
    gramatica = {
        "Programa": [["PARENTESIS_ESQ", "START", "PARENTESIS_DIR", "ListaOuFim"]],
        "ListaOuFim": [["PARENTESIS_ESQ", "ConteudoOuFim"]],
        "ConteudoOuFim": [
            ["END", "PARENTESIS_DIR"],
            ["Conteudo", "PARENTESIS_DIR", "ListaOuFim"],
        ],
        "Comando": [["PARENTESIS_ESQ", "Conteudo", "PARENTESIS_DIR"]],
        "Conteudo": [["Elemento", "RestoConteudo"]],
        "RestoConteudo": [["Elemento", "Cauda"], ["RES"], ["EPSILON"]],
        "Cauda": [["OPERADOR"], ["MEM"], ["IF"], ["WHILE"]],
        "Elemento": [["NUMERO"], ["VARIAVEL"], ["Comando"]],
    }

    parser = ParserLL1(gramatica)
    print("=== TABELA LL(1) GERADA COM SUCESSO ===")
    for nt, mapeamento in parser.tabela_ll1.items():
        print(f"\n[{nt}]:")
        for terminal, regra in mapeamento.items():
            print(f"  Se ler '{terminal}' -> Usar regra: {regra}")

    print("\n\n=== TESTES DE PARSING ===")

    # Teste 1: Programa simples com números
    tokens_teste1 = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "START"},
        {"tipo": "PARENTESIS", "valor": ")"},
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "123"},
        {"tipo": "PARENTESIS", "valor": ")"},
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "END"},
        {"tipo": "PARENTESIS", "valor": ")"},
    ]

    print("\nTeste 1: Programa com número")
    resultado = parser.parsearComandoCompleto(tokens_teste1, 1)
    print(f"Sucesso: {resultado['sucesso']}")
    print(f"Derivacoes: {resultado['derivacoes'][:5]}")
