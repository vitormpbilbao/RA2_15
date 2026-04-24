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
from gramatica import calcularFirst, calcularFollow, construirTabelaLL1  # pyright: ignore[reportMissingImports] # noqa: F401


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

    def _add_erro(self, esperado: str, encontrado: str):
        erro = ErroSintatico(
            numero_comando=self.numero_comando,
            indice_token=self.indice_token,
            esperado=esperado,
            encontrado=encontrado,
            mensagem=f"Cmd {self.numero_comando}[{self.indice_token}]: "
            f"Esperado '{esperado}', encontrado '{encontrado}'",
        )
        self.erros.append(erro)

    def _combinarTerminal(self, esperado, contexto, no):
        """Combina um terminal esperado com o próximo token."""
        token = self._proximoToken()
        terminal = self.obterTerminal(token)

        if terminal == esperado:
            self._avancarToken()
            if token:
                no_terminal = NoArvore(
                    esperado, "terminal", valor=token.get("valor", "")
                )
                no.filhos.append(no_terminal)
            return True
        else:
            self._adicionarErro(esperado, terminal, contexto)
            return False

    def _add_derivacao(self, derivacao: str):
        self.derivacoes.append(derivacao)

    def parsearComando(self, tokens: list[dict], num_comando: int) -> dict:
        # TODO MELHORAR A DOCSTR
        # TODO ATUALIZAR ESSA FUNÇÃO DEPOIS QUE A GRAMÁTICA ESTIVER DEFINIDA, JA QUE ISSO VAI MUDAR MUITO O FLUXO DO PARSER
        """
        Algoritmo LL(1) não-recursivo com pilha.

        Algoritmo:
        1. Inicializar pilha com ['$', 'Programa']
        2. Enquanto pilha não vazia:
           a. Se topo == terminal: combinar com entrada
           b. Se topo == não-terminal: consultar gramática
           c. Se topo == '$': verificar EOF
        """
        self.tokens_atuais = tokens
        self.indice_token = 0
        self.numero_comando = num_comando
        self.pilha_analise = ["$", "Programa"]
        self.derivacoes = []
        self.erros = []
        self.arvore = NoArvore("Programa", "nao_terminal")

        while self.pilha_analise:
            topo = self.pilha_analise[-1]
            token_atual = self._next_token()
            terminal_atual = self.get_terminal(token_atual) if token_atual else "$"

            # Caso 1: Topo é terminal - deve combinar
            if self._is_terminal(topo):
                if topo == terminal_atual:
                    print(f"Combina: {topo}")
                    self._get_next_token()
                    self.pilha_analise.pop()
                else:
                    self._add_erro(esperado=topo, encontrado=terminal_atual)
                    return self._construir_resultado(sucesso=False)

            # Caso 2: Topo é $ (marcador de fim)
            elif topo == "$":
                if terminal_atual == "$":
                    print("Programa reconhecido")
                    self.pilha_analise.pop()
                else:
                    self._add_erro(esperado="EOF", encontrado=terminal_atual)
                    return self._construir_resultado(sucesso=False)

            # Caso 3: Topo é não-terminal - usar gramática
            else:
                regras = self.gramatica.get(topo, [])

                # Encontrar regra correta
                regra_aplicada = self._selecionar_regra(terminal_atual, regras)

                if regra_aplicada is None:
                    self._add_erro(
                        esperado=f"Nao-terminal '{topo}'",
                        encontrado=terminal_atual,
                    )
                    return self._construir_resultado(sucesso=False)

                # Aplicar regra: substituir topo por derivação (inverso)
                self.pilha_analise.pop()
                for simbolo in reversed(regra_aplicada):
                    if simbolo != "EPSILON":
                        self.pilha_analise.append(simbolo)

                self._add_derivacao(f"{topo} → {' '.join(regra_aplicada)}")

        return self._construir_resultado(sucesso=True)

    def _construir_resultado(self, sucesso: bool) -> dict:
        """Constrói dicionário de resultado do parsing."""
        return {
            "numero_comando": self.numero_comando,
            "sucesso": sucesso and len(self.erros) == 0,
            "derivacoes": self.derivacoes,
            "arvore": self._serializar_arvore(self.arvore),
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


def parsear(tokens_planificados: list[dict]) -> dict:
    """
    Função principal - processa todos os comandos.

    Args:
        tokens_planificados: Lista única de tokens (do Aluno 3)

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
    parser = ParserLL1()

    # Agrupar tokens por comando
    comandos = agruparTokensPorComando(tokens_planificados)

    resultados = []

    for num_cmd, tokens_cmd in enumerate(comandos, 1):
        print(f"\nComando {num_cmd}: {[t['valor'] for t in tokens_cmd]}")

        resultado = parser.parsearComando(tokens_cmd, num_cmd)
        resultados.append(resultado)

    return {
        "sucesso": all(r["sucesso"] for r in resultados),
        "resultados": resultados,
        "resumo": f"{sum(1 for r in resultados if r['sucesso'])}/{len(resultados)} comandos válidos",
    }


if __name__ == "__main__":
    print("Rodando o PARSER LL(1)")

    print("\nEstruturas de dados:")
    no = NoArvore("Programa", "nao_terminal")
    print(f"   No: {no}")

    erro = ErroSintatico(
        1, 5, "NUMERO", "VARIAVEL", "Esperado NUMERO, encontrado VARIAVEL"
    )
    print(f"   Erro: {erro}")

    print("\nClasse ParserLL1:")
    parser = ParserLL1()
    print(f"   Não-terminais: {list(parser.gramatica.keys())}")
    print(
        f"   Total de regras: {sum(len(regras) for regras in parser.gramatica.values())}"
    )
