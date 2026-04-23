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
    def __init__(self):
        # Verifica import da gramatica ja que não existe um arquivo de gramatica.py nessa branch
        try:
            from gramatica import construirGramatica  # pyright: ignore[reportMissingImports]

            self.gramatica = construirGramatica()
        except ImportError:
            print("Aviso: gramatica.py não encontrado. Usando gramática vazia.")
            self.gramatica = {}

        # Estado do parser
        self.tokens_atuais = []  # Tokens sendo processados
        self.indice_token = 0  # Posição atual no buffer
        self.pilha_analise = []  # Pilha de símbolos para análise
        self.derivacoes = []  # Histórico de derivações (debug)
        self.arvore = None  # Árvore sintática resultante
        self.erros = []  # Lista de erros encontrados
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


if __name__ == "__main__":
    print("Estruturas de dados importadas com sucesso!")

    no = NoArvore("Programa", "nao_terminal")
    print(f"   No: {no}")

    erro = ErroSintatico(
        1, 5, "NUMERO", "VARIAVEL", "Esperado NUMERO, encontrado VARIAVEL"
    )
    print(f"   Erro: {erro}")
